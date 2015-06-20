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
import utils as U
import sample as S
import err

import time

logger = logging.getLogger(__name__)

MAX_NUM_VARS_EXPECTED = 100000


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

    def __init__(  # np.inf):
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
        self.gen_id = lambda : next(self.id_generator)

        # creates smt vars

        self.create_smt_var = lambda s_str: self.solver.BitVecArray(s_str)

        self.path_var_dict = {}
        var_name_list = ['x_arr', 'state_arr', 'dummy_output_arr',
                         'dummy_nextstate_arr', 'input_arr']
        for var_name in var_name_list:
            self.path_var_dict[var_name] = self.create_smt_var(var_name)

        self.path_dict = ControllerSymbolicAbstraction.get_paths(self.solver,
                controller_path_dir_path, self.path_var_dict)

    def gen_id_(self):
        for i in range(MAX_NUM_VARS_EXPECTED):
            yield i

    def get_new_plant_smt_var(self, cell_id):
        x_str = 'X' + str(cell_id)
        x = self.create_smt_var(x_str)
        return x

    def get_input_smt_var(self, uid_str):

        # id_str = str(self.gen_id())

        ci_str = 'ci' + uid_str
        ci = self.create_smt_var(ci_str)
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

        s_str = 'S' + uid_str + '_' + pid_str
        u_str = 'U' + uid_str + '_' + pid_str

        s = self.create_smt_var(s_str)
        u = self.create_smt_var(u_str)

        # print str(s), s.sexpr()
        # print str(u), u.sexpr()
        # print str(x), x.sexpr()

        return (s, u)

    def instantiate(
        self,
        pc,
        s,
        x,
        s_,
        u,
        ci,
        ):

        # print z3.simplify(pc)
        # print '0'*80
        # print self.path_var_dict['x_arr'], x

        pc = self.solver.substitute(pc, self.path_var_dict['x_arr'], x)
        pc = self.solver.substitute(pc, self.path_var_dict['state_arr'], s)
        pc = self.solver.substitute(pc,
                                    self.path_var_dict['dummy_nextstate_arr'],
                                    s_)
        pc = self.solver.substitute(pc, self.path_var_dict['dummy_output_arr'
                                    ], u)
        pc = self.solver.substitute(pc, self.path_var_dict['input_arr'], ci)

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
        num_samples_found = 0
        start_time = time.time()
        while num_samples_found < num_req_samples:
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_budget:
                return
            states = sample_random()

    def sample_random():
        raise NotImplementedError

    def sample_random_smt(self, abs_state, num_req_samples):
        MAX_ITERS = 20
        num_samples = 0
        iters = 0

        # this cumulitive sample dict will be returned

        total_sample_dict = {}
        var_list = [abs_state.x, abs_state.u, abs_state.s, abs_state.s_,
                    abs_state.ci]
        var2dim_dict = {
            str(abs_state.x): self.num_dims.x,
            str(abs_state.u): self.num_dims.u,
            str(abs_state.s): self.num_dims.s,
            str(abs_state.s_): self.num_dims.s,
            str(abs_state.ci): self.num_dims.ci,
            }
        var2sample_list = []

        # initialize the cumulitive sample dict

        for (var, dim) in var2dim_dict.iteritems():
            total_sample_dict[var] = np.empty((0, dim), dtype=int)

        while num_samples < num_req_samples and iters < MAX_ITERS:
            smt_cons_list = [abs_state.C]
            for (x, ival_cons) in abs_state.x_ival_cons_list:

                # print x, ival_cons

                val = S.sample_ival_constraints(ival_cons, 1)[0]

                # print val

                smt_cons = self.solver.equal(x, np.round(val).astype(int))
                smt_cons_list.append(smt_cons)

            # get back samples for plant states and inputs

            sample_dict = self.solver.sample_bvArray(
                smt_cons_list,
                1,
                var_list,
                var2dim_dict,
                var2sample_list,
                minDist=None,
                )

            # sample found

            if sample_dict:
                num_samples += 1
                for (var, val) in sample_dict.iteritems():
                    existing_samples = total_sample_dict[var]
                    new_sample = sample_dict[var]
                    total_sample_dict[var] = np.concatenate((existing_samples,
                            new_sample))
            iters += 1

        if num_samples == 0:
            print 'no sample found...'

        # return Nones if no sample was found

        normalized_sample_list = [None for i in range(len(var_list))]

        # if any sample was found

        if total_sample_dict:


            sample_list = [total_sample_dict[str(var)] for var in var_list]
            normalized_sample_list = [np.array(val).astype(float) for val in sample_list]
            print 'SAMPLES'

            for (var, val) in zip(var_list, normalized_sample_list):

                # ##!!##logger.debug('{}: {}'.format(var, val))

                pass
        normalized_sample_list.append(num_samples)

        # TODO: remove this
        # if num_samples != num_req_samples:
        #    print iters
        #    raise err.Fatal('FAILED')

        # print total_sample_dict
        # print normalized_sample_list

        print 'num_actual_samples:', num_samples
        return tuple(normalized_sample_list)

    def sample_smt(self, abs_state, num_req_samples):

        # print abs_state
        # get back samples for plant states and inputs

        var_list = [abs_state.x, abs_state.u, abs_state.s, abs_state.s_,
                    abs_state.ci]
        var2dim_dict = {
            str(abs_state.x): self.num_dims.x,
            str(abs_state.u): self.num_dims.u,
            str(abs_state.s): self.num_dims.s,
            str(abs_state.s_): self.num_dims.s,
            str(abs_state.ci): self.num_dims.ci,
            }

        # var2sample_list = [abs_state.x, abs_state.u, abs_state.ci, abs_state.s_]

        var2sample_list = [abs_state.x]  # , abs_state.u]
        sample_dict = self.solver.sample_bvArray(
            abs_state.C,
            num_req_samples,
            var_list,
            var2dim_dict,
            var2sample_list,
            minDist=5,
            )
        if sample_dict:

            # print z3.simplify(abs_state.C)

            sample_list = [sample_dict[str(var)] for var in var_list]
            normalized_sample_list = [np.array(val).astype(float) for val in sample_list]

            print 'SAMPLES'

            # ci_array
            # print 'S_VAL =', normalized_sample_list[2]
            # print 'S__VAL =', normalized_sample_list[3]

            for (var, val) in zip(var_list, normalized_sample_list):

                # ##!!##logger.debug('{}: {}'.format(var, val))

                pass

            x_array = normalized_sample_list[0]
            num_actual_samples = x_array.shape[0]
            normalized_sample_list.append(num_actual_samples)
            print 'num_actual_samples:', num_actual_samples

            # return (x_array, u_array, s_array, s__array, ci_array, n)

            return tuple(normalized_sample_list)
        else:

            # print 'UNSAT'

            return (
                None,
                None,
                None,
                None,
                None,
                0,
                )

    # \alpha()
    # def get_abs_state_from_concrete_state(self, concrete_state, hd=0, p='XXX', cp='XXX'):

    def get_abs_state_from_concrete_state(
        self,
        concrete_state,
        hd=0,
        p='',
        cp='',
        ):
        if hd != 0:
            raise err.Fatal('investigate')
        id_str = str(self.gen_id())
        s_str = 'S' + id_str
        s__str = 'S' + id_str + p
        x_str = 'X' + id_str
        u_str = 'U' + id_str
        ci_str = 'I' + id_str
        s = self.create_smt_var(s_str)
        s_ = self.create_smt_var(s__str)
        u = self.create_smt_var(u_str)
        x = self.create_smt_var(x_str)
        ci = self.create_smt_var(ci_str)
        C = self.solver.equal(s_, concrete_state)
        x_ival_cons_list = []
        return ControllerSymbolicAbstractState(
            C,
            s,
            x,
            s_,
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

            s = abs_state.cs.s_  # C'[s] = C[s']
            (s_, u) = self.get_new_cumulitive_smt_vars(abs_state.cs, uid_str,
                    pid_str)

            # print (s, s_, u, x)

            pc_ = self.instantiate(
                pc=pc,
                s=s,
                x=x,
                s_=s_,
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
                s,
                x,
                s_,
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
                s_array,
                s__array,
                ci_array,
                num_actual_samples,
                ) = \
                    self.get_concrete_states_from_abs_state(reachable_controller_state,
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

                    for i in range(num_actual_samples):

                        # reachable_controller_state = self.get_abs_state_from_concrete_state(s__array[i, :], hd=0, p='p' + str(p_id))#pid_str)

                        reachable_controller_state.C = self.solver.equal(s_, s__array[i, :])
                        reachable_controller_state.hd = 0
                        reachable_controller_state.x_ival_cons_list = [(x,
                                x_ival_cons)]
                        reachable_state_list.append((reachable_controller_state,
                                state))
                        reachable_controller_state.concrete_state_list.append(state[i])

                        # clear cpid history as well

                        reachable_controller_state.cpid = \
                            reachable_controller_state.pid
                else:
                    reachable_state_list.append((reachable_controller_state,
                            state))
                    reachable_controller_state.concrete_state_list.append(state)

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
        s,
        x,
        s_,
        u,
        pid,
        cpid,
        ci,
        hd,
        x_ival_cons_list,
        concrete_state_list=[],
        Cx=None,
        ):

        # time of creation

        self.toc = time.time()
        self.pid = pid
        self.cpid = cpid
        self.s = s
        self.u = u
        self.s_ = s_
        self.x = x
        self.ci = ci

        # constraint on controller

        self.C = C

        # constraint o nplant state

        self.Cx = Cx

        # history depth

        self.hd = hd
        self.concrete_state_list = concrete_state_list
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
        return '(S: {}, S\': {}, X: {}, U: {}, P: {}, CI: {})'.format(
            self.s,
            self.s_,
            self.x,
            self.u,
            self.pid,
            self.ci,
            )


