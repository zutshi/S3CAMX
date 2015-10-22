#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sh
import time

import fileOps as f

MAX_TESTS = 3000
NUM_TESTS = 10
prog_name = 'secam.py'
filename_arg = '--filename'
ss_symex_opt = '--ss-symex'
ss_opt = '--ss-concrete'
sim_opt = '--simulate'
# choice of symex
PC = 'pathcrawler'
KLEE = 'klee'
# choice of symbolic repr of the controller
rep_opt = '--cntrl-rep'
rep = 'trace'
struct_opt = '--trace-struct'
struct = 'tree'

#'./secam.py --filename ./examples/heater_float/heater.tst --ss-symex pathcrawler'
# TODO: use fileops functions ot construct filenames!
result_dir = './regression_results/'
output_log_ext = '.log'
run_summary_log_ext = '.summary'


heater_name = 'heater'
heater_path = './examples/heater/heater.tst'

dc_name = 'dc_motor'
dc_motor_path = './examples/dc_motor/dci.tst'

tenu1_name = 'tenu_1'
tenu1_path = './examples/toy_model_10u/toy_model_10u_1.tst'

tenu2_name = 'tenu_2'
tenu2_path = './examples/toy_model_10u/toy_model_10u_2.tst'

tenu3_name = 'tenu_3'
tenu3_path = './examples/toy_model_10u/toy_model_10u_3.tst'

heat_name = 'heat'
heat_path = './examples/heat/heat.tst'

fuzzy_name = 'fuzzy_invp'
fuzzy_path = './examples/fuzzy_invp/fuzzy_invp.tst'

afc_name = 'afc_FR'
afc_path = './examples/abstractFuelControl/AbstractFuelControl_FR.tst'

spi_name = 'spi'
spi_path = './examples/spi/spi.tst'

SYMEX = True
benchmark_list = [
                  #(heater_name, heater_path),
                  #(dc_name, dc_motor_path),
                  #(tenu1_name, tenu1_path),
                  #(tenu2_name, tenu2_path),
                  #(tenu3_name, tenu3_path),
                  #(heat_name, heat_path),
                  #(fuzzy_name, fuzzy_path),
                  #(afc_name, afc_path),
                  (spi_name, spi_path)
                  ]

# (time ./secam.py ./examples/heater/heater.tst)>>./regression_results/heater.log 2>>./regression_results/heater.time

T = 0.0
time_spent_list = ''
SUCC_CTR = 0
FAIL_CTR = 0
STDOUT_DATA = ''
LAST_RESULT = None

TIME_STAMP = time.strftime("%c")


def process_stdout(msg):
    global STDOUT_DATA
    STDOUT_DATA += msg
    return


# format of t
#   time spent(s) = 0.0
def process_times(time_spent_str):
    print time_spent_str
    global time_spent_list, T
    f.append_data(run_summary_log, time_spent_str)
    time_spent_list += time_spent_str
    t_str = time_spent_str.split('=')[1].strip()
    t = float(t_str)
    T += t


def process_status_msg(msg):
    global SUCC_CTR, FAIL_CTR
    global LAST_RESULT
    if msg.startswith('Concretized'):
        LAST_RESULT = True
        SUCC_CTR += 1
        print '✓'
        f.append_data(run_summary_log, ' ✓ ')
    else:
        LAST_RESULT = False
        FAIL_CTR += 1
        print '✗'
        f.append_data(run_summary_log, ' ✗ ')


def process_stderr(msg):
    if msg.startswith('time'):
        process_times(msg)
    else:
        process_status_msg(msg)


#def main():
for benchmark in benchmark_list:
    name, path = benchmark
    print name, ':', path
    output_log = result_dir + name + output_log_ext
    run_summary_log = result_dir + name + run_summary_log_ext

    # Cleanup globals!
    T = 0.0
    time_spent_list = ''
    SUCC_CTR = 0
    FAIL_CTR = 0

    test_hdr = '{DECO}\n{deco} TEST DATE: {ts}\n{DECO}\n'.format(DECO='#'*40, deco='##', ts=TIME_STAMP)
    f.append_data(run_summary_log, test_hdr)

    #for i in range(NUM_TESTS):
    exceeded_num_runs = False
    done = False
    test_ctr = 0

    if SYMEX:
        run_description = '-- ss-symex --\n'
        arg_list = [filename_arg, path, ss_symex_opt, PC, rep_opt, rep, struct_opt, struct]
    else:
        run_description = '-- running ss-concrete --\n'
        arg_list = [filename_arg, path, ss_opt]
    print run_description
    f.append_data(run_summary_log, run_description)

    while (not done) and (not exceeded_num_runs):
        print 'RUN', test_ctr, ':',
        #sh.python(prog_name, benchmark_path, _out=output_log, _err=process_stderr)
        # ./secam.py --filename ./examples/heater/heater.tst --ss-symex klee
        sh.python(prog_name, *arg_list, _out=process_stdout, _err=process_stderr)
        f.append_data(output_log, STDOUT_DATA)
        STDOUT_DATA = ''

        test_ctr = test_ctr+1 if LAST_RESULT else test_ctr
        done = NUM_TESTS == test_ctr
        exceeded_num_runs = test_ctr > MAX_TESTS

    avg_time_str = 'average time = {}\n'.format(T/NUM_TESTS)
    success_str = 'successfull runs = {}\n'.format(SUCC_CTR)
    fail_str = 'failures = {}\n'.format(FAIL_CTR)
    # time_summary = ''.join(time_spent_list) \
    time_summary = \
        'total_time_taken = {}\n'.format(T) \
        + avg_time_str \
        + success_str  \
        + fail_str     \
        + '\n'

    f.append_data(run_summary_log, time_summary)

#if __name__ == '__main__':
#    main()
