#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import numpy as np
from blessings import Terminal

# import matplotlib
# matplotlib.use('GTK3Agg')
# import matplotlib.pyplot as plt

#TAG:Z3_IND
# Comment out below import
#import smtSolver as smt

import state as st
import utils
from utils import print
import err

term = Terminal()

# import controlifc as cifc

# import time

logger = logging.getLogger(__name__)

MAX_NUM_VARS_EXPECTED = 100000

IV = 'iv'
RV = 'rv'
SI = 'SI'
SF = 'SF'
U = 'U'
X = 'X'
I = 'ci'


class SMTVar(object):
    def __init__(self, var, name_str, dim, typ):
        self.var = var
        self.dim = dim
        self.name_str = name_str
        self.typ = typ
        return


class ControllerVars(object):
    def __init__(self, var_name_2_len_dict, z3_decls):
        self.iv_i = SMTVar()
        self.iv_x = SMTVar()
        self.iv_si = SMTVar()
        self.iv_sf = SMTVar()
        self.rv_u = SMTVar()
        self.rv_si = SMTVar()
        self.rv_sf = SMTVar()


class ControllerSymbolicAbstraction:

    # @staticmethod
    # def get_abs_state(s):
    #    return ControllerSymbolicAbstractState(s)

    # creates smt vars
    def create_smt_var(self, id_str, aux_str=''):
        var_details = self.var_name_2_len_dict[id_str]
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

    def __init__(
            self,
            num_dims,
            controller_sym_path_obj, #controller_path_dir_path,
            min_smt_sample_dist,
            smt_solver, #TAG:Z3_IND - Add solver param
            max_hd=0,
            ):

        # ##!!##logger.debug('ControllerSymbolicAbstraction instance created')
        # super(Abstraction, self).__init__()

        self.min_smt_sample_dist = min_smt_sample_dist
        self.max_hd = max_hd
        self.num_dims = num_dims

        # TODO: gets paths as z3 constraints, should take care of them bby
        # itself

        # TAG:Z3_IND - get the solver from the passed in args
        #self.solver = smt.smt_solver_factory('z3')
        self.solver = smt_solver

        self.id_generator = self.gen_id_()
        self.gen_id = lambda: next(self.id_generator)

        #self.path_var_dict = {}
        #var_name_list = ['x_arr', 'state_arr', 'dummy_output_arr',
        #                 'dummy_nextstate_arr', 'input_arr']

        #var_id_list = [IV + X, IV + SI, IV + SF, RV + U, RV + SI, RV + SF, IV + I]

        self.var_name_2_len_dict = {IV + X: ('iv_x_arr', num_dims.x, float),
                                    IV + SI: ('iv_int_state_arr', num_dims.si, int),
                                    IV + SF: ('iv_float_state_arr', num_dims.sf, float),
                                    RV + U: ('rv_output_arr', num_dims.u, float),
                                    RV + SI: ('rv_int_state_arr', num_dims.si, int),
                                    RV + SF: ('rv_float_state_arr', num_dims.sf, float),
                                    IV + I: ('iv_input_arr', num_dims.ci, float)}
        #var_name_list = cifc.ControllerIfcVarNames(num_dims)

        #self.create_smt_var = create_smt_var

        z3_decls = {}
        # filter out vars with 0 length
        #for var_id in var_id_list:
        #z3_decls[var_id] = self.create_smt_var(var_id)
        nested_list_gen = (self.create_smt_var(k) for k in self.var_name_2_len_dict)
        # cull empty lists which corresponds to empty arrays
        nested_list = [i for i in nested_list_gen if i]
        l_flat = utils.flatten(nested_list) #[e for sub_list in nested_list for e in sub_list]
        z3_decls = {str(d): d for d in l_flat}
        self.path_var_dict = z3_decls

        #self.path_dict = ControllerSymbolicAbstraction.get_paths(
        #    self.solver,
        #    controller_path_dir_path,
        #    self.path_var_dict)

        #self.init_path_obj('list', controller_path_dir_path)
        #self.init_path_obj('list', paths)
        self.controller_sym_path_obj = controller_sym_path_obj
        #self.base_smt_vars = z3_decls

        #self.get_reachable_abs_states = self.get_reachable_abs_states_discards_model
        self.get_reachable_abs_states = self.get_reachable_abs_states_reuses_model
        self.is_symbolic = True
        self.id_ctr = 0

    def gen_id_(self):
        self.id_ctr += 1
        while True:
            yield self.id_ctr

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

        # print(str(s), s.sexpr())
        # print(str(u), u.sexpr())
        # print(str(x), x.sexpr())

        return (si, sf, u)

    def substitute_curr_vars(self, cs):
        cons = cs.C
        num_dims = self.num_dims

        def substitute(cons, v, base_var_name_str, dims):
            for idx in range(dims):
                var_name_str = base_var_name_str + '__' + str(idx)
                #print('replacing', v[idx], '->', self.path_var_dict[var_name_str])
                cons = self.solver.substitute(cons, v[idx], self.path_var_dict[var_name_str])
            return cons

        #print(pc)
        # current state gets modified to standard vars
        cons = substitute(cons, cs.x, 'iv_x_arr', num_dims.x)
        cons = substitute(cons, cs.si, 'iv_int_state_arr', num_dims.si)
        cons = substitute(cons, cs.sf, 'iv_float_state_arr', num_dims.sf)
        cons = substitute(cons, cs.si_, 'rv_int_state_arr', num_dims.si)
        cons = substitute(cons, cs.sf_, 'rv_float_state_arr', num_dims.sf)
        cons = substitute(cons, cs.u, 'rv_output_arr', num_dims.u)
        cons = substitute(cons, cs.ci, 'iv_input_arr', num_dims.ci)
        return cons

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

        # print(z3.simplify(pc))
        # print('0'*80)
        # print(self.path_var_dict['x_arr'], x)

        num_dims = self.num_dims

        def substitute(pc, base_var_name_str, v, dims):
            for idx in range(dims):
                var_name_str = base_var_name_str + '__' + str(idx)
                #print('replacing', self.path_var_dict[var_name_str], '->', v[idx])
                pc = self.solver.substitute(pc, self.path_var_dict[var_name_str], v[idx])
                #print('[]'*10)
                #print(pc)
            return pc

        #print(pc)
        pc = substitute(pc, 'iv_x_arr', x, num_dims.x)
        pc = substitute(pc, 'iv_int_state_arr', si, num_dims.si)
        pc = substitute(pc, 'iv_float_state_arr', sf, num_dims.sf)
        pc = substitute(pc, 'rv_int_state_arr', si_, num_dims.si)
        pc = substitute(pc, 'rv_float_state_arr', sf_, num_dims.sf)
        pc = substitute(pc, 'rv_output_arr', u, num_dims.u)
        pc = substitute(pc, 'iv_input_arr', ci, num_dims.ci)
        #print(pc)
        #print('='*100)
        # print('0'*80)
        # print(pc)

        return pc

    # same as sample_smt_cons but uses solver
    def sample_smt_solver(self, abs_state, num_req_samples, solver):
        minDist = self.min_smt_sample_dist

        # print(abs_state)
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
        #print(var_list)
        #print('='*20, 'sampling', '='*20)
        #print(abs_state.C)

        sample_dict, num_actual_samples = self.solver.sample_scalars(
            solver,
            num_req_samples,
            var2sample_list,
            minDist,
            )
        #for k in sample_dict:
        #    print(k, ':', sample_dict[k])
        #print('='*20)
        #for var_vec in var_list:
        #    for var in var_vec:
        #        print(var, ':', var.hash())
        normalized_sample_array_list = []
        if sample_dict:
            for var_vec in var_list:
                if var_vec:
                    #print(var_vec)
                    sample_list = [sample_dict[var.hash()] for var in var_vec]
                    normalized_sample_array = np.array(sample_list).T
                else:
                    normalized_sample_array = np.empty((num_actual_samples, 0))

                normalized_sample_array_list.append(normalized_sample_array)
            return normalized_sample_array_list + [num_actual_samples]
        else:
            #print('UNSAT')
            return [None]*len(var_list) + [num_actual_samples]

    # optimized version of sample_smt_realVec
    # uses reals as opposed to z3 RealVec
    # This enables the usage of z3_obj.hash() which are
    # way faster than using str(z3_obj)
    #
    # Uses cons to sample
    def sample_smt_cons(self, abs_state, num_req_samples):
        #minDist=0.5
        #minDist = 0.05
        minDist = self.min_smt_sample_dist

        # print(abs_state)
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
        #print(var_list)
        #print('='*20, 'sampling', '='*20)
        #print(abs_state.C)

        # if solver is not passed
        solver = self.solver.solver()
        solver.add(abs_state.C)
        sample_dict, num_actual_samples = self.solver.sample_scalars(
            solver,
            num_req_samples,
            var2sample_list,
            minDist,
            )
        #for k in sample_dict:
        #    print(k, ':', sample_dict[k])
        #print('='*20)
        #for var_vec in var_list:
        #    for var in var_vec:
        #        print(var, ':', var.hash())
        normalized_sample_array_list = []
        if sample_dict:
            for var_vec in var_list:
                if var_vec:
                    #print(var_vec)
                    sample_list = [sample_dict[var.hash()] for var in var_vec]
                    normalized_sample_array = np.array(sample_list).T
                else:
                    normalized_sample_array = np.empty((num_actual_samples, 0))

                normalized_sample_array_list.append(normalized_sample_array)
            return normalized_sample_array_list + [num_actual_samples]
        else:
            #print('UNSAT')
            return [None]*len(var_list) + [num_actual_samples]

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

        #concrete_si_, concrete_sf_ = split_concrete_controller_state(concrete_state)
        #C = self.solver.And(
        #        self.solver.equal(si_, concrete_si_),
        #        self.solver.equal(sf_, concrete_sf_))

        concrete_si, concrete_sf = split_concrete_controller_state(concrete_state)
        C = self.solver.And(
                self.solver.equal(si, concrete_si),
                self.solver.equal(sf, concrete_sf))
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
            )

    # discards model!
    def get_reachable_abs_states_discards_model(
            self,
            abs_state,
            A,
            system_params
            ):
        reachable_state_list = []

        # CA = A.controller_abs

        PA = A.plant_abs
        hd = abs_state.cs.hd + 1

        #x = self.get_new_plant_smt_var(str(abs_state.ps))
        #ci = self.get_input_smt_var(uid_str)

        # construct ci smt constraints
        #ci = self.controller_sym_path_obj.ci
        # TODO: sort this mess out...should not know its a list!
        # Need to be made a class or something
        ci = [self.path_var_dict['iv_input_arr__'+str(i)] for i in range(self.num_dims.ci)]
        ci_ival_cons = system_params.ci
        ci_smt = self.solver.ic2smt(ci_ival_cons, ci)
        # print(ci_smt)

        #x = self.controller_sym_path_obj.x
        x = [self.path_var_dict['iv_x_arr__'+str(i)] for i in range(self.num_dims.x)]
        X_smt = PA.get_smt2_constraints(abs_state.ps, x)
        # print(X_smt)

        # # substitute the current vars with original program vars

        #print(abs_state.cs.C)
        C_subs = self.substitute_curr_vars(abs_state.cs)
        # print(abs_state.cs.C)

        self.controller_sym_path_obj.set_global_cons(C_subs, ci_smt, X_smt)
        ##self.controller_sym_path_obj.unset_global_cons()

        uid_str = str(self.gen_id())
        num_req_samples = A.num_samples
        for p_id, pc_solver in self.controller_sym_path_obj.sat_path_gen():

            # TODO: makes life simpler for now...easier to convert solver to
            # constraints and use the existing functions instead of using the
            # solver directly.
            # This must be fixed and the solver should be directly handled to
            # get any performance benefits!

            pc_ = self.solver.And(*pc_solver.assertions())

            pid_str = 'p' + str(p_id)
            cumulitive_pid_str = abs_state.cs.cpid + pid_str

            x = self.get_new_plant_smt_var(str(abs_state.ps))
            ci = self.get_input_smt_var(uid_str)

            # print(abs_state.cs)
            si = abs_state.cs.si_  # C'[s] = C[s']
            sf = abs_state.cs.sf_  # C'[s] = C[s']
            (si_, sf_, u) = self.get_new_cumulitive_smt_vars(abs_state.cs, uid_str, pid_str)

            #print('='*10, 'pc', '='*10)
            #print(pc_)
            #print('0'*20)
            pc_ = self.instantiate(pc_, si, sf, x, si_, sf_, u, ci)
            #print(pc_)
            #exit()

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
                )

            # n = actual number of samples

            #(
            #    x_array,
            #    u_array,
            #    si_array,
            #    sf_array,
            #    si__array,
            #    sf__array,
            #    ci_array,
            #    num_actual_samples,
            #)\
            #    = self.get_concrete_states_from_abs_state(reachable_controller_state, num_req_samples)

            (
                x_array,
                u_array,
                si_array,
                sf_array,
                si__array,
                sf__array,
                ci_array,
                num_actual_samples,
            ) = self.sample_smt_cons(reachable_controller_state, num_req_samples)

            # TODO: remove the below d and p arrays
            # One strategy is to separate concrete states of plant and
            # controller

            d_array = np.tile(abs_state.ps.d, (num_actual_samples, 1))
            p_array = np.tile(abs_state.ps.pvt, (num_actual_samples, 1))
            pi_array = np.zeros((num_actual_samples, A.num_dims.pi))
            t = abs_state.plant_state.n * A.delta_t
            print('t:', t)
            t_array = np.tile(t, (num_actual_samples, 1))

            s_array = np.concatenate((si_array, sf_array), axis=1)
            print('s:', s_array)
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

            # if history depth exceeded, concretize all states!

            if abs_state.cs.hd >= self.max_hd:

                # NOTE: when concretizing, need to pick only one sample
                # Let's pick the first one
                i = 0
                # for i in range(num_actual_samples):

                #reachable_controller_state.C = self.solver.And(
                #        self.solver.equal(si_, si__array[i, :]),
                #        self.solver.equal(sf_, sf__array[i, :]))
                reachable_controller_state.C = self.solver.And(
                        self.solver.equal(si, si__array[i, :]),
                        self.solver.equal(sf, sf__array[i, :]))
                reachable_controller_state.hd = 0
                reachable_state_list.append((reachable_controller_state, state))

                # clear cpid history as well

                reachable_controller_state.cpid = \
                    reachable_controller_state.pid
            else:
                reachable_state_list.append((reachable_controller_state, state))

                # print(reachable_controller_state)

        if not reachable_state_list:
            raise err.Fatal('no reachable state found!')

        return reachable_state_list

    # reuses model
    def get_reachable_abs_states_reuses_model(
            self,
            abs_state,
            A,
            system_params
            ):
        reachable_state_list = []

        # CA = A.controller_abs

        PA = A.plant_abs
        hd = abs_state.cs.hd + 1

        #x = self.get_new_plant_smt_var(str(abs_state.ps))
        #ci = self.get_input_smt_var(uid_str)

        # construct ci smt constraints
        #ci = self.controller_sym_path_obj.ci
        # TODO: sort this mess out...should not know its a list!
        # Need to be made a class or something
        ci = [self.path_var_dict['iv_input_arr__'+str(i)] for i in range(self.num_dims.ci)]
        ci_ival_cons = system_params.ci
        ci_smt = self.solver.ic2smt(ci_ival_cons, ci)
        # print(ci_smt)

        #x = self.controller_sym_path_obj.x
        x = [self.path_var_dict['iv_x_arr__'+str(i)] for i in range(self.num_dims.x)]
        X_smt = PA.get_smt2_constraints(abs_state.ps, x)
        # print(X_smt)

        # # substitute the current vars with original program vars

        #print(abs_state.cs.C)
        C_subs = self.substitute_curr_vars(abs_state.cs)
        #print(abs_state.cs.C)
        #exit()
        # print(abs_state.cs.C)

        self.controller_sym_path_obj.set_global_cons(C_subs, ci_smt, X_smt)
        ##self.controller_sym_path_obj.unset_global_cons()

        num_req_samples = A.num_samples

        #print(C_subs)
        #print(ci_smt)
        #print(X_smt)

        uid_str = str(self.gen_id())
        for p_id, pc_solver in self.controller_sym_path_obj.sat_path_gen():

            # TODO: makes life simpler for now...easier to convert solver to
            # constraints and use the existing functions instead of using the
            # solver directly.
            # This must be fixed and the solver should be directly handled to
            # get any performance benefits!
            #
            pid_str = 'p' + str(p_id)
            cumulitive_pid_str = abs_state.cs.cpid + pid_str

            reachable_controller_state = ControllerSymbolicAbstractState(
                C=C_subs,
                si=[self.path_var_dict['iv_int_state_arr__'+str(i)] for i in range(self.num_dims.si)],
                sf=[self.path_var_dict['iv_float_state_arr__'+str(i)] for i in range(self.num_dims.sf)],
                x=[self.path_var_dict['iv_x_arr__'+str(i)] for i in range(self.num_dims.x)],
                si_=[self.path_var_dict['rv_int_state_arr__'+str(i)] for i in range(self.num_dims.si)],
                sf_=[self.path_var_dict['rv_float_state_arr__'+str(i)] for i in range(self.num_dims.sf)],
                u=[self.path_var_dict['rv_output_arr__'+str(i)] for i in range(self.num_dims.u)],
                pid=pid_str,
                cpid=cumulitive_pid_str,
                ci=[self.path_var_dict['iv_input_arr__'+str(i)] for i in range(self.num_dims.ci)],
                hd=hd,
                )

            #   #x=[self.path_var_dict['iv_x_arr__'+str(i)] for i in range(self.num_dims.x)],
            #    #ci=[self.path_var_dict['iv_input_arr__'+str(i)] for i in range(self.num_dims.ci)],
            # protect the solver from the changes the sampler() might make.
            #pc_solver.push()
            (
                x_array,
                u_array,
                si_array,
                sf_array,
                si__array,
                sf__array,
                ci_array,
                num_actual_samples,
            ) = self.sample_smt_solver(reachable_controller_state, num_req_samples, pc_solver)

            #print('solver', pc_solver)
            #print(x_array)

            #pc_solver.pop()

            pc_ = self.solver.And(*pc_solver.assertions())

            x = self.get_new_plant_smt_var(str(abs_state.ps))
            ci = self.get_input_smt_var(uid_str)
            # print(abs_state.cs)
            si = abs_state.cs.si_  # C'[s] = C[s']
            sf = abs_state.cs.sf_  # C'[s] = C[s']
            (si_, sf_, u) = self.get_new_cumulitive_smt_vars(abs_state.cs, uid_str, pid_str)

            pc_ = self.instantiate(pc_, si, sf, x, si_, sf_, u, ci)

            reachable_controller_state.C = pc_
            reachable_controller_state.si = si
            reachable_controller_state.sf = sf
            reachable_controller_state.x = x
            reachable_controller_state.si_ = si_
            reachable_controller_state.sf_ = sf_
            reachable_controller_state.u = u
            reachable_controller_state.ci = ci

            # n = actual number of samples

            #(
            #    x_array,
            #    u_array,
            #    si_array,
            #    sf_array,
            #    si__array,
            #    sf__array,
            #    ci_array,
            #    num_actual_samples,
            #)\
            #    = self.get_concrete_states_from_abs_state(reachable_controller_state, num_req_samples)

            # TODO: remove the below d and p arrays
            # One strategy is to separate concrete states of plant and
            # controller

            d_array = np.tile(abs_state.ps.d, (num_actual_samples, 1))
            p_array = np.tile(abs_state.ps.pvt, (num_actual_samples, 1))
            pi_array = np.zeros((num_actual_samples, A.num_dims.pi))
            t = abs_state.plant_state.n * A.delta_t
            ######################################
            #TODO: wrap this up somehow
            #print()
            #print(term.move_up + term.move_up)
            ######################################
            #with term.location():
            #    print('t:', t)
            print('t:', t)
            t_array = np.tile(t, (num_actual_samples, 1))

            s_array = np.concatenate((si_array, sf_array), axis=1)
            #print('s:', s_array)
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

            # if history depth exceeded, concretize all states!

            if abs_state.cs.hd >= self.max_hd:

                # NOTE: when concretizing, need to pick only one sample
                # Let's pick the first one
                i = 0
                # for i in range(num_actual_samples):

                #reachable_controller_state.C = self.solver.And(
                #        self.solver.equal(si_, si__array[i, :]),
                #        self.solver.equal(sf_, sf__array[i, :]))
                reachable_controller_state.C = self.solver.And(
                        self.solver.equal(si, si__array[i, :]),
                        self.solver.equal(sf, sf__array[i, :]))
                reachable_controller_state.hd = 0
                reachable_state_list.append((reachable_controller_state, state))

                # clear cpid history as well

                reachable_controller_state.cpid = \
                    reachable_controller_state.pid
            else:
                reachable_state_list.append((reachable_controller_state, state))

                # print(reachable_controller_state)

        if not reachable_state_list:
            raise err.Fatal('no reachable state found!')

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

        # print('req. samples = {}'.format(num_req_samples))
        return self.sample_smt(abs_state, num_req_samples)
        # print('found samples = {}'.format(num_actual_samples))


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
            ):

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

        # history depth

        self.hd = hd
        # whats the purpose of this list? long forgotten?

        # print(cpid)

        return

    def __eq__(self, abs_state):

        # print('controller_eq_invoked')

        return hash(self) == hash(abs_state)

    def __hash__(self):

        # print('controller_hash_invoked')

        # return hash(tuple(self.s))
        # print(self.s)
        # print('#', self.s_.sexpr())
        # return hash(self.s_.sexpr())

        # TODO: fix it! removing hash function to speed up for now.
        # Must supply a unique hash function!
        # return hash(self.pid)
        # print('cpid:', self.cpid, self.pid)

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
