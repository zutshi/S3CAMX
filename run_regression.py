#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sh

import fileOps as f

NUM_TESTS = 100
prog_name = 'secam.py'
filename_arg = '--filename'
ss_symex_opt = '--ss-symex'
ss_opt = '--ss-concrete'
sim_opt = '--simulate'
# choice of symex
PC = 'pathcrawler'
KLEE = 'klee'

#'./secam.py --filename ./examples/heater_float/heater.tst --ss-symex pathcrawler'

benchmark_path = './examples/heater_float/heater.tst'
output_log = './regression_results/heater_float.log'
run_summary_log = './regression_results/heater_float.summary'

# (time ./secam.py ./examples/heater/heater.tst)>>./regression_results/heater.log 2>>./regression_results/heater.time

T = 0.0
time_spent_list = ''
SUCC_CTR = 0
FAIL_CTR = 0
STDOUT_DATA = ''


def process_stdout(msg):
    global STDOUT_DATA
    STDOUT_DATA += msg
    return


# format of t
#   time spent(s) = 0.0
def process_times(time_spent_str):
    global time_spent_list, T
    time_spent_list += time_spent_str
    t_str = time_spent_str.split('=')[1].strip()
    t = float(t_str)
    T += t


def process_status_msg(msg):
    global SUCC_CTR, FAIL_CTR
    if msg.startswith('Concretized'):
        SUCC_CTR += 1
        print '✓'
    else:
        FAIL_CTR += 1
        print '✗'


def process_stderr(msg):
    if msg.startswith('time'):
        process_times(msg)
    else:
        process_status_msg(msg)

for i in range(NUM_TESTS):
    print 'RUN', i, ':',
    #sh.python(prog_name, benchmark_path, _out=output_log, _err=process_stderr)
    # ./secam.py --filename ./examples/heater/heater.tst --ss-symex klee
    arg_list = [filename_arg, benchmark_path, ss_symex_opt, PC]
    sh.python(prog_name, *arg_list, _out=process_stdout, _err=process_stderr)
    f.append_data(output_log, STDOUT_DATA)
    STDOUT_DATA = ''

avg_time_str = 'average time = {}\n'.format(T/NUM_TESTS)
success_str = 'successfull runs = {}\n'.format(SUCC_CTR)
fail_str = 'failures = {}\n'.format(FAIL_CTR)
time_summary = ''.join(time_spent_list) \
    + 'total_time_taken = {}\n'.format(T) \
    + avg_time_str \
    + success_str  \
    + fail_str     \
    + '\n'

f.append_data(run_summary_log, time_summary)
