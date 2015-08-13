#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import numpy as np

# TODO: This is not clearly understood, and is deprecated!!

import imp

import utils
import err
import fileOps as fp
import state as st

# only for testing
# import importlib
# A = importlib.import_module('abstraction')
# S = importlib.import_module('sample')

import sample as S
import random

np.set_printoptions(threshold=10000)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

COMMA = ','
SQ = '\''


def simulator_factory(
        config_dict,
        benchmark_os_path,
        plt,
        plant_pvt_init_data,
        parallel=False,
        test_params=None,
        ):

    # ##!!##logger.debug('requested simulator creation')

    if config_dict['type'] == 'string':
        try:
            sim_type = config_dict['plant_description']
            if sim_type == 'matlab':
                logger.info('creating matlab simulator')

                # get the m_file's path

                m_file_path = config_dict['plant_path']
                abs_m_file_path = fp.construct_path(m_file_path, benchmark_os_path)
                if fp.validate_file_names([abs_m_file_path]):

                    # return MatlabSim(m_file_path, benchmark_os_path, parallel)

                    return MEngPy(m_file_path, benchmark_os_path, parallel)
                else:
                    raise err.FileNotFound('file does not exist: ' + m_file_path)
            elif sim_type == 'simulink':
                return SimulinkSim()
            elif sim_type == 'python':
                logger.info('creating Native Python simulator')

                # get the file path

                python_file_path = config_dict['plant_path']
                #(module_name, file_ext) = python_file_path.split('.')
                (module_name, file_ext) = fp.split_filename_ext(python_file_path)
                if file_ext != 'py':
                    raise err.Fatal('Python file extension py expected, found: {}'.format(file_ext))
                module_path = fp.construct_path(python_file_path, benchmark_os_path)
                if fp.validate_file_names([module_path]):
                    return NativeSim(module_name, module_path, plt, plant_pvt_init_data, parallel)
                else:
                    raise err.FileNotFound('file does not exist: ' + python_file_path)
            elif sim_type == 'test':
                return TestSim(test_params)
            else:
                raise err.Fatal('unknown sim type : {}'.format(sim_type))

            # Make the accessed data as None, so presence of spurious data can be detected in a
            # sanity check

            config_dict['sim_type'] = None
            config_dict['plant_path'] = None
        except KeyError, key:
            raise err.Fatal('expected abstraction parameter undefined: {}'.format(key))
    else:
        raise err.Fatal('unhandled non string type config_dict!')

        # for attr in config_dict:
        #    setattr(self, attr, config_dict[attr])


class Simulator(object):

    def __init__(self):
        self.parallel = False

        # TODO: most of the below is unhandled
        # stateDict not used yet
        # store information about each state,
        #       id |-> (type=bool/cont,scatterOrNot)

        self.stateDict = {}

        # inputs and params are unhandled...

        self.inputs = None
        self.params = None

        # currently plot in matlab itself

        self.plot = None

    # Assumptions
    # For Each state a valid state is provided:
    # else [inf, inf, inf, ... inf] is returned

    def simulate(
            self,
            sim_states,
            T,
            property_checker=None,
            property_violated_flag=None,
            ):
        raise NotImplementedError

    def simulate_entire_trajectories(self, sim_states, T):
        raise NotImplementedError

    def simulate_entire_trajectories_cont(self, sim_states, T):
        raise NotImplementedError


def matlab_communicator_factory(communicator_type):
    if communicator_type == 'pymatlab':
        logger.info('requested pymatlab communicator object')
        return PyMatlab()
    elif communicator_type == 'matlab_engine':
        logger.info('requested matlab engine communicator object')
        return MatlabEngine()
    else:
        raise err.Fatal('Internal Error')


class MatlabCommunicator(object):

    def __init__(self):
        pass

    def call_function(
            self,
            ret_val_list,
            fun_name,
            arg_list,
            ):
        raise NotImplementedError

    def call_function_retVal(
            self,
            ret_val_list,
            fun_name,
            arg_list,
            ):
        raise NotImplementedError

    def put_value(self, var_name, var_val):
        raise NotImplementedError

    def get_value(self, var_name):
        raise NotImplementedError

    def exec_command(self, cmd_str):
        raise NotImplementedError


class PyMatlab(MatlabCommunicator):

    # TODO: currently accepts only a single arguement!

    @staticmethod
    def get_matlab_command_str(command, arg):
        single_quotes = '\''
        if command == 'addpath':
            s = 'addpath({0}{1}{0})'.format(single_quotes, arg)
        elif command == '':
            s = ''
        else:
            raise err.Fatal('Internal error!')
        return s

    @staticmethod
    def get_fun_call_str(ret_val_str, fun_name, arg_str):
        if ret_val_str:
            return '[{}] = {}({});'.format(ret_val_str, fun_name, arg_str)
        else:
            return '{}({});'.format(fun_name, arg_str)

    def __init__(self):
        logger.info('instantiating matlab')
        import pymatlab

# self.session = pymatlab.session_factory('-nodisplay -nosplash')
# self.session = pymatlab.session_factory('-nosplash -nodesktop -nodisplay')

        self.session = pymatlab.session_factory()

    def call_function(
            self,
            ret_val_list,
            fun_name,
            arg_list,
            ):
        arg_str = COMMA.join(arg_list)
        ret_val_str = COMMA.join(ret_val_list)
        fun_call_str = self.get_fun_call_str(ret_val_str, fun_name, arg_str)

        # ##!!##logger.debug('created fun call: ' + fun_call_str)

        self.exec_command(fun_call_str)

    def call_function_retVal(
            self,
            ret_val_list,
            fun_name,
            arg_list,
            ):
        arg_composed_str = COMMA.join(arg_list)
        ret_val_composed_str = COMMA.join(ret_val_list)
        fun_call_str = self.get_fun_call_str(ret_val_composed_str, fun_name, arg_composed_str)

        # ##!!##logger.debug('created fun call with retVal: ' + fun_call_str)

        self.exec_command(fun_call_str)
        return [self.get_value(ret_val_str) for ret_val_str in ret_val_list]

    def put_value(self, var_name, var_val):

        # ##!!##logger.debug('setting {} to {}'.format(var_name, var_val))

        self.session.putvalue(var_name, var_val)

        # cross check!
        # ##!!##logger.debug('crosschecking by reading set value')

        self.get_value(var_name)

    def get_value(self, var_name):

        # ##!!##logger.debug('getting ' + var_name)

        var_val = self.session.getvalue(var_name)

        # ##!!##logger.debug('read value: ' + str(var_val))

        return var_val

    def exec_command(self, cmd_str):

        # ##!!##logger.debug('executing command: ' + cmd_str)

        self.session.run(cmd_str)


class MatlabEngine(MatlabCommunicator):

    def __init__(self):
        raise NotImplementedError


class MatlabSim(Simulator):

    @staticmethod
    def matlab2py_indices(idx):

        # idx can be singleton or a numpy array

        return idx - 1

    @staticmethod
    def py2matlab_indices(idx):

        # idx can be singleton or a numpy array

        return idx + 1

    def __init__(
            self,
            m_file_path,
            benchmark_os_path,
            parallel,
            ):
        super(MatlabSim, self).__init__()

        self.parallel = parallel

        # parse file name

        self.m_file = m_file_path
        m_file_name_split = self.m_file.split('.')
        if m_file_name_split[1].strip() != 'm':
            raise err.Fatal('internal error!')
        self.m_fun = m_file_name_split[0].strip()

        # instantiate matlab

        self.communicator = matlab_communicator_factory('pymatlab')
        comm = self.communicator
        logger.info('created matlab simulator from file: %s', self.m_file)

        # add paths

        comm.call_function([], 'addpath', [SQ + benchmark_os_path + SQ])

        # for matlab, matlabpool needs to be invoked if parallelism is
        # requested

        if self.parallel:
            comm.exec_command('matlabpool')
            [pool_size, ] = comm.call_function_retVal(['pool_size'], 'matlabpool', ['{0}size{0}'.format(SQ)])
            logger.info('simulator is parallel with #threads: %s',
                        str(pool_size))
        else:
            logger.info('simulator is instantiated as single threaded')

        # load simulator functions into workspace

        comm.put_value('SIM_Str', self.m_fun)
        comm.exec_command('sim_function = str2func(SIM_Str)')
        comm.exec_command('simulate_system = simulate_m_file(1)')
        comm.exec_command('simulate_system_par = simulate_m_file(2)')
        comm.exec_command('simulate_entire_trajectories = simulate_m_file(3)')
        comm.exec_command('simulate_entire_trajectories_cont = simulate_m_file(4)'
                          )
        logger.info('loaded functions from simulate_m_file.m')

    def simulate(
            self,
            sim_states,
            T,
            property_checker=None,
            property_violated_flag=None,
            ):

        # print sim_states.cont_states
        # print sim_states.discrete_states
        # print sim_states.pvt_states

        T_array = np.array([T])
        comm = self.communicator
        comm.put_value('t', sim_states.t)
        comm.put_value('initial_continuous_states', sim_states.cont_states)
        comm.put_value('initial_discrete_states', sim_states.discrete_states)
        comm.put_value('initial_pvt_states', sim_states.pvt_states)
        comm.put_value('control_inputs', sim_states.controller_outputs)
        comm.put_value('T', T_array)
        if property_checker is None:
            comm.put_value('property_check', np.array([0]))
        else:
            comm.put_value('property_check', np.array([1]))

        # TODO: dummy control input!

        comm.put_value('inputs', np.zeros(sim_states.cont_states.shape))

#        # TODO: dummy exogenous input!
#        comm.put_value('inputs', np.zeros(sim_states.cont_states.shape))

        ret_val_str_list = ['ret_t', 'ret_X', 'ret_D', 'ret_P', 'pvf']
        arg_str_list = [
            'sim_function',
            't',
            'T',
            'initial_continuous_states',
            'initial_discrete_states',
            'initial_pvt_states',
            'control_inputs',
            'inputs',
            'property_check',
            ]

        if self.parallel:
            print 'unhandled..modify signature to include time first'
            exit()
            fun_name_str = 'simulate_system_par'
            [X_, D_, P_] = comm.call_function_retVal(ret_val_str_list, fun_name_str, arg_str_list)
        else:
            fun_name_str = 'simulate_system'
            [T_, X_, D_, P_, pvf] = comm.call_function_retVal(ret_val_str_list, fun_name_str, arg_str_list)

        # print 'output'
        # print X_
        # print D_
        # print P_
        # print '='*20
        # t_array = np.tile(T, (sim_states.n))
        # property_violated_flag = property_checker

        if property_checker is not None:
            property_violated_flag[0] = bool(pvf)

            # print pvf, property_violated_flag[0]
        # return st.StateArray(t_array, X_, D_, P_)
        # TODO: fix this weird matlab-numpy interfacing

        t_array = np.array(T_, ndmin=2).T
        x = np.array(X_, ndmin=2)
        if D_.ndim <= 1:
            d = np.array(D_, ndmin=2).T
        else:
            d = D_
        if P_.ndim <= 1:
            pvt = np.array(P_, ndmin=2).T
        else:
            pvt = P_
        return st.StateArray(
            t=t_array,
            x=x,
            d=d,
            pvt=pvt,
            s=sim_states.controller_states,
            u=sim_states.controller_outputs,
            pi=sim_states.plant_extraneous_inputs,
            ci=sim_states.controller_extraneous_inputs,
            )

    # TODO
    # WARN: UNTESTED

    def simulate_entire_trajectories(self, sim_states, T):
        comm = self.communicator
        comm.put_value('initial_continuous_states', sim_states.cont_states)
        comm.put_value('initial_discrete_states', sim_states.discrete_states)
        comm.put_value('initial_pvt_states', sim_states.pvt_states)
        comm.put_value('T', np.array([T]))

        ret_val_str_list = ['data_mat', 'idx_arr']
        arg_str_list = [
            'sim_function',
            'initial_continuous_states',
            'initial_discrete_states',
            'initial_pvt_states',
            'inputs',
            'T',
            ]
        fun_name_str = 'simulate_entire_trajectories'
        if self.parallel:
            [data_arr, idx_arr] = comm.call_function_retVal(ret_val_str_list, fun_name_str, arg_str_list)
        else:

            logger.warning('non-parallel simulate_entire_trajectories isunimplemented'
                           )
            raise NotImplementedError('single threaded implementation missing')
        idx_arr = self.matlab2py_indices(idx_arr)
        list_of_trajs = []

        # quick sanity check

        if len(idx_arr.shape) != 1 or idx_arr[0] != 0:
            print 'idx_arr: ', idx_arr
            raise err.Fatal('sanity check on idx_arr fails!')

        # get a pairwise iterator for the index array

        for (i, j) in utils.pairwise(idx_arr):
            list_of_trajs.append(data_arr[i:j, :])

        # append the last trajectory

        logger.info('Populating trajectories...')
        list_of_trajs.append(data_arr[j:, :])

        # ##!!##logger.debug('===Trajectories===\n%s', str(list_of_trajs))

        return list_of_trajs

    def simulate_entire_trajectories_cont(self, sim_states, T):
        comm = self.communicator
        comm.put_value('initial_continuous_states', sim_states.cont_states)
        comm.put_value('initial_discrete_states', sim_states.discrete_states)
        comm.put_value('initial_pvt_states', sim_states.pvt_states)
        comm.put_value('T', np.array([T]))

        ret_val_str_list = ['data_mat', 'idx_arr']
        arg_str_list = ['sim_function', 'initial_continuous_states', 'T']
        fun_name_str = 'simulate_entire_trajectories_cont'
        [data_arr, idx_arr] = comm.call_function_retVal(ret_val_str_list, fun_name_str, arg_str_list)

        # ##!!##logger.debug('converting indices')

        idx_arr = self.matlab2py_indices(idx_arr)
        list_of_trajs = []

        # quick sanity check

        if len(idx_arr.shape) != 1 or idx_arr[0] != 0:
            print 'idx_arr: ', idx_arr
            raise err.Fatal('sanity check on idx_arr fails!')

        # get a pairwise iterator for the index array

        for (i, j) in utils.pairwise(idx_arr):
            list_of_trajs.append(data_arr[i:j, :])

        # append the last trajectory

        logger.info('Populating trajectories...')
        list_of_trajs.append(data_arr[j:, :])

        # ##!!##logger.debug('===Trajectories===\n' + str(list_of_trajs))

        return list_of_trajs


# imp.load_source(name, pathname[, file])
# Load and initialize a module implemented as a Python source file and return
# its module object. If the module was already initialized, it will be
# initialized again. The name argument is used to create or access a module
# object. The pathname argument points to the source file. The file argument is
# the source file, open for reading as text, from the beginning. It must
# currently be a real file object, not a user-defined class emulating a file.
# Note that if a properly matching byte-compiled file (with suffix .pyc or
# .pyo) exists, it will be used instead of parsing the given source file.

class NativeSim(Simulator):

    def __init__(
            self,
            module_name,
            module_path,
            plt,
            plant_pvt_init_data,
            parallel,
            ):
        super(NativeSim, self).__init__()

        sim_module = imp.load_source(module_name, module_path)
        self.sim_obj = sim_module.SIM(plt, plant_pvt_init_data)
        self.sim = self.sim_obj.sim

    def simulate(
            self,
            sim_states,
            T,
            property_checker=None,
            property_violated_flag=None,
            ):
        t_array = np.empty((sim_states.n, 1))

        num_dim = sim_states.cont_states.shape[1]
        X_array = np.empty((sim_states.n, num_dim))

        num_dim = sim_states.discrete_states.shape[1]
        D_array = np.empty((sim_states.n, num_dim))

        num_dim = sim_states.pvt_states.shape[1]
        P_array = np.empty((sim_states.n, num_dim))

        i = 0

        for state in sim_states.iterable():
            dummy_val = 0.0
            (t, X, D, pvt) = self.sim(
                (state.t, state.t + T),
                state.x,
                state.d,
                state.pvt,
                state.u,
                dummy_val,
                property_checker,
                property_violated_flag,
                )
            t_array[i, :] = t
            X_array[i, :] = X
            D_array[i, :] = D
            P_array[i, :] = pvt
            i += 1

        return st.StateArray(
            t=t_array,
            x=X_array,
            d=D_array,
            pvt=P_array,
            s=sim_states.controller_states,
            u=sim_states.controller_outputs,
            pi=sim_states.plant_extraneous_inputs,
            ci=sim_states.controller_extraneous_inputs,
            )

    def check_property(self, trace):
        pass

    def simulate_entire_trajectories(self, sim_states, T):
        raise NotImplementedError


class SimulinkSim(Simulator):

    pass


class TestSim(Simulator):

    def __init__(self, graph):
        super(TestSim, self).__init__()
        self.G = graph
        self.Abs = None

#    def recurse_graph(node):
#        for n in self.G[node]:
#            recurse_graph(n)

    def set_abstraction(self, abstraction):
        self.A = abstraction

        # Add the initial and final abstract states into the graph
        # randomly create edges

        if self.G.Type == 'test_csg1':
            for init_abs_state in abstraction.initial_state_set:

                # add initial states as nodes, do not create edges!

                if init_abs_state not in self.G:
                    self.G.add_node(init_abs_state)
            for final_abs_state in abstraction.final_state_set:

                # add final states as nodes, do not create edges!

                if final_abs_state not in self.G:
                    self.G.add_node(final_abs_state)
        elif self.G.Type == 'test_random':

                # Connect only one initial state
            #            for init_abs_state in abstraction.initial_state_set:
            #                # add initial states as nodes, do not create edges!
            #                if init_abs_state not in self.G:
            #                    self.G.add_node(init_abs_state)
            #            for final_abs_state in abstraction.final_state_set:
            #                # add final states as nodes, do not create edges!
            #                if final_abs_state not in self.G:
            #                    self.G.add_node(final_abs_state)

            #            ais = abstraction.initial_state_set.pop()
            #            abstraction.initial_state_set.add(ais)
            #            self.G.add_edge(ais, random.choice(self.G.nodes()))
            #
            #            # Connect only one final state
            #            afs = abstraction.final_state_set.pop()
            #            abstraction.final_state_set.add(afs)
            #            self.G.add_edge(afs, random.choice(self.G.nodes()))

            # Connect all init states

            for init_abs_state in abstraction.initial_state_set:
                if init_abs_state not in self.G:

                    # add random edges between each initial_state and some
                    # state in the graph. This also automatically adds all the
                    # initial_state as nodes

                    self.G.add_edge(init_abs_state,
                                    random.choice(self.G.nodes()))
            for final_abs_state in abstraction.final_state_set:
                if final_abs_state not in self.G:

                    # add random edges between each initial_state and some
                    # state in the graph. This also automatically adds all the
                    # initial_state as nodes

                    self.G.add_edge(random.choice(self.G.nodes()),
                                    final_abs_state)
        elif self.G.Type == 'test_no':
            raise err.Fatal('Internal: set_abstraction() called on a not-intended-for-testing graph!'
                            )
        else:
            logger.error('unknown graph type: {}', self.G.Type)
            raise err.Fatal('unknown graph type!')

        return self.G

    def simulate(self, sim_state_array, T):

        num_init_state = sim_state_array.n
        X_array_complete = np.zeros((num_init_state, self.A.num_dim))
        t_array_complete = np.zeros(num_init_state)
        dummy_d_array_complete = np.zeros(num_init_state)
        dummy_p_array_complete = np.zeros(num_init_state)

        # TODO: accessing A introduces a cross reference!!

        inf_array = np.tile(np.inf, self.A.num_dim)

#        for concrete_state in sim_state_array.iterable():

        for i in xrange(sim_state_array.n):
            cont_state = sim_state_array.cont_states[i, :]
            abs_state = self.A.get_abstract_state(cont_state)

            # All_Predetermined_Reachable_States

            aprs = self.G.neighbors(abs_state)
            if aprs:
                rchd_abs_state = random.choice(aprs)
                cons = self.A.get_concrete_state_constraints(rchd_abs_state)
                X_array = S.sample_interval(cons, 1)
                n = self.A.get_n_for(abs_state)
                t = n * T + T
                t_array_complete[i] = t
                X_array_complete[i, :] = X_array
            else: # If not state is reachable!

                n = self.A.get_n_for(abs_state)
                t = n * T + T
                t_array_complete[i] = np.tile(t, 1)
                X_array_complete[i, :] = inf_array

        concrete_state_arr = st.StateArray(t_array_complete,
                                           X_array_complete,
                                           dummy_d_array_complete,
                                           dummy_p_array_complete)
        return concrete_state_arr


# Matlab Engine for Pythion

class MEngPy(Simulator):

    def __init__(
            self,
            m_file_path,
            benchmark_os_path,
            parallel,
            ):
        self.parallel = parallel
        import matlab.engine as matlab_engine
        import matlab as matlab
        # Don't seem to nee matlab.engine other than to start the matlab
        # session.
        # self.matlab_engine = matlab_engine
        self.matlab = matlab

        print 'initializing matlab...'
        self.eng = matlab_engine.start_matlab()
        print 'done'

        self.m_file = m_file_path

        m_file_name_split = self.m_file.split('.')
        if m_file_name_split[1].strip() != 'm':
            raise err.Fatal('internal error!')

        self.m_fun_str = m_file_name_split[0].strip()

        # self.sim_fun = self.eng.simulate_m_file(1)

        # add paths
        # comm.call_function([], 'addpath', [SQ + benchmark_os_path + SQ])

        self.eng.addpath(benchmark_os_path)

        #TAG:CLSS
        # TODO: Remove this hack. Added for backwards compatibility
        # detect if the simulator file is a function or a class
        # source: http://blogs.mathworks.com/loren/2013/08/26/what-kind-of-matlab-file-is-this/
        # classy = 8 if class else is 0 (function or a script)
        classy = self.eng.exist(self.m_fun_str, 'class')
        if classy == 0.0:
            print 'maltab file is a function'
            self.sim_is_class = False
        elif classy == 8.0:
            print 'maltab file is a class'
            self.sim_is_class = True
            self.sim_obj = self.eng.init_plant(self.m_fun_str)
        else:
            raise err.Fatal('''Supplied matlab simulator is neither a class or a function:
                possible floating point error?. exist() returned: {}'''.format(classy))

    # Assumptions
    # For Each state a valid state is provided:
    # else [inf, inf, inf, ... inf] is returned

    def simulate(
            self,
            sim_states,
            T,
            property_checker=None,
            property_violated_flag=None,
            ):

        #print '='*100
        #print sim_states
        #print '='*100

        if property_checker is None:
            property_check = 0
        else:
            property_check = 1

        matlab = self.matlab

        m_t = matlab.double(sim_states.t.tolist())
        m_T = matlab.double([T])
        m_c = matlab.double(sim_states.cont_states.tolist())
        m_d = matlab.double(sim_states.discrete_states.tolist())
        m_p = matlab.double(sim_states.pvt_states.tolist())
        m_u = matlab.double(sim_states.controller_outputs.tolist())
        #m_p = matlab.double([0.0] * sim_states.cont_states.shape[0])
        #m_pc = matlab.double([property_check])
        m_pc = property_check

        #TAG:CLSS
        if self.sim_is_class:
            [T__, X__, D__, P__, pvf_] = self.eng.simulate_plant(
                self.sim_obj,
                m_t,
                m_T,
                m_c,
                m_d,
                m_p,
                m_u,
                m_p,
                m_pc,
                )
        else:
            [T__, X__, D__, P__, pvf_] = self.eng.simulate_plant_fun(
                self.m_fun_str,
                m_t,
                m_T,
                m_c,
                m_d,
                m_p,
                m_u,
                m_p,
                m_pc,
                )

        T_ = np.array(T__)
        X_ = np.array(X__)
        D_ = np.array(D__)
        P_ = np.array(P__)
        #print T__, X__
        #print T_, X_

        pvf = pvf_

        if property_checker is not None:
            property_violated_flag[0] = bool(pvf)

        # TODO: fix this weird matlab-numpy interfacing
        # FIXED: is it correct though?
        t_array = np.array(T_, ndmin=2)
        x = np.array(X_, ndmin=2)
        if D_.ndim <= 1:
            d = np.array(D_, ndmin=2).T
        else:
            d = D_
        if P_.ndim <= 1:
            pvt = np.array(P_, ndmin=2).T
        else:
            pvt = P_
        statearray = st.StateArray(
            t=t_array,
            x=x,
            d=d,
            pvt=pvt,
            s=sim_states.controller_states,
            u=sim_states.controller_outputs,
            pi=sim_states.plant_extraneous_inputs,
            ci=sim_states.controller_extraneous_inputs,
            )
        #print '='*100
        #print statearray
        #print '='*100
        return statearray
