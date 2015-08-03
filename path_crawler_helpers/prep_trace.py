#!/usr/bin/env python
from optparse import OptionParser
import sys
import ast
import tqdm
import glob

import z3

import py2z3.py2z3 as py2z3
import constraint_manager as cm
import fileOps as f
import err

OUTPUT_DIR_PATH = './tmp_paths/'

# TODO: should be automatically determined instead of being hardcoded
VAR_NAME_LIST = ['iv_input_arr',
                 'iv_int_state_arr',
                 'iv_float_state_arr',
                 'iv_x_arr',
                 'rv_int_state_arr',
                 'rv_float_state_arr',
                 'rv_output_arr']

VAR_TYP_DICT = {'iv_input_arr': 'R',
                'iv_int_state_arr': 'I',
                'iv_float_state_arr': 'R',
                'iv_x_arr': 'R',
                'rv_int_state_arr': 'I',
                'rv_float_state_arr': 'R',
                'rv_output_arr': 'R'}

# ##################################
# Begin the hacky functions
# ##################################


def solverlist_to_smt2file(solver_list):
    path = OUTPUT_DIR_PATH
    # 6 digit names padded with 0
    file_name = 'test{:06}.smt2'
    debug_file_name = 'test{:06}.dbg'
    #for idx, solver in enumerate(solver_list):
    # instead of enumerate, use zip. Enables tqdm to predict!
    for idx, solver in tqdm.tqdm(zip(range(len(solver_list)), solver_list)):
        file_path = f.construct_path(file_name.format(idx), path)
        debug_file_path = f.construct_path(debug_file_name.format(idx), path)
        f.write_data(file_path, solver.to_smt2())
        f.write_data(debug_file_path, repr(solver))


def convert_vars_to_array():
    pass


# TODO: fix this mess on multiple levels
def expr_obj(dim_def_dict):
    #iv_ci = Empty(); iv_ci.typStr = 'R'; iv_ci.nameStr = 'iv_ci'
    #iv_s0 = Empty(); iv_s0.typStr = 'R'; iv_s0.nameStr = 'iv_s0'
    #iv_s1 = Empty(); iv_s1.typStr = 'R'; iv_s1.nameStr = 'iv_s1'
    #iv_s2 = Empty(); iv_s2.typStr = 'R'; iv_s2.nameStr = 'iv_s2'
    #iv_s3 = Empty(); iv_s3.typStr = 'R'; iv_s3.nameStr = 'iv_s3'
    #iv_x0 = Empty(); iv_x0.typStr = 'R'; iv_x0.nameStr = 'iv_x0'
    #rv_s0 = Empty(); rv_s0.typStr = 'R'; rv_s0.nameStr = 'rv_s0'
    #rv_s1 = Empty(); rv_s1.typStr = 'R'; rv_s1.nameStr = 'rv_s1'
    #rv_s2 = Empty(); rv_s2.typStr = 'R'; rv_s2.nameStr = 'rv_s2'
    #rv_s3 = Empty(); rv_s3.typStr = 'R'; rv_s3.nameStr = 'rv_s3'
    #rv_u0 = Empty(); rv_u0.typStr = 'R'; rv_u0.nameStr = 'rv_u0'

    # py2z3 does not differentiate between i/p, o/p, and states. The same is
    # true for current CASymbolic.py. It requires an smt file w/o knowing what
    # is i/p and o/p as long as the names remain the same.
    #e.outputs = []
    #e.states = []
    #e.inputs = [iv_ci, iv_s0, iv_s1, iv_s2, iv_s3, iv_x0, rv_s0, rv_s1, rv_s2, rv_s3, rv_u0]

    ##################################################
    # Earlier idea which assumes arbitrary vars, but,
    # no arrays
    ##################################################
    #    e.inputs = []
    #    op_vals = paths[0].input_vals
    #    for v_name_str in op_vals.var_list:
    #        v = Empty()
    #        # don't care about the type
    #        v.typStr = 'X'
    #        v.nameStr = v_name_str
    #        e.inputs.append(v)
    #    print op_vals.var_list
    #####################################################

    ##################################################
    # Current idea which assumes pre-known var names
    # in the form of arrays
    ##################################################
        #var_name_list = ['iv_input_arr', 'iv_state_arr', 'iv_x_arr', 'rv_state_arr', 'rv_output_arr']
    #####################################################

    #e.parsedPathList = [(paths[0][0].py_ast, paths[0][1].py_ast_list)]
    # remove special parsing of outputs
    #e.parsedpathlist = [(path.simplified_path_pred.py_ast, path.output_vals.py_ast_list) for path in paths]
    e = Empty()
    global VAR_NAME_LIST
    global VAR_TYP_DICT
    e.inputs = []
    for var_name_str in VAR_NAME_LIST:
        v = Empty()
        # don't care about the type
        # TODO: FIX THIS!!
        #print >> sys.stderr, term.red('WARNING: setting all var types as Reals!! Ignoring Ints')
        v.typStr = VAR_TYP_DICT[var_name_str]
        # indicate a vector
        v.subTypStr = 'V'
        v.dim = dim_def_dict[var_name_str]
        v.nameStr = var_name_str
        e.inputs.append(v)

    e.outputs = []
    e.states = []

    # create an empty list which py2z3 will fillup
    e.pathListZ3 = []
    #e.parsedPathList = [(paths[0][0].py_ast, paths[0][1].py_ast_list)]
    # remove special parsing of outputs
    #e.parsedpathlist = [(path.simplified_path_pred.py_ast, path.output_vals.py_ast_list) for path in paths]
    e.parsedPathList = []
    return e


# converts string cons to z3 cons
# Refer to get_z3_solver_list() for details
def py_str_to_z3_cons(cons_py_str, dim_def_dict, dbg=False):
    e = expr_obj(dim_def_dict)

    output_cons_list = []

    cons_py_ast = ast.parse(cons_py_str)
    e.parsedPathList = [(cons_py_ast, output_cons_list)]

    # for debug!
    #e.py_str = cons_py_str

    if dbg:
        print 'cons_py_str:', cons_py_str
    z3_expr = py2z3.translate(e)
    if dbg:
        print 'z3_expr:', z3_expr.pathListZ3[0]

    return z3_expr.pathListZ3[0][0]


class NodeData(object):
    def __init__(self, parsed_ID, py_str, z3_cons):
        self.parsed_ID = parsed_ID
        self.py_str = py_str
        self.z3_cons = z3_cons
        #self.z3_str = z3_cons.sexpr()

    def __str__(self):
        s = str(self.parsed_ID)
        return s


# Terminal node data is slightly different.
# In addition to regular node data it also has a path id
class TerminalNodeData(NodeData):
    def __init__(self, path_id, *args, **kwargs):
        super(TerminalNodeData, self).__init__(*args, **kwargs)
        self.path_id = path_id


#####################
####### UNUSED ######
#####################
# Builds a tree containing exhausitve paths
# Such a tree can have undirected cycles and will have paths which pathcrawler
# might have rejected as trivially feasible
# Was a mistake when it was designed
def create_complete_cons_tree(paths):
    print '='*40
    print 'building tree...'
    node_table = {}
    tree = cm.Tree()
    node = tree.root
    node_table[node.ID] = node
    for path in paths:
        for parsed_ID, pred_str in path.path_pred.ordered_parsedID_cons_list:
            print parsed_ID,
            hash_ID = hash(parsed_ID)
            child_node = node_table.get(hash_ID)
            if child_node is None:
                child_node = cm.Node(ID=hash_ID, data=parsed_ID, pred=pred_str)
                node_table[child_node.ID] = child_node
            else:
                try:
                    assert(child_node.pred == pred_str)
                except AssertionError:
                    pass
                    #print '[mismatch:: {}, {}]'.format(child_node.pred, pred_str),
                    #raise AssertionError
                #print node.__repr__(), '-->', child_node.__repr__()
            node.add_child(child_node)
            #print node.children
            #print data
            #node.add_child(child_node)
            node = child_node
        node = tree.root
        print
    return tree


# Coverts the parsed paths to z3 solvers
# Uses py2z3.
# This is almost surely not the best way to do things, but quite convinient
def get_z3_solver_list(paths):
    dim_def_dict = paths[0].dimensions.dim_def_dict
    e = expr_obj(dim_def_dict)
    output_cons_list = []
    for path in paths:
        cons_py_str = path.simplified_path_pred.py_str + ' and ' + path.output_vals.py_str
        cons_py_ast = ast.parse(cons_py_str)
        e.parsedPathList.append((cons_py_ast, output_cons_list))

    paths_z3 = py2z3.translate(e)
    solver_list = []
    for p in paths_z3.pathListZ3:
        s = z3.Solver()
        s.add(p[0])
        #cc = p[0]
        op_list = p[1]
        for op in op_list:
            c = op[0] == op[1]
            s.add(c)
            #cc = z3.And(cc, c)
        #s.add(z3.simplify(cc))
        solver_list.append(s)
    return solver_list


class Empty():
    pass


class PathObj(object):
    # remove global cons, in other words make them True
    def unset_global_cons_unused(self):
        #self.global_z3_cons = True
        self.solver = z3.Solver()

    def set_solver_unused(self, solver):
        self.solver = solver
        return

    # Add global constraints to the tree
    # i.e., add the constraint C to every node!
    def set_global_cons(self, *args):
        self.solver = z3.Solver()
        self.solver.add(z3.And(*args))
        #self.global_z3_cons = z3.And(*args)
        return

    def sat_path_gen(self, dbg=False):
        raise NotImplementedError

    def sanity_check(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class ConsTree(cm.Tree, PathObj):
    def __init__(self, paths):
        # init base class
        super(ConsTree, self).__init__()
        # TODO: True is sent as z3_cons...works ok, but a better soln to keep
        # types uniform?
        # overwrite root node's data
        self.root.data = NodeData('root', 'True', True)
        #self.global_z3_cons = True

    #def create_cons_tree(paths):
        dim_def_dict = paths[0].dimensions.dim_def_dict
        print '='*40
        print 'building tree...', 'from', len(paths), 'paths'
        node_table = {}
        #tree = cm.Tree()
        #tree = ConsTree()
        node = self.root
        node_table[node.ID] = node
        for idx, path in enumerate(paths):

            for parsed_ID, pred_str in path.path_pred.ordered_parsedID_cons_list:
                hash_ID = hash(parsed_ID)
                child_node = node.fetch_child_using_ID(hash_ID)

                if (child_node is None) or (child_node.data.py_str != pred_str):
                    #child_node = cm.Node(ID=hash_ID, data=parsed_ID, pred=pred_str)
                    z3_cons = py_str_to_z3_cons(pred_str, dim_def_dict)
                    if type(z3_cons) is bool:
                        # can not be False!! Pathcrawler only outputs trivially
                        # true constraints and never trivially false ones.
                        assert(z3_cons)
                        continue
                    #print parsed_ID, pred_str, type(z3_cons[0]), z3_cons[0].sexpr()
                    child_node = cm.Node(ID=hash_ID, data=NodeData(parsed_ID, pred_str, z3_cons))
                    node.add_child(child_node)

                #else:
                #    try:
                #        assert(child_node.data.py_str == pred_str)
                #    except AssertionError as e:
                #        print idx
                #        print parsed_ID
                #        print 'child_node.data.py_str:', child_node.data.py_str
                #        print 'pred_str:', pred_str
                #        raise AssertionError(e)

                node = child_node
                # for loop end

            # add a termination node which has the output constraints
            op_pred_str = path.output_vals.py_str
            #print '='*100
            #print op_pred_str
            op_z3_cons = py_str_to_z3_cons(op_pred_str, dim_def_dict, dbg=False)
            #print op_z3_cons
            term_node_ID = 'tn_' + str(idx)
            child_node = cm.Node(ID=hash(term_node_ID),
                                 data=TerminalNodeData(idx, term_node_ID, op_pred_str, op_z3_cons))
            node.add_child(child_node)

            # move pointer back to the root node
            node = self.root

        # update num_paths
        self.num_paths = self.compute_paths()
        return

    def sat_path_gen(self, dbg=False):

        def traverse(S_, node):

            if dbg:
                print 'node:', node, '[pushing]'
            S_.push()
            S_.add(node.data.z3_cons)

            res = S_.check()
            if res == z3.sat:
                if dbg:
                    print 'node is SAT'
                if node.children:
                    for c in node.children:
                        if dbg:
                            print 'jumping to child node', c
                        # weird syntax because traverse(S_, c) does not work!
                        for Y in traverse(S_, c):
                            yield Y

                # reached terminal node, give the solver instance
                else:
                    if dbg:
                        print 'terminal node: yielding'
                    yield (node.data.path_id, S_)
            elif res == z3.unsat:
                if dbg:
                    print 'node is UNSAT'
            else:
                print S_.reason_unknown()
                raise err.Fatal('SAT check: unkwnown. Reason above')

            # pop the node's constraint at the end of the function
            if dbg:
                print 'popping'
            S_.pop()

        # check if global constraints are SAT
        #S = z3.Solver()
        S = self.solver
        #S.add(self.global_z3_cons)

        # if UNSAT return an empty generator:
        # https://stackoverflow.com/questions/13243766/python-empty-generator-function
        if S.check() == z3.unsat:
            return (_ for _ in ())
        else:
            return traverse(S, self.root)

    def sanity_check(self):
        flat_tree = self.flatten()
        num_paths = self.compute_paths()
        return len(flat_tree) == num_paths


class ConsList(PathObj):
    def __init__(self, init_from, initializer):
        if init_from == 'paths':
            paths = initializer
            solver_list = get_z3_solver_list(paths)
            # collate all constraints in the solver by `Anding' them
            self.cons_list = [z3.And(*solver.assertions()) for solver in solver_list]
            self.num_paths = len(self.cons_list)
        elif init_from == 'smt2_files':
            dir_path = initializer
            filenames = glob.glob(dir_path + '*.smt2')
            self.cons_list = []
            print 'reading smt2 files'
            for fl in filenames:

                # ##!!##logger.debug('reading path: {}'.format(f))

                smt_string = f.get_data(fl)
                try:
                    pc = z3.parse_smt2_string(smt_string, decls={})
                    self.cons_list.append(pc)
                except Exception, e:
                    print fl
                    raise e
        return

    def sat_path_gen(self, dbg=False):
        #S = z3.Solver()
        #S.add(self.global_z3_cons)
        S = self.solver

        for idx, c in enumerate(self.cons_list):
            S.push()
            S.add(c)

            res = S.check()

            if res == z3.sat:
                if dbg:
                    print 'cons is SAT'
                yield (idx, S)
            elif res == z3.unsat:
                if dbg:
                    print 'cons is UNSAT'
            else:
                print S.reason_unknown()
                raise err.Fatal('SAT check: unkwnown. Reason above')

            S.pop()
        return

    # slower function, to mimic the older implementation.
    # was written to diagnose the speedup!
    def sat_path_gen_old(self, dbg=False):

        for idx, c in enumerate(self.cons_list):
            S = z3.Solver()
            #S.add(self.global_z3_cons)
            S.add(*self.solver.assertions())
            S.add(c)

            res = S.check()

            if res == z3.sat:
                if dbg:
                    print 'cons is SAT'
                yield (idx, S)
            elif res == z3.unsat:
                if dbg:
                    print 'cons is UNSAT'
            else:
                print S.reason_unknown()
                raise err.Fatal('SAT check: unkwnown. Reason above')

        return

    def sanity_check(self):
        return True

    def __str__(self):
        s = ''
        for cons in self.cons_list:
            s += str(cons)
        return s


# TODO: code duplication w.r.t. pathcrawler_obj()
def get_conslist_from_smt2(dir_path):
    path_obj = ConsList('smt2_files', dir_path)
    assert(path_obj.sanity_check())
    return path_obj


def pathcrawler_obj(paths, opt):

    if opt == 'list':
        path_obj = ConsList('paths', paths)
    elif opt == 'tree':
        # TODO: ideally should instantiate ConsTree()
        # but ConsTree inherits form 2 classes and calls Super!
        # not shure how its decided about args passing to Super...
        # Should be fixed after understaindg how arguement passing in super
        # works in case of Multiple Inheritance.
        path_obj = ConsTree(paths)
    else:
        raise err.Fatal('unhandled option!:{}'.format(opt))

    assert(path_obj.sanity_check())
    return path_obj


def paths_to_smt2(paths):
    solver_list = get_z3_solver_list(paths)
    solverlist_to_smt2file(solver_list)


# sample usage
def main():
    import pc_trace_parser as pctp
    usage = 'usage: %prog <filename> or %prog --test'
    parser = OptionParser(usage)

    parser.add_option('--demo', type='choice', dest='structure', choices=['list', 'tree'], default=None, help='demo')
    parser.add_option('--dump', action='store_true', dest='dump', help='dump smt2 files in'+OUTPUT_DIR_PATH)
    parser.add_option('--test', action='store_true', dest='test', help='run unit tests')

    (options, args) = parser.parse_args()

    if options.test:
        #paths = pctp.trace_file_to_paths(test_file)
        paths = pctp.trace_to_paths(TEST_TRACE)
        run_unit_tests(paths)
        return
    else:
        #print options.filename
        #data = read_default_file()
        if not args:
            parser.error(usage)

        if options.dump:
            if not f.is_dir_empty(OUTPUT_DIR_PATH):
                raw_input('{} not empty. Empty it first.'.format(OUTPUT_DIR_PATH))
                return
            else:
                paths = pctp.trace_file_to_paths(args[0])
                path_obj = pathcrawler_obj(paths, 'list')
                paths_to_smt2(paths)

        if options.structure is not None:
            # tree
            if options.structure == 'tree':
                paths = pctp.trace_file_to_paths(args[0])
                path_obj = pathcrawler_obj(paths, 'tree')
                print path_obj
                print 'num_paths:', path_obj.compute_paths()
                #path_obj.pretty_print()
                #pt = PathCrawlerTrace(args[0], 'tree')
            # list
            else:
                paths = pctp.trace_file_to_paths(args[0])
                path_obj = pathcrawler_obj(paths, 'list')
                print path_obj
                #pt = PathCrawlerTrace(args[0], 'list')
                #pt.paths_to_smt2()
                #paths_to_smt2(paths)
            #print path_obj
    return


def run_unit_tests(paths):
    ##############
    ## Test Tree
    ##############

    path_obj = pathcrawler_obj(paths, 'tree')
    #pt = PathCrawlerTrace(test_file, 'tree')

    dim_def_dict = paths[0].dimensions.dim_def_dict
    #cons_tree = pt.paths_to_cons_tree()
    #cons_tree.pretty_print()
    #flat_tree = cons_tree.flatten()
    #for path in flat_tree:
    #    print path
    print 'total paths', path_obj.num_paths
    assert(path_obj.num_paths == 26)

    dbg = True
    # TEST 1
    num_SAT_paths = get_sat_paths_test(path_obj, True, dbg)
    assert(num_SAT_paths == path_obj.num_paths)
    print 'TEST 1: success', num_SAT_paths

    # TEST 2
    num_SAT_paths = get_sat_paths_test(path_obj, False, dbg)
    assert(num_SAT_paths == 0)
    print 'TEST 2: success', num_SAT_paths

    # TEST 3
    cons = py_str_to_z3_cons('iv_x_arr[0]<=68.0 and iv_x_arr[0]>=67.0', dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, cons, dbg)
    assert(num_SAT_paths == 9)
    print 'TEST 3: success', num_SAT_paths

    # TEST 4
    cons = py_str_to_z3_cons('iv_x_arr[0]<=50.0', dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, cons, dbg)
    assert(num_SAT_paths == 9)
    print 'TEST 4: success', num_SAT_paths

    # TEST 5
    cons = py_str_to_z3_cons('iv_x_arr[0]>=100.0', dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, cons, dbg)
    assert(num_SAT_paths == 8)
    print 'TEST 5: success', num_SAT_paths

    # TEST 6
    cons_py_str = 'iv_x_arr[0]>=100.0 and iv_int_state_arr[3]<5'
    z3_cons = py_str_to_z3_cons(cons_py_str, dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, z3_cons, dbg)
    #assert(num_SAT_paths == 6)
    print 'TEST 6: success', num_SAT_paths

    # TEST 7
    cons_py_str = 'iv_x_arr[0]>=100.0 and iv_int_state_arr[3]>5'
    z3_cons = py_str_to_z3_cons(cons_py_str, dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, z3_cons, dbg)
    #assert(num_SAT_paths == 2)
    print 'TEST 7: success', num_SAT_paths

    ##############
    ## Test List
    ##############
    path_obj = pathcrawler_obj(paths, 'list')
    #pt = PathCrawlerTrace(test_file, 'list')
    dim_def_dict = paths[0].dimensions.dim_def_dict

    print 'total paths', path_obj.num_paths
    assert(path_obj.num_paths == 26)

    dbg = True
    # TEST 1
    num_SAT_paths = get_sat_paths_test(path_obj, True, dbg)
    assert(num_SAT_paths == path_obj.num_paths)
    print 'TEST 1: success', num_SAT_paths

    # TEST 2
    num_SAT_paths = get_sat_paths_test(path_obj, False, dbg)
    assert(num_SAT_paths == 0)
    print 'TEST 2: success', num_SAT_paths

    # TEST 3
    cons = py_str_to_z3_cons('iv_x_arr[0]<=68.0 and iv_x_arr[0]>=67.0', dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, cons, dbg)
    assert(num_SAT_paths == 9)
    print 'TEST 3: success', num_SAT_paths

    # TEST 4
    cons = py_str_to_z3_cons('iv_x_arr[0]<=50.0', dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, cons, dbg)
    assert(num_SAT_paths == 9)
    print 'TEST 4: success', num_SAT_paths

    # TEST 5
    cons = py_str_to_z3_cons('iv_x_arr[0]>=100.0', dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, cons, dbg)
    assert(num_SAT_paths == 8)
    print 'TEST 5: success', num_SAT_paths

    # TEST 6
    cons_py_str = 'iv_x_arr[0]>=100.0 and iv_int_state_arr[3]<5'
    z3_cons = py_str_to_z3_cons(cons_py_str, dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, z3_cons, dbg)
    #assert(num_SAT_paths == 6)
    print 'TEST 6: success', num_SAT_paths

    # TEST 7
    cons_py_str = 'iv_x_arr[0]>=100.0 and iv_int_state_arr[3]>5'
    z3_cons = py_str_to_z3_cons(cons_py_str, dim_def_dict)
    num_SAT_paths = get_sat_paths_test(path_obj, z3_cons, dbg)
    #assert(num_SAT_paths == 2)
    print 'TEST 7: success', num_SAT_paths
    #pt.paths_to_smt2()
    return


def get_sat_paths_test(cons_tree, global_cons, dbg):
    cons_tree.set_global_cons(global_cons)
    SAT_path_ctr = 0
    for pid, s in cons_tree.sat_path_gen():
        if dbg:
            #print >> sys.stderr, '='*20, pid, '='*20
            print >> sys.stderr, s
        SAT_path_ctr += 1
    #if dbg: print >> sys.stderr, SAT_path_ctr
    return SAT_path_ctr


# TODO: use this data instead of the file to perform tests
TEST_TRACE = '''


TEST CASE 1

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 488.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 -29_2 +31 -38 +38b +41 -44 +47


Path Predicate for case 1:
heater.c: +29 input[0].x_arr[0]>=66.000000 (iteration of loop line 17)
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5 (exit loop line 17)
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: +47 0=0

Simplified Path Predicate for case 1:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]>=70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]>=5 AND
0<>input[0].int_state_arr[1]

Output Values for case 1: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 1, 1
ret_val[0].int_state_arr[1] = 0, 0
ret_val[0].int_state_arr[2] = 0, 0
ret_val[0].output_arr[0] = 0.000000, 0.000000
ret_val[0].int_state_arr[3] = (input[0].int_state_arr[3]+1), -132498

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: -47 0<>0
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 +38b +41 -44 -47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: +44 1>2
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 +38b +41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 0=input[0].int_state_arr[1]
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 +38b -41


TEST CASE 2

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = 0;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 488.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 -29_2 +31 -38 +38b -41 -44 +47


Path Predicate for case 2:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: +47 0=0

Simplified Path Predicate for case 2:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]>=70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]>=5 AND
0=input[0].int_state_arr[1]

Output Values for case 2: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 0, 0
ret_val[0].int_state_arr[1] = 0, 0
ret_val[0].int_state_arr[2] = 0, 0
ret_val[0].output_arr[0] = 0.000000, 0.000000
ret_val[0].int_state_arr[3] = (input[0].int_state_arr[3]+1), -132498

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: -47 0<>0
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 +38b -41 -44 -47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: +44 0>2
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 +38b -41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 -38b


TEST CASE 3

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 488.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 -29_2 +31 -38 -38b +41 -44 +47


Path Predicate for case 3:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: -44 (input[0].int_state_arr[0]+1)=<2
heater.c: +47 0=0

Simplified Path Predicate for case 3:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]>=70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
0<>input[0].int_state_arr[1] AND
(input[0].int_state_arr[0]+1)=<2

Output Values for case 3: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = (input[0].int_state_arr[0]+1), -13089
ret_val[0].int_state_arr[1] = 0, 0
ret_val[0].int_state_arr[2] = 0, 0
ret_val[0].output_arr[0] = 0.000000, 0.000000
ret_val[0].int_state_arr[3] = (input[0].int_state_arr[3]+1), -132498

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: -44 (input[0].int_state_arr[0]+1)=<2
heater.c: -47 0<>0
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 -38b +41 -44 -47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 -38b +41 +44


TEST CASE 4

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = 570691921;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 488.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 -29_2 +31 -38 -38b +41 +44 -47


Path Predicate for case 4:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
heater.c: -47 input[0].int_state_arr[1]<>0

Simplified Path Predicate for case 4:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]>=70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
0<>input[0].int_state_arr[1] AND
(input[0].int_state_arr[0]+1)>2 AND
input[0].int_state_arr[1]<>0

Output Values for case 4: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = (input[0].int_state_arr[0]+1), 570691922
ret_val[0].int_state_arr[1] = input[0].int_state_arr[1], -97684
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 1
ret_val[0].output_arr[0] = ((double)input[0].int_state_arr[1]), -97684.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
heater.c: +47 input[0].int_state_arr[1]=0
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 -38b +41 +44 +47
infeasible (with the given preconditions) (detected by constraint propagation)

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 0=input[0].int_state_arr[1]
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 -38b -41


TEST CASE 5

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = 0;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 488.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 -29_2 +31 -38 -38b -41 -44 +47


Path Predicate for case 5:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: -44 input[0].int_state_arr[0]=<2
heater.c: +47 0=0

Simplified Path Predicate for case 5:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]>=70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
0=input[0].int_state_arr[1] AND
input[0].int_state_arr[0]=<2

Output Values for case 5: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = input[0].int_state_arr[0], -13090
ret_val[0].int_state_arr[1] = 0, 0
ret_val[0].int_state_arr[2] = 0, 0
ret_val[0].output_arr[0] = 0.000000, 0.000000
ret_val[0].int_state_arr[3] = (input[0].int_state_arr[3]+1), -132498

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: -44 input[0].int_state_arr[0]=<2
heater.c: -47 0<>0
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 -38b -41 -44 -47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: +44 input[0].int_state_arr[0]>2
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 -38b -41 +44


TEST CASE 6

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = 2096930252;
input__controller[0].int_state_arr[1] = 0;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 488.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 -29_2 +31 -38 -38b -41 +44 +47


Path Predicate for case 6:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: +44 input[0].int_state_arr[0]>2
heater.c: +47 0=0

Simplified Path Predicate for case 6:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]>=70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
0=input[0].int_state_arr[1] AND
input[0].int_state_arr[0]>2

Output Values for case 6: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = input[0].int_state_arr[0], 2096930252
ret_val[0].int_state_arr[1] = 0, 0
ret_val[0].int_state_arr[2] = 0, 0
ret_val[0].output_arr[0] = 0.000000, 0.000000
ret_val[0].int_state_arr[3] = (input[0].int_state_arr[3]+1), -132498

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: +44 input[0].int_state_arr[0]>2
heater.c: -47 0<>0
Path Prefix to cover :
heater.c
+29 -29_2 +31 -38 -38b -41 +44 -47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
Path Prefix to cover :
heater.c
+29 -29_2 +31 +38


TEST CASE 7

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = 1425928325;
input__controller[0].x_arr[0] = 488.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 -29_2 +31 +38 +41 -44 +47


Path Predicate for case 7:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: +47 0=0

Simplified Path Predicate for case 7:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]>=70.000000 AND
input[0].int_state_arr[3]>=5 AND
0<>input[0].int_state_arr[1]

Output Values for case 7: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 1, 1
ret_val[0].int_state_arr[1] = 0, 0
ret_val[0].int_state_arr[2] = 0, 0
ret_val[0].output_arr[0] = 0.000000, 0.000000
ret_val[0].int_state_arr[3] = (input[0].int_state_arr[3]+1), 1425928326

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: -47 0<>0
Path Prefix to cover :
heater.c
+29 -29_2 +31 +38 +41 -44 -47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: +41 0<>input[0].int_state_arr[1]
heater.c: +44 1>2
Path Prefix to cover :
heater.c
+29 -29_2 +31 +38 +41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 0=input[0].int_state_arr[1]
Path Prefix to cover :
heater.c
+29 -29_2 +31 +38 -41


TEST CASE 8

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = 0;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = 1425928325;
input__controller[0].x_arr[0] = 488.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 -29_2 +31 +38 -41 -44 +47


Path Predicate for case 8:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: +47 0=0

Simplified Path Predicate for case 8:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]>=70.000000 AND
input[0].int_state_arr[3]>=5 AND
0=input[0].int_state_arr[1]

Output Values for case 8: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 0, 0
ret_val[0].int_state_arr[1] = 0, 0
ret_val[0].int_state_arr[2] = 0, 0
ret_val[0].output_arr[0] = 0.000000, 0.000000
ret_val[0].int_state_arr[3] = (input[0].int_state_arr[3]+1), 1425928326

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: -47 0<>0
Path Prefix to cover :
heater.c
+29 -29_2 +31 +38 -41 -44 -47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 0=input[0].int_state_arr[1]
heater.c: +44 0>2
Path Prefix to cover :
heater.c
+29 -29_2 +31 +38 -41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: -29_2 input[0].x_arr[0]>=70.000000
heater.c: -31 input[0].x_arr[0]<70.000000
Path Prefix to cover :
heater.c
+29 -29_2 -31
infeasible (conjunction of constraint and its negation)

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
Path Prefix to cover :
heater.c
+29 +29_2


TEST CASE 9

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 69.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 +29_2 -38 +38b +41 -44 -47


Path Predicate for case 9:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: -47 2<>0

Simplified Path Predicate for case 9:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]>=5 AND
2<>input[0].int_state_arr[1]

Output Values for case 9: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 1, 1
ret_val[0].int_state_arr[1] = 2, 2
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 126654
ret_val[0].output_arr[0] = 2.000000, 2.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: +47 2=0
Path Prefix to cover :
heater.c
+29 +29_2 -38 +38b +41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: +44 1>2
Path Prefix to cover :
heater.c
+29 +29_2 -38 +38b +41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 2=input[0].int_state_arr[1]
Path Prefix to cover :
heater.c
+29 +29_2 -38 +38b -41


TEST CASE 10

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = 2;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 69.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 +29_2 -38 +38b -41 -44 -47


Path Predicate for case 10:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: -47 2<>0

Simplified Path Predicate for case 10:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]>=5 AND
2=input[0].int_state_arr[1]

Output Values for case 10: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 0, 0
ret_val[0].int_state_arr[1] = 2, 2
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 126654
ret_val[0].output_arr[0] = 2.000000, 2.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: +47 2=0
Path Prefix to cover :
heater.c
+29 +29_2 -38 +38b -41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: +44 0>2
Path Prefix to cover :
heater.c
+29 +29_2 -38 +38b -41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
Path Prefix to cover :
heater.c
+29 +29_2 -38 -38b


TEST CASE 11

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 69.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 +29_2 -38 -38b +41 -44 -47


Path Predicate for case 11:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: -44 (input[0].int_state_arr[0]+1)=<2
heater.c: -47 2<>0

Simplified Path Predicate for case 11:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
2<>input[0].int_state_arr[1] AND
(input[0].int_state_arr[0]+1)=<2

Output Values for case 11: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = (input[0].int_state_arr[0]+1), -13089
ret_val[0].int_state_arr[1] = 2, 2
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 1
ret_val[0].output_arr[0] = 2.000000, 2.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: -44 (input[0].int_state_arr[0]+1)=<2
heater.c: +47 2=0
Path Prefix to cover :
heater.c
+29 +29_2 -38 -38b +41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
Path Prefix to cover :
heater.c
+29 +29_2 -38 -38b +41 +44


TEST CASE 12

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = 68604515;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 69.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 +29_2 -38 -38b +41 +44 -47


Path Predicate for case 12:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
heater.c: -47 input[0].int_state_arr[1]<>0

Simplified Path Predicate for case 12:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
2<>input[0].int_state_arr[1] AND
(input[0].int_state_arr[0]+1)>2 AND
input[0].int_state_arr[1]<>0

Output Values for case 12: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = (input[0].int_state_arr[0]+1), 68604516
ret_val[0].int_state_arr[1] = input[0].int_state_arr[1], -97684
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 1
ret_val[0].output_arr[0] = ((double)input[0].int_state_arr[1]), -97684.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
heater.c: +47 input[0].int_state_arr[1]=0
Path Prefix to cover :
heater.c
+29 +29_2 -38 -38b +41 +44 +47


TEST CASE 13

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = 68604515;
input__controller[0].int_state_arr[1] = 0;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 69.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 +29_2 -38 -38b +41 +44 +47


Path Predicate for case 13:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
heater.c: +47 input[0].int_state_arr[1]=0

Simplified Path Predicate for case 13:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
2<>input[0].int_state_arr[1] AND
(input[0].int_state_arr[0]+1)>2 AND
input[0].int_state_arr[1]=0

Output Values for case 13: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = (input[0].int_state_arr[0]+1), 68604516
ret_val[0].int_state_arr[1] = 0, 0
ret_val[0].int_state_arr[2] = 0, 0
ret_val[0].output_arr[0] = 0.000000, 0.000000
ret_val[0].int_state_arr[3] = (input[0].int_state_arr[3]+1), -132498

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 2=input[0].int_state_arr[1]
Path Prefix to cover :
heater.c
+29 +29_2 -38 -38b -41


TEST CASE 14

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = 2;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 69.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 +29_2 -38 -38b -41 -44 -47


Path Predicate for case 14:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: -44 input[0].int_state_arr[0]=<2
heater.c: -47 2<>0

Simplified Path Predicate for case 14:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
2=input[0].int_state_arr[1] AND
input[0].int_state_arr[0]=<2

Output Values for case 14: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = input[0].int_state_arr[0], -13090
ret_val[0].int_state_arr[1] = 2, 2
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 1
ret_val[0].output_arr[0] = 2.000000, 2.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: -44 input[0].int_state_arr[0]=<2
heater.c: +47 2=0
Path Prefix to cover :
heater.c
+29 +29_2 -38 -38b -41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: +44 input[0].int_state_arr[0]>2
Path Prefix to cover :
heater.c
+29 +29_2 -38 -38b -41 +44


TEST CASE 15

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = 188711622;
input__controller[0].int_state_arr[1] = 2;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = 69.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 +29_2 -38 -38b -41 +44 -47


Path Predicate for case 15:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: +44 input[0].int_state_arr[0]>2
heater.c: -47 2<>0

Simplified Path Predicate for case 15:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
2=input[0].int_state_arr[1] AND
input[0].int_state_arr[0]>2

Output Values for case 15: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = input[0].int_state_arr[0], 188711622
ret_val[0].int_state_arr[1] = 2, 2
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 1
ret_val[0].output_arr[0] = 2.000000, 2.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: +44 input[0].int_state_arr[0]>2
heater.c: +47 2=0
Path Prefix to cover :
heater.c
+29 +29_2 -38 -38b -41 +44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
Path Prefix to cover :
heater.c
+29 +29_2 +38


TEST CASE 16

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = 1820462094;
input__controller[0].x_arr[0] = 69.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 +29_2 +38 +41 -44 -47


Path Predicate for case 16:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: -47 2<>0

Simplified Path Predicate for case 16:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]>=5 AND
2<>input[0].int_state_arr[1]

Output Values for case 16: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 1, 1
ret_val[0].int_state_arr[1] = 2, 2
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 126654
ret_val[0].output_arr[0] = 2.000000, 2.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: +47 2=0
Path Prefix to cover :
heater.c
+29 +29_2 +38 +41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: +41 2<>input[0].int_state_arr[1]
heater.c: +44 1>2
Path Prefix to cover :
heater.c
+29 +29_2 +38 +41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 2=input[0].int_state_arr[1]
Path Prefix to cover :
heater.c
+29 +29_2 +38 -41


TEST CASE 17

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = 2;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = 1820462094;
input__controller[0].x_arr[0] = 69.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
+29 +29_2 +38 -41 -44 -47


Path Predicate for case 17:
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: -47 2<>0

Simplified Path Predicate for case 17:
input[0].x_arr[0]>=66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]>=5 AND
2=input[0].int_state_arr[1]

Output Values for case 17: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 0, 0
ret_val[0].int_state_arr[1] = 2, 2
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 126654
ret_val[0].output_arr[0] = 2.000000, 2.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: +47 2=0
Path Prefix to cover :
heater.c
+29 +29_2 +38 -41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: +29 input[0].x_arr[0]>=66.000000
heater.c: +29_2 input[0].x_arr[0]<70.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 2=input[0].int_state_arr[1]
heater.c: +44 0>2
Path Prefix to cover :
heater.c
+29 +29_2 +38 -41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
Path Prefix to cover :
heater.c
-29


TEST CASE 18

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = -35.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
-29 -31 +33 -38 +38b +41 -44 -47


Path Predicate for case 18:
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: -47 1<>0

Simplified Path Predicate for case 18:
input[0].x_arr[0]<66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]>=5 AND
1<>input[0].int_state_arr[1]

Output Values for case 18: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 1, 1
ret_val[0].int_state_arr[1] = 1, 1
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 126654
ret_val[0].output_arr[0] = 1.000000, 1.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: +47 1=0
Path Prefix to cover :
heater.c
-29 -31 +33 -38 +38b +41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: +44 1>2
Path Prefix to cover :
heater.c
-29 -31 +33 -38 +38b +41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 1=input[0].int_state_arr[1]
Path Prefix to cover :
heater.c
-29 -31 +33 -38 +38b -41


TEST CASE 19

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = 1;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = -35.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
-29 -31 +33 -38 +38b -41 -44 -47


Path Predicate for case 19:
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: -47 1<>0

Simplified Path Predicate for case 19:
input[0].x_arr[0]<66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]>=5 AND
1=input[0].int_state_arr[1]

Output Values for case 19: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 0, 0
ret_val[0].int_state_arr[1] = 1, 1
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 126654
ret_val[0].output_arr[0] = 1.000000, 1.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: +47 1=0
Path Prefix to cover :
heater.c
-29 -31 +33 -38 +38b -41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: +38b input[0].int_state_arr[2]>=5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: +44 0>2
Path Prefix to cover :
heater.c
-29 -31 +33 -38 +38b -41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
Path Prefix to cover :
heater.c
-29 -31 +33 -38 -38b


TEST CASE 20

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = -35.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
-29 -31 +33 -38 -38b +41 -44 -47


Path Predicate for case 20:
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: -44 (input[0].int_state_arr[0]+1)=<2
heater.c: -47 1<>0

Simplified Path Predicate for case 20:
input[0].x_arr[0]<66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
1<>input[0].int_state_arr[1] AND
(input[0].int_state_arr[0]+1)=<2

Output Values for case 20: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = (input[0].int_state_arr[0]+1), -13089
ret_val[0].int_state_arr[1] = 1, 1
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 1
ret_val[0].output_arr[0] = 1.000000, 1.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: -44 (input[0].int_state_arr[0]+1)=<2
heater.c: +47 1=0
Path Prefix to cover :
heater.c
-29 -31 +33 -38 -38b +41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
Path Prefix to cover :
heater.c
-29 -31 +33 -38 -38b +41 +44


TEST CASE 21

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = 1089094964;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = -35.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
-29 -31 +33 -38 -38b +41 +44 -47


Path Predicate for case 21:
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
heater.c: -47 input[0].int_state_arr[1]<>0

Simplified Path Predicate for case 21:
input[0].x_arr[0]<66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
1<>input[0].int_state_arr[1] AND
(input[0].int_state_arr[0]+1)>2 AND
input[0].int_state_arr[1]<>0

Output Values for case 21: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = (input[0].int_state_arr[0]+1), 1089094965
ret_val[0].int_state_arr[1] = input[0].int_state_arr[1], -97684
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 1
ret_val[0].output_arr[0] = ((double)input[0].int_state_arr[1]), -97684.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
heater.c: +47 input[0].int_state_arr[1]=0
Path Prefix to cover :
heater.c
-29 -31 +33 -38 -38b +41 +44 +47


TEST CASE 22

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = 1089094964;
input__controller[0].int_state_arr[1] = 0;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = -35.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
-29 -31 +33 -38 -38b +41 +44 +47


Path Predicate for case 22:
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: +44 (input[0].int_state_arr[0]+1)>2
heater.c: +47 input[0].int_state_arr[1]=0

Simplified Path Predicate for case 22:
input[0].x_arr[0]<66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
1<>input[0].int_state_arr[1] AND
(input[0].int_state_arr[0]+1)>2 AND
input[0].int_state_arr[1]=0

Output Values for case 22: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = (input[0].int_state_arr[0]+1), 1089094965
ret_val[0].int_state_arr[1] = 0, 0
ret_val[0].int_state_arr[2] = 0, 0
ret_val[0].output_arr[0] = 0.000000, 0.000000
ret_val[0].int_state_arr[3] = (input[0].int_state_arr[3]+1), -132498

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 1=input[0].int_state_arr[1]
Path Prefix to cover :
heater.c
-29 -31 +33 -38 -38b -41


TEST CASE 23

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = 1;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = -35.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
-29 -31 +33 -38 -38b -41 -44 -47


Path Predicate for case 23:
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: -44 input[0].int_state_arr[0]=<2
heater.c: -47 1<>0

Simplified Path Predicate for case 23:
input[0].x_arr[0]<66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
1=input[0].int_state_arr[1] AND
input[0].int_state_arr[0]=<2

Output Values for case 23: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = input[0].int_state_arr[0], -13090
ret_val[0].int_state_arr[1] = 1, 1
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 1
ret_val[0].output_arr[0] = 1.000000, 1.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: -44 input[0].int_state_arr[0]=<2
heater.c: +47 1=0
Path Prefix to cover :
heater.c
-29 -31 +33 -38 -38b -41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: +44 input[0].int_state_arr[0]>2
Path Prefix to cover :
heater.c
-29 -31 +33 -38 -38b -41 +44


TEST CASE 24

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = 1303328685;
input__controller[0].int_state_arr[1] = 1;
input__controller[0].int_state_arr[2] = 0;
input__controller[0].int_state_arr[3] = -132499;
input__controller[0].x_arr[0] = -35.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
-29 -31 +33 -38 -38b -41 +44 -47


Path Predicate for case 24:
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: +44 input[0].int_state_arr[0]>2
heater.c: -47 1<>0

Simplified Path Predicate for case 24:
input[0].x_arr[0]<66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]<5 AND
input[0].int_state_arr[2]<5 AND
1=input[0].int_state_arr[1] AND
input[0].int_state_arr[0]>2

Output Values for case 24: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = input[0].int_state_arr[0], 1303328685
ret_val[0].int_state_arr[1] = 1, 1
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 1
ret_val[0].output_arr[0] = 1.000000, 1.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: -38 input[0].int_state_arr[3]<5
heater.c: -38b input[0].int_state_arr[2]<5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: +44 input[0].int_state_arr[0]>2
heater.c: +47 1=0
Path Prefix to cover :
heater.c
-29 -31 +33 -38 -38b -41 +44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: +38 input[0].int_state_arr[3]>=5
Path Prefix to cover :
heater.c
-29 -31 +33 +38


TEST CASE 25

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = -97684;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = 297982856;
input__controller[0].x_arr[0] = -35.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
-29 -31 +33 +38 +41 -44 -47


Path Predicate for case 25:
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: -47 1<>0

Simplified Path Predicate for case 25:
input[0].x_arr[0]<66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]>=5 AND
1<>input[0].int_state_arr[1]

Output Values for case 25: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 1, 1
ret_val[0].int_state_arr[1] = 1, 1
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 126654
ret_val[0].output_arr[0] = 1.000000, 1.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: -44 1=<2
heater.c: +47 1=0
Path Prefix to cover :
heater.c
-29 -31 +33 +38 +41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: +41 1<>input[0].int_state_arr[1]
heater.c: +44 1>2
Path Prefix to cover :
heater.c
-29 -31 +33 +38 +41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 1=input[0].int_state_arr[1]
Path Prefix to cover :
heater.c
-29 -31 +33 +38 -41


TEST CASE 26

Dimensions:
input__controller = 1;
input__controller[0].input_arr = 1;
input__controller[0].int_state_arr = 4;
input__controller[0].float_state_arr = 0;
input__controller[0].x_arr = 1;
ret_val__controller = 1;
ret_val__controller[0].int_state_arr = 4;
ret_val__controller[0].float_state_arr = 0;
ret_val__controller[0].output_arr = 1;

Other input values:
input__controller[0].input_arr[0] = 413.000000;
input__controller[0].int_state_arr[0] = -13090;
input__controller[0].int_state_arr[1] = 1;
input__controller[0].int_state_arr[2] = 126653;
input__controller[0].int_state_arr[3] = 297982856;
input__controller[0].x_arr[0] = -35.000000;
ret_val__controller[0].int_state_arr[0] = -94157;
ret_val__controller[0].int_state_arr[1] = 150061;
ret_val__controller[0].int_state_arr[2] = -39978;
ret_val__controller[0].int_state_arr[3] = -197447;
ret_val__controller[0].output_arr[0] = -157.000000;

Result:
unknown

Path Covered :
heater.c
-29 -31 +33 +38 -41 -44 -47


Path Predicate for case 26:
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: -47 1<>0

Simplified Path Predicate for case 26:
input[0].x_arr[0]<66.000000 AND
input[0].x_arr[0]<70.000000 AND
input[0].int_state_arr[3]>=5 AND
1=input[0].int_state_arr[1]

Output Values for case 26: (Symbolic,Concrete)
return value = 0, 0
ret_val[0].int_state_arr[0] = 0, 0
ret_val[0].int_state_arr[1] = 1, 1
ret_val[0].int_state_arr[2] = (input[0].int_state_arr[2]+1), 126654
ret_val[0].output_arr[0] = 1.000000, 1.000000
ret_val[0].int_state_arr[3] = 0, 0

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: -44 0=<2
heater.c: +47 1=0
Path Prefix to cover :
heater.c
-29 -31 +33 +38 -41 -44 +47
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: +33 input[0].x_arr[0]<66.000000
heater.c: +38 input[0].int_state_arr[3]>=5
heater.c: -41 1=input[0].int_state_arr[1]
heater.c: +44 0>2
Path Prefix to cover :
heater.c
-29 -31 +33 +38 -41 +44
trivially infeasible

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: -31 input[0].x_arr[0]<70.000000
heater.c: -33 input[0].x_arr[0]>=66.000000
Path Prefix to cover :
heater.c
-29 -31 -33
infeasible (conjunction of constraint and its negation)

to explore negation deepest unexplored condition of predicate,
Path Predicate Prefix to solve :
heater.c: -29 input[0].x_arr[0]<66.000000
heater.c: +31 input[0].x_arr[0]>=70.000000
Path Prefix to cover :
heater.c
-29 +31
infeasible (with the given preconditions) (detected by constraint propagation)
'''

if __name__ == '__main__':
    #with term.fullscreen():
    main()
