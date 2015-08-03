import pyparsing as pp
import ast
import re
from blessings import Terminal


import fileOps as f
import err

term = Terminal()


DEFAULTFILENAME = './trace/controller'
# global tokens
SEMI = pp.Literal(";").suppress()
COLON = pp.Literal(":").suppress()
COMMA = pp.Literal(",").suppress()
PLUS = pp.Literal("+")
MINUS = pp.Literal("-")
UNDERSCORE = pp.Literal('_')
#LPAREN = pp.Literal("(").suppress()
#RPAREN = pp.Literal(")").suppress()


integer = pp.Word(pp.nums)
alpha = pp.alphas
#IDENT = pp.Word(pp.srange("[a-zA-Z_]"), pp.srange("[a-zA-Z0-9_]"))
ident = pp.Word(pp.alphanums+"_")


def read_default_file():
    fileName = DEFAULTFILENAME
    data = f.get_data(fileName)
    return data


# TODO: removing all (double) and (int) conversions
# Handle it better by using an explicit conversion call?
def remove_typecasts(s):
    s = s.replace('(double)', '')
    s = s.replace('(int)', '')
    s = s.replace('(unsigned char)', '')
    return s


class TestCase(object):
    def __init__(self, s):
        self.dimensions = s[0]
        self.input_vals = s[1]
        self.path_pred = s[2]
        self.simplified_path_pred = s[3]
        self.output_vals = s[4]
        return


def print_test_case(s):
    with term.location():
        print 'parsing test case:', s[0]
    return


# format:
#   heat_controller.c: +17 0<3   (iteration of loop line 17)
#   heat_controller.c: +17 1<3   (iteration of loop line 17)
#   heat_controller.c: +17 2<3   (iteration of loop line 17)
#   heat_controller.c: -17 3>=3   (exit loop line 17)
#   ...
#    ###########
#    operators present in a trace file: replaced to
#    =      :   ==
#    <>     :   !=
#    >=     :   not replaced
#    =<     :   >=
class PathPred():

    def __init__(self, s_):
        s = s_[0]
        #s = s.replace('\n', ' ')
        # prevent matching of '>=' and '=<'...
        # usual replace fails: s = s.replace('=', '==')
        # (?<!...): negative look behind for '>'
        # (?!...): negative look forward for '<'
        s = re.sub(r'(?<!>)=(?!<)', r'==', s)
        #print s
        s = s.replace('<>', '!=')
        #print s
        s = s.replace(r'=<', r'<=')
        s = remove_typecasts(s)
        #print s
        stmt_list = s.strip().split('\n')
        stmt_list = [stmt.split(' ') for stmt in stmt_list]

        ordered_id_cons_gen = ((stmt[1], stmt[2]) for stmt in stmt_list)
        #self.ordered_hashID_parsedID_cons_list \
        #    = [(hash(ID), self.cond_parser(ID), cons) for ID, cons in ordered_id_cons_gen]

        self.ordered_parsedID_cons_list \
            = [(self.cond_parser(ID), cons) for ID, cons in ordered_id_cons_gen]

        #lst = []
        #prev_pred_ID = []
        #for ID, cons in ordered_id_cons_gen:
        #    pred_ID = self.cond_parser(ID)

        #for i in ordered_parsedId_cons_list:
        #    print i

        # debug prints...
        #for i in stmt_list:
        #    print i[0], '\t', i[1], '\t', i[2]
        #    print self.cond_parser(i[1])

        #self.py_str = cons
        #############
        # TODO: below is not being used. Ast conversion is done at the end
        # But its good for incremental error check, so let it stay for the time
        # being!
        # ###########
        # TODO: remove try block for efficiency
        #       current purpose is to improve error reporting
        try:
            # 'Ands' all constraints (even the ones which should be OR-ed) and
            # checks if they can be parsed by the python ast parser. Just a
            # sanity check!!
            pred_stmt_gen = (('(' + stmt[2] + ')') for stmt in stmt_list)
            cons = reduce(lambda x, y: '{} and {}'.format(x, y), pred_stmt_gen)
            ast.parse(cons)
        except:
            print '='*100
            print s_[0], '\n########', cons
            raise err.Fatal('python ast parsing failure')
        #self.z3_cons = py2z3.translate(py_ast)
        return

    def cond_parser(self, s):
        # actually, pathcrawler's outputs are ambiguous!
        # current observation:
        #   sub_cond_and is for sure 'and'
        #   sub_cond_or can be either 'or' or 'and'
        sub_cond_and = UNDERSCORE.suppress() + integer
        sub_cond_or = pp.Word(pp.alphas)

        sub_cond_and.setParseAction(lambda s: s[0])
        sub_cond_or.setParseAction(lambda s: s[0])

        sub_cond = sub_cond_or | sub_cond_and
        pred_cond = (PLUS | MINUS) + integer

        # e.g. '+' + '23'
        # e.g. '-' + '23'
        pred_cond.setParseAction(lambda s: int(s[0] + s[1]))

        cond = pred_cond + pp.Optional(sub_cond, default='')

        # e.g. (-23, '_2')
        # e.g. (-23, 'a')
        # e.g. (-23, '')
        cond.setParseAction(lambda s: (s[0], s[1]))
        # parse and get the token list only. Ignore the empty dict
        parsed_obj = cond.parseString(s, parseAll=True)
        # parsed_obj behaves as a list
        # can also used parsed_obj.asList()[0]
        return parsed_obj[0]


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
class SimplifiedPathPred():
    ctr = 0

    def __init__(self, s_):
        SimplifiedPathPred.ctr += 1
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
        s = remove_typecasts(s)
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
# SimplifiedPathPred
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
        s = remove_typecasts(s)
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

        # sanity check to report user friendly error if dimension section is empty
        non_blank_defs = 0
        for df in s_list:
            if df != '':
                non_blank_defs += 1
        if non_blank_defs == 0:
            raise err.Fatal('dim_def_list is empty!')
        else:
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
    # no speedup observed usin gpackrat!
    #pp.ParserElement.enablePackrat()

    # lexer rules
    TC = pp.Keyword('TEST CASE').suppress() + integer
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
    path_pred = PPFC + pp.SkipTo(pp.LineEnd(), False).suppress() + pp.SkipTo(SPPFC, False)
    path_covered = PC + COLON + pp.SkipTo(PPFC, False)
    result = RES + COLON + pp.SkipTo(PC, False)
    input_val = OIV + COLON + pp.SkipTo(RES, False)
    dimension = DIM + COLON + pp.SkipTo(OIV, False)

    simplified_path_pred.setParseAction(SimplifiedPathPred)
    path_pred.setParseAction(PathPred)
    op_vals.setParseAction(OutputVals)
    input_val.setParseAction(OtherInputVals)
    dimension.setParseAction(Dimensions)
    TC.setParseAction(print_test_case)

    #TC + integer.suppress()            \
    test_case = \
        TC.suppress()                                 \
        + dimension                        \
        + input_val                        \
        + result.suppress()                \
        + path_covered.suppress()          \
        + path_pred                        \
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
    paths = pc_trace.parseString(data, parseAll=True)
    #for p in paths:
    #    print p
    return paths


def trace_to_paths(trace):
    return parse_trace(preprocess_trace(trace))


def trace_file_to_paths(trace_file):
    return parse_trace(preprocess_trace(f.get_data(trace_file)))


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
