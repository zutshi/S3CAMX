#!/usr/bin/env python
import pyparsing as pp
import ast
import re
from optparse import OptionParser

import fileOps as f
import err
import py2z3.py2z3 as py2z3
import z3

DEFAULTFILENAME = './trace/controller'
OUTPUT_DIR_PATH = './tmp_paths/'
# global tokens
SEMI = pp.Literal(";").suppress()
COLON = pp.Literal(":").suppress()
COMMA = pp.Literal(",").suppress()

integer = pp.Word(pp.nums)
#IDENT = pp.Word(pp.srange("[a-zA-Z_]"), pp.srange("[a-zA-Z0-9_]"))
ident = pp.Word(pp.alphanums+"_")


def read_default_file():
    fileName = DEFAULTFILENAME
    data = f.get_data(fileName)
    return data


class TestCase(object):
    def __init__(self, s):
        self.dimensions = s[0]
        self.input_vals = s[1]
        self.path_pred = s[2]
        self.output_vals = s[3]
        return


# format:
#    iv_x0<660 AND
#    iv_x0<700 AND
#    iv_s3>=5 AND
#    ...
#    ###########
#    operators present in a trace file: replaced to
#    =      :   ==
#    <>     :   !=
#    >=     :   not replaced
#    =<     :   >=
class PathPred():
    ctr = 0

    def __init__(self, s_):
        #print '='*20, PathPred.ctr, '='*20
        PathPred.ctr += 1
        s = s_[0]
        s = s.replace('AND', 'and')
        s = s.replace('\n', ' ')
        # prevent matching of '>=' and '=<'...
        # usual replace fails: s = s.replace('=', '==')
        # (?<!...): negative look behind for '>'
        # (?!...): negative look forward for '<'
        s = re.sub(r'(?<!>)=(?!<)', r'==', s)
        #print s
        s = s.replace('<>', '!=')
        #print s
        s = s.replace(r'=<', r'<=')
        s = s.replace('(double)', '')
        s = s.replace('(int)', '')
        #print s
        self.py_str = s
        #############
        # TODO: below is not being used. ast conversion is done at the end
        # But its good for incremental error check, so let it stay for the time
        # being!
        # ###########
        # TODO: remove try block for efficiency
        #       current purpose is to improve error reporting
        try:
            self.py_ast = ast.parse(s)
        except:
            print s_[0], '\n########', s
            raise err.Fatal('python ast parsing failure')
        #self.z3_cons = py2z3.translate(py_ast)
        return

    #@staticmethod
    #def parse(s):
    #    and_ = pp.Keyword('AND')
    #    pred = ident
    #    pred_list = pred + pp.ZeroOrMore(and_ + pred)
    #    return


# format:
#   return value = 0, 0
#   rv_u0 = 10, 10
#   rv_s0 = 1, 1
#   rv_s1 = 1, 1
#   rv_s2 = (iv_s2+1), 92058
#   ...
#########################################
# new implementaiton, treats outputs
# as any other constraints, similar to
# PathPred
##########################################
class OutputVals():

    def __init__(self, s_):
        s = s_[0]
        # remove everything after comma, i.e., the concrete values
        # Assume the string to be multiline (re.M) and do it for every line
        s = re.sub(r',.*$', r'', s, flags=re.M)
        # remove return value
        s = re.sub(r'return value.*$', r'', s, flags=re.M)
        # change assignment '=' to equality constraint '=='
        s = s.replace('=', '==')
        # cleanup
        s = s.strip()
        # and all constraints now
        s = s.replace('\n', ' and ')
        # TODO: removing all (double) and (int) conversions
        # Handle it better by using an explicit conversion call?
        s = s.replace('(double)', '')
        s = s.replace('(int)', '')
        self.py_str = s
        #############
        # TODO: below is not being used. ast conversion is done at the end
        # But its good for incremental error check, so let it stay for the time
        # being!
        # ###########
        try:
            self.py_ast = ast.parse(s)
        except:
            print s_[0], '\n########', s
            raise err.Fatal('parsing failure')
        return
#########################################
# older implementaiton, did special
# handling  as required by the py2z3
#########################################
#class OutputVals():
#    def __init__(self, s_):
#        s = s_[0]
#        # remove everything after comma, i.e., the concrete values
#        # Assume the string to be multiline (re.M) and do it for every line
#        s = re.sub(r',.*$', r'', s, flags=re.M)
#        # remove return value
#        s = re.sub(r'return value.*$', r'', s, flags=re.M)
#        # cleanup
#        s = s.strip()
#        # split into multiple lines
#        s_list = s.split('\n')
#        self.py_ast_list = []
#        #try:
#        for op_str in s_list:
#            lhs, rhs = op_str.split('=')
#            self.py_ast_list.append((lhs.strip(), ast.parse(rhs.strip())))
#        #except:
#        #    print s_[0], '\n########', s
#        #    err.Fatal('parsing failure')
#        return


# format:
#   iv_ci = -191722;
#   iv_s0 = -206734;
#   iv_s1 = -98109;
#   ...
class OtherInputVals():
    def __init__(self, s_):
        s = s_[0]
        # delete everything after =, including =
        # do this for every line (re.M)
        s = re.sub(r'=.*', r'', s, flags=re.M)
        # split into multiple lines
        s_list = s.split('\n')
        self.var_list = s_list
        return


# format:
# input = 1;
# input[0].input_arr = 1;
# input[0].state_arr = 4;
# input[0].x_arr = 1;
# ret_val = 1;
# ret_val[0].state_arr = 4;
# ret_val[0].output_arr = 1;
# ...
class Dimensions():
    def __init__(self, s_):
        s = s_[0]
        s = s.replace(';', '')
        s = s.strip()
        s_list = s.split('\n')
        # dim_def_list: [(k0, d0),..., (kn, dn) ]
        dim_def_list = map(lambda x: x.split('='), s_list)
        self.dim_def_dict = {k.strip(): int(d) for (k, d) in dim_def_list}
        return


#def parse_path():
#    USCORE = pp.Literal("_")
#    a2z = pp.Word(pp.alphas)
#    integer = pp.Word(pp.nums)
#
#    sat_cons = pp.Literal('+')
#    unsat_cons = pp.Literal('-')
#    sat_unsat_cons = (plus | minus)
#    line_num = integer
#    or_cons = a2z
#    and_cons = USCORE + integer
#    times = pp.Literal('x') + integer
#    # [+-][0-9][_[0-9] | [a-z]]x[0-9]
#
#    path_cons = sat_unsat_cons + line_num + pp.Optional(and_cons | or_cons) + pp.Optional(times)
#    path_cons_list = pp.OneOrmore(path_cons)

def parse_trace(data):

    # lexer rules
    TC = pp.Keyword('TEST CASE').suppress()
    DIM = pp.Keyword('Dimensions').suppress()
    OIV = pp.Keyword('Other input values').suppress()
    RES = pp.Keyword('Result').suppress()
    PC = pp.Keyword('Path Covered').suppress()
    PPFC = pp.Keyword('Path Predicate for case').suppress()
    SPPFC = pp.Keyword('Simplified Path Predicate for case').suppress()
    OVFC = pp.Keyword('Output Values for case').suppress()
    #SYMCON = pp.Keyword('(Symbolic,Concrete).suppress()').suppress()
    EX1 = pp.Keyword('to explore negation deepest unexplored condition of predicate').suppress()
    EX2 = pp.Keyword('Path Predicate Prefix to solve').suppress()

    # Grammar

    EOF = pp.StringEnd()
    #headings_list = [TC, DIM, OIV, RES, PC, PPFC, SPPFC, OVFC, EX1, EX2]
    #mf_hl = pp.MatchFirst(headings_list)
    #heading2idx_dict = {E: idx for idx, E in enumerate(headings_list)}

    # sections [in reverse order]
#    explores = EX1 + COMMA + EX2 + COLON + (pp.SkipTo(TC, False) | pp.SkipTo(pp.StringEnd(), False))
#    op_vals = OVFC + pp.SkipTo(pp.LineEnd(), False).suppress() + pp.SkipTo(EX1, False)
#    simplified_path_pred = SPPFC + pp.SkipTo(pp.LineEnd(), False).suppress() + pp.SkipTo(OVFC, False)
#    path_pred = PPFC + pp.SkipTo(pp.LineEnd(), False) + pp.SkipTo(SPPFC, False)
#    path_covered = PC + COLON + pp.SkipTo(PPFC, False)
#    result = RES + COLON + pp.SkipTo(PC, False)
#    input_val = OIV + COLON + pp.SkipTo(RES, False)
#    dimension = DIM + COLON + pp.SkipTo(OIV, False)

    explores = EX1 + COMMA + EX2 + COLON \
        + (pp.SkipTo(TC, False) | pp.SkipTo(EOF, False))
    op_vals = OVFC + pp.SkipTo(pp.LineEnd(), False).suppress() \
        + (pp.SkipTo(EX1, False) | pp.SkipTo(EOF, False))
    simplified_path_pred = SPPFC + pp.SkipTo(pp.LineEnd(), False).suppress() + pp.SkipTo(OVFC, False)
    path_pred = PPFC + pp.SkipTo(pp.LineEnd(), False) + pp.SkipTo(SPPFC, False)
    path_covered = PC + COLON + pp.SkipTo(PPFC, False)
    result = RES + COLON + pp.SkipTo(PC, False)
    input_val = OIV + COLON + pp.SkipTo(RES, False)
    dimension = DIM + COLON + pp.SkipTo(OIV, False)

    simplified_path_pred.setParseAction(PathPred)
    op_vals.setParseAction(OutputVals)
    input_val.setParseAction(OtherInputVals)
    dimension.setParseAction(Dimensions)

    test_case = \
        TC + integer.suppress()            \
        + dimension                        \
        + input_val                        \
        + result.suppress()                \
        + path_covered.suppress()          \
        + path_pred.suppress()             \
        + simplified_path_pred             \
        + op_vals                          \
        + pp.Optional(explores.suppress())

    test_case.setParseAction(TestCase)
    pc_trace = pp.OneOrMore(test_case)
    #pc_trace.validate()
    # TODO: wasteful repeated parsing
    # all 'Other input values:' sections are the same for us. Just use the
    # first one. Its a waste to parse all though!
    # Same with Dimensions!
    paths = pc_trace.parseString(data, True)
    #for p in paths:
    #    print p
    solver_list = get_z3_solver_list(paths)
    solverlist_to_smt2file(solver_list)

# ##################################
# Begin the hacky functions
# ##################################


def solverlist_to_smt2file(solver_list):
    path = OUTPUT_DIR_PATH
    # 6 digit names padded with 0
    file_name = 'test{:06}.smt2'
    debug_file_name = 'test{:06}.dbg'
    for idx, solver in enumerate(solver_list):
        file_path = f.construct_path(file_name.format(idx), path)
        debug_file_path = f.construct_path(debug_file_name.format(idx), path)
        f.write_data(file_path, solver.to_smt2())
        f.write_data(debug_file_path, repr(solver))


def convert_vars_to_array():
    pass


# Coverts the parsed paths to z3 solvers
# Uses py2z3.
# This is almost surely not the best way to do things, but quite convinient
def get_z3_solver_list(paths):
    dim_def_dict = paths[0].dimensions.dim_def_dict
    e = Empty()
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
    var_name_list = ['iv_input_arr',
                     'iv_int_state_arr',
                     'iv_float_state_arr',
                     'iv_x_arr',
                     'rv_int_state_arr',
                     'rv_float_state_arr',
                     'rv_output_arr']
    e.inputs = []
    e.outputs = []
    e.states = []
    for var_name_str in var_name_list:
        v = Empty()
        # don't care about the type
        v.typStr = 'R'
        # indicate a vector
        v.subTypStr = 'V'
        v.dim = dim_def_dict[var_name_str]
        v.nameStr = var_name_str
        e.inputs.append(v)
#####################################################

    # create an empty list which py2z3 will fillup
    e.pathListZ3 = []
    #e.parsedPathList = [(paths[0][0].py_ast, paths[0][1].py_ast_list)]
    # remove special parsing of outputs
    #e.parsedpathlist = [(path.path_pred.py_ast, path.output_vals.py_ast_list) for path in paths]
    e.parsedPathList = []
    output_cons_list = []
    for path in paths:
        cons_py_str = path.path_pred.py_str + ' and ' + path.output_vals.py_str
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


def preprocess_trace(trace_file_data):
    trace_file_data = trace_file_data.replace('__controller', '')
    # replace: input[0].<name>[idx] -> name[idx]
    trace_file_data = re.sub(
        r'input\[0\]\.(?P<name>[\w]+)\[(?P<idx>[0-9]+)\]',
        r'iv_\g<name>[\g<idx>]',
        trace_file_data)

    # replace: ret_val[0].<name>[idx] -> name[idx]
    trace_file_data = re.sub(
        r'ret_val\[0\]\.(?P<name>[\w]+)\[(?P<idx>[0-9]+)\]',
        r'rv_\g<name>[\g<idx>]',
        trace_file_data)

    # now rename the arrays in the dimension section
    trace_file_data = re.sub(
        r'input\[0\]\.(?P<name>[\w]+)',
        r'iv_\g<name>',
        trace_file_data)
    trace_file_data = re.sub(
        r'ret_val\[0\]\.(?P<name>[\w]+)',
        r'rv_\g<name>',
        trace_file_data)

    return trace_file_data


def main():
    usage = 'usage: %prog <filename>'
    parser = OptionParser(usage)
    #parser.add_option('-f', '--filename', dest='filename', help='name of the file')
    (options, args) = parser.parse_args()

    #print options.filename
    #data = read_default_file()
    if not args:
        parser.error(usage)

    if not f.is_dir_empty(OUTPUT_DIR_PATH):
        raw_input('{} not empty. Empty it first.'.format(OUTPUT_DIR_PATH))
        return

    data = f.get_data(args[0])
    data = preprocess_trace(data)
    #print data
    #exit()
    parse_trace(data)

if __name__ == '__main__':
    main()
