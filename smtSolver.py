#!/usr/bin/python
# -*- coding: utf-8 -*-

import fractions as fr
import logging
import z3

import c_info
import err
import utils as U

logger = logging.getLogger(__name__)

INT_SIZE = c_info.sizeof_int()  # bytes
BYTE = 8  # bits
INT_SIZE_BITS = INT_SIZE * BYTE
HEX_BASE = 16
BIN_BASE = 2
REAL2FLOAT_PRECISION = 6

def smt_solver_factory(solver_name):
    if solver_name == 'z3':
        return Z()
    else:
        raise err.Fatal('solver name not recognized: {}'.format(solver_name))


class Solver(object):

    pass


class Z(Solver):

    def __init__(self):

        # self.solver = z3.Solver()

        self.TRUE = z3.BoolVal(True)
        self.FALSE = z3.BoolVal(False)

        return

    def And(self, *args):
        return z3.And(*args)

    def ArraySort(self, *args):
        return z3.ArraySort(*args)

    def BitVecSort(self, *args):
        return z3.BitVecSort(*args)

    def Function(self, *args):
        return z3.Function(*args)

    def Array(self, *args):
        return z3.Array(*args)

    def smt2_2_constraints(self, s, decls):
        return z3.parse_smt2_string(s, decls=decls)

    def SAT(self, c):
        s = z3.Solver()
        s.add(c)
        return s.check() == z3.sat

    def equal(self, x, val):
        cons_list = []
        if isinstance(x, z3.ExprRef):
            if x.sort() == z3.ArraySort(z3.BitVecSort(32), z3.BitVecSort(8)):
                for i in range(len(val)):
                    c_equal = z3.Concat(x[INT_SIZE * i + 3], x[INT_SIZE * i + 2],
                                        x[INT_SIZE * i + 1], x[INT_SIZE * i + 0]) \
                        == val[i]
                    cons_list.append(c_equal)
            elif x.sort() == z3.RealSort():
                c_equal = x == val
                cons_list.append(c_equal)
            else:
                raise err.Fatal('unhandled sort x: {}'.format(x.sort()))
        elif isinstance(x, list):
            cons_list = map((lambda x, c: x == c), x, val)
        else:
            raise err.Fatal('unhandled type: {}'.format(type(x)))
        return z3.And(cons_list)

    def RealVector(self, s_str, length):
        return z3.RealVector(s_str, length)

    def IntVector(self, s_str, length):
        return z3.IntVector(s_str, length)

    def BitVecArray(self, s_str):
        return z3.Array(s_str, z3.BitVecSort(32), z3.BitVecSort(8))

    # TODO: depends on interval constraints api...is this ok?
    def ic2smt(self, ic, x):
        cons_list = []
        if isinstance(x, z3.ExprRef):
            if x.sort() == z3.ArraySort(z3.BitVecSort(32), z3.BitVecSort(8)):
                for i in range(ic.dim):
                    c_upper_bound = z3.Concat(x[INT_SIZE * i + 3],
                                              x[INT_SIZE * i + 2],
                                              x[INT_SIZE * i + 1],
                                              x[INT_SIZE * i + 0]) \
                                    <= ic.h[i]
                    c_lower_bound = z3.Concat(x[INT_SIZE * i + 3],
                                              x[INT_SIZE * i + 2],
                                              x[INT_SIZE * i + 1],
                                              x[INT_SIZE * i + 0]) \
                                    >= ic.l[i]
                    cons_list.append(c_upper_bound)
                    cons_list.append(c_lower_bound)
            else:
                raise err.Fatal('unknown sort: {}'.format(x.sort()))
        elif isinstance(x, list):
            cons_list = map((lambda x, c: x <= c), x, ic.h)\
                      + map((lambda x, c: x >= c), x, ic.l)
        else:
            raise err.Fatal('unhandled type: {}'.format(type(x)))
        return z3.And(cons_list)


    # TODO: fix the function call!

    def substitute(
        self,
        C,
        v,
        v_,
        ):
        return z3.substitute(C, (v, v_))

    def simplify(self, *args):
        return z3.simplify(*args)

    def solver(self):
        return z3.Solver()

    def sample_bvArray(
        self,
        surface,
        num_points,
        outputVarList,
        var2dim_dict,
        var2sample_list,
        minDist,
        ):

        # minDist = 1

        surface2Sample = surface
        samplesDict = {}

        # initialize samples dict

        for outputVar in outputVarList:
            samplesDict[str(outputVar)] = []

        s = z3.Solver()

        # normCons = z3.BoolVal(True)

        normCons = []

    #  print '---------------- sampling ----------------'
    #  print surface2Sample
    #  print '------------------------------------------'

        s.add(surface2Sample)
        for i in range(num_points):

            # print U.decorate(str(normCons))

            s.add(normCons)

            # print U.decorate(str(s))
            # ##!!##logger.debug(str(s))

            if s.check() == z3.sat:
                model = s.model()
                sample_dict = model2var_bvArray(model, outputVarList, var2dim_dict)
                for k in samplesDict:
                    samplesDict[k].append(sample_dict[k])

                # get norm constraints for next iteration
                var_val2sample_list = [(k, sample_dict[str(k)]) for k in
                                       var2sample_list]
                normCons = get_norm_cons_bvArray(var_val2sample_list, var2dim_dict,
                                       minDist)
            else:
                if i == 0:

                    # ##!!##logger.debug('surface is UNSAT')
                    # # ##!!##logger.debug('unsat core:\n{}'.format(s.unsat_core))

                    return {}
                else:

                    # ##!!##logger.debug('!!!!!!!!!! no more samples possible !!!!!!!!!!!')
                    # ##!!##logger.debug('max samples: {}'.format(i))

                    print 'max samples: {}'.format(i)
                    break

        return samplesDict

    def sample_scalars(
        self,
        surface,
        num_points,
        var2sample_list,
        minDist,
        ):

        # minDist = 1

        num_actual_samples = 0
        surface2Sample = surface
        samplesDict = {}

        # initialize samples dict

        #for outputVar in varList:
        #    samplesDict[outputVar.hash()] = []

        s = z3.Solver()

        # normCons = z3.BoolVal(True)

        normCons = []

    #  print '---------------- sampling ----------------'
    #  print surface2Sample
    #  print '------------------------------------------'

        s.add(surface2Sample)
        for i in range(num_points):

            # print U.decorate(str(normCons))

            s.add(normCons)

            #print U.decorate(str(s))
            # ##!!##logger.debug(str(s))

            if s.check() == z3.sat:
                num_actual_samples += 1
                model = s.model()
                sample_dict = model2var_scalar(model)
                #for k, d in samplesDict.iteritems():
                #    d.append(sample_dict[k])
                for var_hash, sample in sample_dict.iteritems():
                    samplesDict[var_hash] = samplesDict.get(var_hash, []) + [sample]

                # get norm constraints for next iteration
                var_val2sample_list = [(k, sample_dict[k.hash()]) for k in
                                       var2sample_list]
                normCons = get_norm_cons_scalar(var_val2sample_list, minDist)
            else:
                if i == 0:

                    # ##!!##logger.debug('surface is UNSAT')
                    # # ##!!##logger.debug('unsat core:\n{}'.format(s.unsat_core))

                    return {}, 0
                else:

                    # ##!!##logger.debug('!!!!!!!!!! no more samples possible !!!!!!!!!!!')
                    # ##!!##logger.debug('max samples: {}'.format(i))

                    print 'max samples: {}'.format(i)
                    break

        return samplesDict, num_actual_samples

    def sample_realVec(
        self,
        surface,
        num_points,
        outputVarList,
        var2dim_dict,
        var2sample_list,
        minDist,
        ):

        # minDist = 1

        surface2Sample = surface
        samplesDict = {}

        # initialize samples dict

        for outputVar in outputVarList:
            samplesDict[str(outputVar)] = []

        s = z3.Solver()

        # normCons = z3.BoolVal(True)

        normCons = []

    #  print '---------------- sampling ----------------'
    #  print surface2Sample
    #  print '------------------------------------------'

        s.add(surface2Sample)
        for i in range(num_points):

            # print U.decorate(str(normCons))

            s.add(normCons)

            #print U.decorate(str(s))
            # ##!!##logger.debug(str(s))

            if s.check() == z3.sat:
                model = s.model()
                sample_dict = model2var_realVec(model, outputVarList, var2dim_dict)
                for k, d in samplesDict.iteritems():
                    d.append(sample_dict[k])

                # get norm constraints for next iteration
                var_val2sample_list = [(k, sample_dict[str(k)]) for k in
                                       var2sample_list]
                normCons = get_norm_cons_realVec(var_val2sample_list, var2dim_dict,
                                       minDist)
            else:
                if i == 0:

                    # ##!!##logger.debug('surface is UNSAT')
                    # # ##!!##logger.debug('unsat core:\n{}'.format(s.unsat_core))

                    return {}
                else:

                    # ##!!##logger.debug('!!!!!!!!!! no more samples possible !!!!!!!!!!!')
                    # ##!!##logger.debug('max samples: {}'.format(i))

                    print 'max samples: {}'.format(i)
                    break

        return samplesDict


def model2var_bvArray(model, outputVarList, var2dim_dict):
    sample_dict = {}
    for output_arr in outputVarList:
        n = var2dim_dict[str(output_arr)]
        num_elements = n * INT_SIZE
        x_arr = []
        a = model[output_arr]
        x_packed = [0 for i in range(num_elements)]
        if num_elements > a.num_entries():

            # raise err.Fatal('something fishy? Must investigate!')

            recorded_idx_set = set()
            for i in range(a.num_entries()):
                e = a.entry(i)
                idx = e.as_list()[0].as_long()
                val = e.as_list()[1].as_long()
                x_packed[idx] = val
                recorded_idx_set.add(idx)

            missing_idx_set = set(range(num_elements)) - recorded_idx_set

            for idx in missing_idx_set:
                x_packed[idx] = a.else_value().as_long()
        elif num_elements < a.num_entries():
            raise err.Fatal('not possible!')
        else:
            for i in range(num_elements):
                x_packed[a.as_list()[i][0].as_long()] = \
                    a.as_list()[i][1].as_long()

        for i in range(n):
            x_packed_i_reversed = x_packed[i * INT_SIZE:(i + 1) * INT_SIZE]
            x_packed_i_reversed.reverse()
            x_bin_list = [bin(j)[2:].zfill(BYTE) for j in x_packed_i_reversed]
            x_bin_str = '0b' + ''.join(x_bin_list)
            x_int = int(x_bin_str, BIN_BASE)
            if x_bin_str[2:][0] == '1':
                x_int = -(BIN_BASE ** INT_SIZE_BITS - x_int)
            x_arr.append(x_int)
        sample_dict[str(output_arr)] = x_arr
    return sample_dict


def z3val2pyval(val):
    if val.is_real():
        return z3real2pyfloat(val)
    # TODO: what is z3.is_int_value() ?
    # from the docs, seem more appropriate. But, an analogoue for reals does
    # not exist. Confusing....
    elif val.is_int():
        return z3int2pyint(val)
    else:
        raise err.Fatal('unhandled z3 val type')


def z3real2pyfloat(r):
    ################# slow!
    #n = float(r.numerator().as_long())
    #d = float(r.denominator().as_long())
    #return n/d
    ################# optimized, a magnitude faster
    return float(r.as_decimal(REAL2FLOAT_PRECISION).replace('?', ''))


def z3int2pyint(z):
    return z.as_long()


def pyval2z3val(val):
    if type(val) is float:
        return z3.RealVal(val)
    elif type(val) is int:
        return z3.IntVal(val)
    else:
        raise err.Fatal('unhandled python val type!')


# converts z3 Reals to floats!!
# Precision is lost of course.
def model2var_realVec(model, outputVarList, var2dim_dict):
    sample_dict = {}
    for output_arr in outputVarList:
        num_elements = var2dim_dict[str(output_arr)]
        x_arr = [model[output_arr[i]] for i in range(num_elements)]
        # TODO: replace all vars which have no models with 0
        # Is this handling correct?
        x_arr = [z3.RealVal(0) if x is None else x for x in x_arr]
        x_arr = [z3val2pyval(x) for x in x_arr]
        #print str(output_arr)
        #print x_arr
        sample_dict[str(output_arr)] = x_arr
    #print sample_dict
    #exit()
    return sample_dict


# converts z3 Reals to floats!!
# Precision is lost of course.
# UNUSED!!
def model2var_scalar_withvarlist(model, varList):
    sample_dict = {}
    for var in varList:
        # TODO: annoying computation at every step!!
        py_zero = 0.0 if var.is_real() else 0
        var_val = model[var]
        # TODO: replace all vars which have no models with 0
        # Is this handling correct?
        var_val = py_zero if var_val is None else z3val2pyval(var_val)
        sample_dict[var.hash()] = var_val
    return sample_dict


# converts z3 Reals to floats!!
# Precision is lost of course.
# IMPROVED! Does not use varlist
def model2var_scalar(model):
    sample_dict = {}
    # NOTE: var obtained from model is not var. It is actually of type
    # FuncDeclRef. But, it seems to have the same hash as the original
    # variable! XXX: UNCONFIRMED!
    for var in model:
        var_val = model[var]
        # TODO: annoying computation at every step!!
        py_zero = 0.0 if var_val.is_real() else 0
        var_val = z3val2pyval(var_val)
        sample_dict[var.hash()] = var_val
    return sample_dict


# Objective is to sample control inputs (u) uniformly
def get_norm_cons_bvArray(varValList, var2dim_dict, minDist):
    normConsList = []
    for (var, val) in varValList:
        n = var2dim_dict[str(var)]
        for i in range(n):
            c_upper_bound = -z3.Concat(var[INT_SIZE * i + 3], var[INT_SIZE * i
                                       + 2], var[INT_SIZE * i + 1],
                                       var[INT_SIZE * i + 0]) + val[i] \
                >= minDist
            c_lower_bound = z3.Concat(var[INT_SIZE * i + 3], var[INT_SIZE * i
                                      + 2], var[INT_SIZE * i + 1],
                                      var[INT_SIZE * i + 0]) - val[i] \
                >= minDist

            # c_ne = z3.Concat(var[INT_SIZE * i + 3],
            #                 var[INT_SIZE * i + 2],
            #                 var[INT_SIZE * i + 1],
            #                 var[INT_SIZE * i + 0])\
            #                 != val[i]

            normConsList.append(c_upper_bound)
            normConsList.append(c_lower_bound)

            # normConsList.append(c_ne)

    # return (c_ne)
    return z3.Or(*normConsList)


def get_norm_cons_realVec(varValList, var2dim_dict, min_dist):
    normConsList = []
    for (var, element_list) in varValList:
        n = var2dim_dict[str(var)]
        c_upper_bound = [var[i] <= element_list[i] - min_dist for i in range(n)]
        c_lower_bound = [var[i] >= element_list[i] + min_dist for i in range(n)]
        normConsList += c_upper_bound + c_lower_bound

    return z3.Or(*normConsList)

def get_norm_cons_scalar(varValList, min_dist):
    c_upper_bound_list = [var <= var_val - min_dist for (var, var_val) in varValList]
    c_lower_bound_list = [var >= var_val + min_dist for (var, var_val) in varValList]
    normConsList = c_upper_bound_list + c_lower_bound_list
    return z3.Or(*normConsList)
