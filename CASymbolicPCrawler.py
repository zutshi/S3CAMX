#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import logging
import numpy as np

# import matplotlib
# matplotlib.use('GTK3Agg')
# import matplotlib.pyplot as plt

import fileOps as fp
import smtSolver as smt
import state as st
import utils
import sample
import err
# import controlifc as cifc

import time

logger = logging.getLogger(__name__)

MAX_NUM_VARS_EXPECTED = 100000

IV = 'iv'
RV = 'rv'
SI = 'SI'
SF = 'SF'
U = 'U'
X = 'X'
I = 'ci'


class ControllerSymbolicAbstraction:

    # @staticmethod
    # def get_abs_state(s):
    #    return ControllerSymbolicAbstractState(s)

    @staticmethod
    def get_paths(solver, controller_path_dir_path, decls):
        path = controller_path_dir_path

        # get path files, which are in smt2 format with the same extension
        # ##!!##logger.debug('reading files(controller_paths) form {}'.format(path))

        filenames = glob.glob(path + '*.smt2')
        path_dict = {}
        for (idx, f) in enumerate(filenames):

            # ##!!##logger.debug('reading path: {}'.format(f))

            smt_string = fp.get_data(f)
            pc = solver.smt2_2_constraints(smt_string, decls)
            path_dict[str(idx)] = pc
        return path_dict

    def __init__(
            self,
            num_dims,
            controller_path_dir_path,
            max_hd=0,
            ):

        # ##!!##logger.debug('ControllerSymbolicAbstraction instance created')
        # super(Abstraction, self).__init__()

        self.max_hd = max_hd
        self.num_dims = num_dims

        # TODO: gets paths as z3 constraints, should take care of them bby
        # itself

        self.solver = smt.smt_solver_factory('z3')
        self.id_generator = self.gen_id_()
        self.gen_id = lambda: next(self.id_generator)

        #self.path_var_dict = {}
        #var_name_list = ['x_arr', 'state_arr', 'dummy_output_arr',
        #                 'dummy_nextstate_arr', 'input_arr']

        #var_id_list = [IV + X, IV + SI, IV + SF, RV + U, RV + SI, RV + SF, IV + I]

        var_name_2_len_dict = {IV + X: ('iv_x_arr', num_dims.x, float),
                               IV + SI: ('iv_int_state_arr', num_dims.si, int),
                               IV + SF: ('iv_float_state_arr', num_dims.sf, float),
                               RV + U: ('rv_output_arr', num_dims.u, float),
                               RV + SI: ('rv_int_state_arr', num_dims.si, int),
                               RV + SF: ('rv_float_state_arr', num_dims.sf, float),
                               IV + I: ('iv_input_arr', num_dims.ci, float)}
        #var_name_list = cifc.ControllerIfcVarNames(num_dims)

        # creates smt vars
        def create_smt_var(id_str, aux_str=''):
            var_details = var_name_2_len_dict[id_str]
            name_str = var_details[0] + aux_str
            length = var_details[1]
            # if array length is 0, do not create a z3 var
            #if length == 0:
            #    return None
            if var_details[2] is float:
                return self.solver.RealVector(name_str, length)
            elif var_details[2] is int:
                return self.solver.IntVector(name_str, length)
            else:
                raise err.Fatal('unhandled type')

        self.create_smt_var = create_smt_var

        z3_decls = {}
        # filter out vars with 0 length
        #for var_id in var_id_list:
        #z3_decls[var_id] = self.create_smt_var(var_id)
        nested_list_gen = (self.create_smt_var(k) for k in var_name_2_len_dict)
        # cull empty lists which corresponds to empty arrays
        nested_list = [i for i in nested_list_gen if i]
        l_flat = utils.flatten(nested_list) #[e for sub_list in nested_list for e in sub_list]
        z3_decls = {str(d): d for d in l_flat}
        self.path_var_dict = z3_decls

        self.path_dict = ControllerSymbolicAbstraction.get_paths(
            self.solver,
            controller_path_dir_path,
            self.path_var_dict)

    def gen_id_(self):
        for i in range(MAX_NUM_VARS_EXPECTED):
            yield i

    def get_new_plant_smt_var(self, cell_id):
        #x_str = X + str(cell_id)
        x = self.create_smt_var(IV+X, str(cell_id))
        return x

    def get_input_smt_var(self, uid_str):

        # id_str = str(self.gen_id())

        #ci_str = 'ci' + uid_str
        ci = self.create_smt_var(IV+I, uid_str)
        return ci

    # get new control states and control inputs

    def get_new_cumulitive_smt_vars(
            self,
            abs_state,
            uid_str,
            pid_str,
            ):

        # path_trace_str = 'p' + str(p_id)

        # s_str = str(abs_state.s_) + pid_str
        # u_str = str(abs_state.u) + pid_str

        #s_str = 'S' + uid_str + '_' + pid_str
        #u_str = 'U' + uid_str + '_' + pid_str

        si = self.create_smt_var(RV+SI, uid_str + '_' + pid_str)
        sf = self.create_smt_var(RV+SF, uid_str + '_' + pid_str)
        u = self.create_smt_var(RV+U, uid_str + '_' + pid_str)

        # print str(s), s.sexpr()
        # print str(u), u.sexpr()
        # print str(x), x.sexpr()

        return (si, sf, u)

    def instantiate(
          self,
          pc,
          si,
          sf,
          x,
          si_,
          sf_,
          u,
          ci,
          ):

        # print z3.simplify(pc)
        # print '0'*80
        # print self.path_var_dict['x_arr'], x

        num_dims = self.num_dims

        def substitute(pc, base_var_name_str, v, dims):
            for idx in range(dims):
                var_name_str = base_var_name_str + '__' + str(idx)
                pc = self.solver.substitute(pc, self.path_var_dict[var_name_str], v[idx])
            return pc

        #print pc
        pc = substitute(pc, 'iv_x_arr', x, num_dims.x)
        pc = substitute(pc, 'iv_int_state_arr', si, num_dims.si)
        pc = substitute(pc, 'iv_float_state_arr', sf, num_dims.sf)
        pc = substitute(pc, 'rv_int_state_arr', si_, num_dims.si)
        pc = substitute(pc, 'rv_float_state_arr', sf_, num_dims.sf)
        pc = substitute(pc, 'rv_output_arr', u, num_dims.u)
        pc = substitute(pc, 'iv_input_arr', ci, num_dims.ci)
        #print pc
        #print '='*100
        # print '0'*80
        # print pc

        return pc

    # def valid(self, abs_state):
        # return self.solver.SAT(abs_state.C)

    def meta_sampler(
          self,
          abs_state,
          num_req_samples,
          time_budget,
          ):
        raise NotImplementedError

    def timed_sampler(
          self,
          abs_state,
          num_req_samples,
          time_budget,
          ):
        raise NotImplementedError

    # optimized version of sample_smt_realVec
    # uses reals as opposed to z3 RealVec
    # This enables the usage of z3_obj.hash() which are
    # way faster than using str(z3_obj)
    def sample_smt(self, abs_state, num_req_samples):

        # print abs_state
        # get back samples for plant states and inputs

        var_list = [
            abs_state.x,
            abs_state.u,
            abs_state.si,
            abs_state.sf,
            abs_state.si_,
            abs_state.sf_,
            abs_state.ci]

        ###############################
        var2sample_list = utils.flatten([abs_state.x])  # , abs_state.u]
        #print var_list
        sample_dict, num_actual_samples = self.solver.sample_scalars(
            abs_state.C,
            num_req_samples,
            var2sample_list,
            minDist=0.05,
            )
        normalized_sample_array_list = []
        if sample_dict:
            for var_vec in var_list:
                if var_vec:
                    sample_list = [sample_dict[var.hash()] for var in var_vec]
                    normalized_sample_array = np.array(sample_list).T
                else:
                    normalized_sample_array = np.empty((num_actual_samples, 0))

                normalized_sample_array_list.append(normalized_sample_array)
            return normalized_sample_array_list + [num_actual_samples]
        else:
            return [None]*len(var_list) + [num_actual_samples]

    def sample_smt_delme(self, abs_state, num_req_samples):
        num_dims = self.num_dims

        # print abs_state
        # get back samples for plant states and inputs

        # #############################
        # NOTE: var_list and var_dim_list must have the same ordering of vars!!
        var_list = utils.flatten([
            abs_state.x,
            abs_state.u,
            abs_state.si,
            abs_state.sf,
            abs_state.si_,
            abs_state.sf_,
            abs_state.ci])

        var_dim_list = [
            num_dims.x,
            num_dims.u,
            num_dims.si,
            num_dims.sf,
            num_dims.si,
            num_dims.sf,
            num_dims.ci]
        ###############################
        var2sample_list = utils.flatten([abs_state.x])  # , abs_state.u]
        print var_list
        sample_dict, num_actual_samples = self.solver.sample_scalars(
            abs_state.C,
            num_req_samples,
            var2sample_list,
            minDist=5,
            )
        if sample_dict:

            # NOTE: list(sample_dict) won't work because ordering in var_list is
            # important
            sample_list_flat = [sample_dict.get(var.hash(), []) for var in var_list]
            # TODO: The below two transformations are not easy to udnerstand or work
            # with. Consider simplification!!
            sample_list = utils.group_list(sample_list_flat, var_dim_list)

            # replace empty list by [[]] to mantain numpy array dimensions
            normalized_sample_list =\
                [np.array(val).T if val else np.empty((num_actual_samples, 0)) for val in sample_list]

            print 'SAMPLES'

            for i in var_list:
                print i
            print '='*20
            for i in normalized_sample_list:
                print i
            exit()
            for (var, val) in zip(var_list, normalized_sample_list):
                #print '{}: {}'.format(var, val)
                # ##!!##logger.debug('{}: {}'.format(var, val))
                pass

            normalized_sample_list.append(num_actual_samples)
            print 'num_actual_samples:', num_actual_samples

            # return (x_array, u_array, s_array, s__array, ci_array, n)

            return tuple(normalized_sample_list)
        else:

            # print 'UNSAT'

            return tuple([None]*len(var_dim_list) + [0])

    # \alpha()
    # def get_abs_state_from_concrete_state(self, concrete_state, hd=0, p='XXX', cp='XXX'):

    def get_abs_state_from_concrete_state(
            self,
            concrete_state,
            hd=0,
            p='',
            cp='',
            ):

        def split_concrete_controller_state(concrete_state):
            nsi = self.num_dims.si
            #nsf = self.num_dims.sf
            si = concrete_state[0:nsi]
            sf = concrete_state[nsi:]
            return si, sf

        if hd != 0:
            raise err.Fatal('investigate')
        id_str = str(self.gen_id())
        si_str = SI + id_str
        sf_str = SF + id_str
        si__str = SI + id_str + p
        sf__str = SF + id_str + p
        x_str = X + id_str
        u_str = U + id_str
        ci_str = I + id_str
        si = self.create_smt_var(IV+SI, si_str)
        sf = self.create_smt_var(IV+SF, sf_str)
        si_ = self.create_smt_var(RV+SI, si__str)
        sf_ = self.create_smt_var(RV+SF, sf__str)
        u = self.create_smt_var(RV+U, u_str)
        x = self.create_smt_var(IV+X, x_str)
        ci = self.create_smt_var(IV+I, ci_str)
        concrete_si_, concrete_sf_ = split_concrete_controller_state(concrete_state)
        C = self.solver.And(
                self.solver.equal(si_, concrete_si_),
                self.solver.equal(sf_, concrete_sf_))
        x_ival_cons_list = []
        return ControllerSymbolicAbstractState(
            C,
            si,
            sf,
            x,
            si_,
            sf_,
            u,
            p,
            cp,
            ci,
            hd,
            x_ival_cons_list,
            )

    def get_reachable_abs_states(
            self,
            abs_state,
            A,
            system_params,
            ):
        reachable_state_list = []

        # CA = A.controller_abs

        PA = A.plant_abs
        hd = abs_state.cs.hd + 1

        uid_str = str(self.gen_id())

        x = self.get_new_plant_smt_var(str(abs_state.ps))
        ci = self.get_input_smt_var(uid_str)

        # construct ci smt constraints

        #ci_ival_cons = system_params.ci.scaleNround(self.CONVERSION_FACTOR)
        ci_ival_cons = system_params.ci
        ci_smt = self.solver.ic2smt(ci_ival_cons, ci)

        X_smt = PA.get_smt2_constraints(abs_state.ps, x)
        x_ival_cons = PA.get_ival_constraints(abs_state.ps)
        x_ival_cons_list = abs_state.cs.x_ival_cons_list + [(x, x_ival_cons)]

        for (p_id, pc) in self.path_dict.iteritems():

            # pid_str = abs_state.cs.pid + 'p' + str(p_id)

            pid_str = 'p' + str(p_id)
            cumulitive_pid_str = abs_state.cs.cpid + pid_str

            # print abs_state.cs

            si = abs_state.cs.si_  # C'[s] = C[s']
            sf = abs_state.cs.sf_  # C'[s] = C[s']
            (si_, sf_, u) = self.get_new_cumulitive_smt_vars(abs_state.cs, uid_str, pid_str)

            # print (s, s_, u, x)

            pc_ = self.instantiate(
                pc=pc,
                si=si,
                sf=sf,
                x=x,
                si_=si_,
                sf_=sf_,
                u=u,
                ci=ci,
                )

            # print 'X_smt\n', X_smt
            # print 'init', abs_state.cs.C
            # print 'pc\n', self.solver.simplify(pc)

            pc_ = self.solver.And(pc_, abs_state.cs.C, X_smt, ci_smt)
            pc_ = self.solver.simplify(pc_)

            # print 'simplified pc'
            # print pc_
            # print '='*80

            # The below logging operation is very expensive. Commenting out!
            # # ##!!##logger.debug('simplified pc:\n{}'.format(U.decorate(str(pc_))))

            reachable_controller_state = ControllerSymbolicAbstractState(
                pc_,
                si,
                sf,
                x,
                si_,
                sf_,
                u,
                pid_str,
                cumulitive_pid_str,
                ci,
                hd,
                x_ival_cons_list,
                )
            reachable_controller_state.Cx = X_smt

            # requested number of samples

            num_req_samples = A.num_samples

            # n = actual number of samples

            (
                x_array,
                u_array,
                si_array,
                sf_array,
                si__array,
                sf__array,
                ci_array,
                num_actual_samples,
            )\
                = self.get_concrete_states_from_abs_state(reachable_controller_state,
                                                          num_req_samples)
            if num_actual_samples != 0:

                # TODO: remove the below d and p arrays
                # One strategy is to separate concrete states of plant and
                # controller

                d_array = np.tile(abs_state.ps.d, (num_actual_samples, 1))
                p_array = np.tile(abs_state.ps.pvt, (num_actual_samples, 1))
                pi_array = np.zeros((num_actual_samples, A.num_dims.pi))
                t = abs_state.plant_state.n * A.delta_t
                print 't:', t
                t_array = np.tile(t, (num_actual_samples, 1))

                s_array = np.concatenate((si_array, sf_array), axis=1)
                print 's:', s_array
                #s__array = np.concatenate((si__array, sf__array))

                state = st.StateArray(
                    t=t_array,
                    x=x_array,
                    d=d_array,
                    pvt=p_array,
                    s=s_array,
                    u=u_array,
                    pi=pi_array,
                    ci=ci_array,
                    )

                # plot
                # plt.annotate('{},{}'.format(x, u), (x_array[0, 0], x_array[0, 1]))

                # if history depth exceeded, concretize all states!

                if abs_state.cs.hd >= self.max_hd:

                    # ##!!##logger.debug('max history depth reached, concretizing...')

                    # NOTE: when concretizing, need to pick only one sample
                    # Let's pick the first one
                    i = 0
                    # for i in range(num_actual_samples):

                    reachable_controller_state.C = self.solver.And(
                            self.solver.equal(si_, si__array[i, :]),
                            self.solver.equal(sf_, sf__array[i, :]))
                    reachable_controller_state.hd = 0
                    reachable_controller_state.x_ival_cons_list = [(x, x_ival_cons)]
                    reachable_state_list.append((reachable_controller_state, state))

                    # clear cpid history as well

                    reachable_controller_state.cpid = \
                        reachable_controller_state.pid
                else:
                    reachable_state_list.append((reachable_controller_state, state))

                # print reachable_controller_state

        if not reachable_state_list:
            raise err.Fatal('no reachable state found!')

        # print reachable_state_list

        return reachable_state_list

    # \gamma()
    # TODO: should check for cached concrete states
    # def get_concrete_states_from_abs_state(self, abs_state, num_req_samples):

        # ###### Pick 1!

        # (x_array, u_array, s_array, s__array, ci_array, num_actual_samples)\
        #        = self.sample_smt(abs_state, num_req_samples)

        # (x_array, u_array, s_array, s__array, ci_array, num_actual_samples)\
        #        = self.sample_random_smt(abs_state, num_req_samples)

        # return (x_array, u_array, s_array, s__array, ci_array, num_actual_samples)

    def get_concrete_states_from_abs_state(self, abs_state, num_req_samples):

        # print 'req. samples = {}'.format(num_req_samples)

        return self.sample_smt(abs_state, num_req_samples)

        # print 'found samples = {}'.format(num_actual_samples)
    # ####
    # FIXME: below unused code needs to accomodate si and sf!

        (
            x_array,
            u_array,
            s_array,
            s__array,
            ci_array,
            num_actual_samples,
            ) = self.sample_smt(abs_state, 1)

        if num_actual_samples > 0:
            (
                x_array_,
                u_array_,
                s_array_,
                s__array_,
                ci_array_,
                num_actual_samples_,
                ) = self.sample_random_smt(abs_state, num_req_samples)

            if num_actual_samples_ == 0:
                return (
                    x_array,
                    u_array,
                    s_array,
                    s__array,
                    ci_array,
                    num_actual_samples,
                    )
            else:
                return (
                    x_array_,
                    u_array_,
                    s_array_,
                    s__array_,
                    ci_array_,
                    num_actual_samples_,
                    )
        else:
            return (
                x_array,
                u_array,
                s_array,
                s__array,
                ci_array,
                num_actual_samples,
                )

    def get_ival_constraints(self, abs_state):
        raise NotImplementedError


class ControllerSymbolicAbstractState(object):

    # c_pid

    def __init__(
            self,
            C,
            si,
            sf,
            x,
            si_,
            sf_,
            u,
            pid,
            cpid,
            ci,
            hd,
            x_ival_cons_list,
            Cx=None,
            ):

        # time of creation

        self.toc = time.time()
        self.pid = pid
        self.cpid = cpid
        self.si = si
        self.sf = sf
        self.u = u
        self.si_ = si_
        self.sf_ = sf_
        self.x = x
        self.ci = ci

        # constraint on controller

        self.C = C

        # constraint o nplant state

        self.Cx = Cx

        # history depth

        self.hd = hd
        self.x_ival_cons_list = x_ival_cons_list

        # print cpid

        return

    def __eq__(self, abs_state):

        # print 'controller_eq_invoked'

        return hash(self) == hash(abs_state)

    def __hash__(self):

        # print 'controller_hash_invoked'

        # return hash(tuple(self.s))
        # print self.s
        # print '#', self.s_.sexpr()
        # return hash(self.s_.sexpr())

        # TODO: fix it! removing hash function to speed up for now.
        # Must supply a unique hash function!
        # return hash(self.pid)
        # print 'cpid:', self.cpid, self.pid

        return hash(self.cpid)

    def __repr__(self):
        return '(Si: {}, Sf: {}, Si\': {}, Sf\': {}, X: {}, U: {}, P: {}, CI: {})'.format(
            self.si,
            self.sf,
            self.si_,
            self.sf_,
            self.x,
            self.u,
            self.pid,
            self.ci,
            )
