#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
run_regression.py
------------------
A script provided for convinient evaluation of S3CAMX and S3CAM on a
given system. Sequentially evaluates the systems registered in
'benchmark_list' defined below. Each system is analyzed using S3CAMX
or S3CAM as chosen at the prompt for 'NUM_TESTS=10' times. Also
provided is an option is to run ./secam.py in order to randomly
simulate a system. This reproduces the DoD metric using 100,000 random
simulations, apart from the AFC system for which 100 simulataions were
used.

For each system, the results are stored in './regression_results/'
using the below format:

    <system_name>.<analyses_engine>.summary
        Contains a concise summary of the results.

    <system_name>.<analyses_engine>.log
        Contains the complete output log in case debugging is
        required.

    analyses_engine: can be either S3CAM, S3CAMX (S3CAM + symbolic
    execution) or SIM (random simulations).

    e.g. For the heater system, running S3CAMX will produce the below
    two files
        heater.S3CAM.summary, heater.S3CAMX.log

The files are appended (and not overwritten) after each run. Also,
the write is unbuffered, and happens as soon as the result is computed
without waiting for the entire script to terminate. This ensures
partial recovery in case of sudden interruptions.

Multiple copies of run_regression.py can be run simultaneously without
any issues as long as the combination of system and analyses being run
is not exactly the same. Otherwise, the output files will get
incoherent due to simulataneous writes.
'''

import sh
import time

import fileOps as f

TIMEOUT = 3600
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
simple_output = '--basic-visual'

print '''{0}
Make sure to set paths before running S3CAMX!
[refer to readme for more details]
{0}'''.format('#'*20)

user_ip = raw_input('Run S3CAMX[X] or S3CAM[C] or Random Testing[S]? ')
if user_ip.lower() == 'x':
    RUN_MODE = 'S3CAMX'
elif user_ip.lower() == 'c':
    RUN_MODE = 'S3CAM'
elif user_ip.lower() == 's':
    RUN_MODE = 'SIM'
else:
    print 'Did not not understand input!'
    exit()

#'./secam.py --filename ./examples/heater_float/heater.tst --ss-symex pathcrawler'
# TODO: use fileops functions ot construct filenames!
result_dir = './regression_results/'
output_log_ext = '.log'
run_summary_log_ext = '.summary'


heater_name = 'heater'
heater_path = './examples/heater/heater.tst'

dc_name = 'dc_motor'
dc_motor_path = './examples/dc_motor/dci.tst'

mrs1_name = 'mrs1'
mrs1_path = './examples/mrs/mrs1.tst'

mrs2_name = 'mrs2'
mrs2_path = './examples/mrs/mrs2.tst'

mrs3_name = 'mrs3'
mrs3_path = './examples/mrs/mrs3.tst'

heat_name = 'heat'
heat_path = './examples/heat/heat.tst'

fuzzy_name = 'fuzzy_invp'
fuzzy_path = './examples/fuzzy_invp/fuzzy_invp.tst'

afc_name = 'afc_FR'
afc_path = './examples/abstractFuelControl/AbstractFuelControl_FR.tst'

spi1_name = 'spi1'
spi1_path = './examples/spi/spi1.tst'

spi2_name = 'spi2'
spi2_path = './examples/spi/spi2.tst'

spi3_name = 'spi3'
spi3_path = './examples/spi/spi3.tst'

# standby example till ci is fixed to like pi in --ss-concrete mode
spi_name = 'spi_plant'
spi_path = './examples/spi_plant/spi.tst'

benchmark_list = [
                  (heater_name, heater_path),
                  (dc_name, dc_motor_path),
                  (mrs1_name, mrs1_path),
                  (mrs2_name, mrs2_path),
                  (mrs3_name, mrs3_path),
                  (heat_name, heat_path),
                  (fuzzy_name, fuzzy_path),
                  (spi1_name, spi1_path),
                  (spi2_name, spi2_path),
                  (spi3_name, spi3_path),
                  (afc_name, afc_path),
                  ]

# (time ./secam.py ./examples/heater/heater.tst)>>./regression_results/heater.log 2>>./regression_results/heater.time

T = 0.0
time_spent_list = ''
SUCC_CTR = 0
FAIL_CTR = 0
STDOUT_DATA = ''
LAST_RESULT = None
TIMEOUT_FLAG = False

TIME_STAMP = time.strftime("%c")


def process_stdout(msg):
    global STDOUT_DATA
    STDOUT_DATA += msg
    return


# format of t
#   time spent(s) = 0.0
def process_times(time_spent_str):
    #print time_spent_str
    global time_spent_list, T
    f.append_data(run_summary_log, '\n\t'+time_spent_str[:-1])
    time_spent_list += time_spent_str
    t_str = time_spent_str.split('=')[1].strip()
    t = float(t_str)
    T += t


def process_status_msg(msg):
    global SUCC_CTR, FAIL_CTR, LAST_RESULT
    if msg.startswith('Concretized'):
        LAST_RESULT = True
        SUCC_CTR += 1
        #print '✓'
        #print 'sub run ✓'
        #f.append_data(run_summary_log, ' ✓ ')
    else:
        LAST_RESULT = False
        FAIL_CTR += 1
        #print 'sub run ✗ '
        #f.append_data(run_summary_log, ' ✗ ')


def process_stderr(msg):
    if msg.startswith('time'):
        process_times(msg)
    else:
        process_status_msg(msg)


#def main():
for benchmark in benchmark_list:
    name, path = benchmark
    print name, ':', path
    output_log = result_dir + name + '.' + RUN_MODE + output_log_ext
    run_summary_log = result_dir + name + '.' + RUN_MODE + run_summary_log_ext

    # Cleanup globals!
    T = 0.0
    time_spent_list = ''
    SUCC_CTR = 0
    FAIL_CTR = 0

    test_hdr = '\n{DECO}\n{deco} TEST DATE: {ts}\n{DECO}\n'.format(DECO='#'*40, deco='##', ts=TIME_STAMP)
    f.append_data(run_summary_log, test_hdr)

    #for i in range(NUM_TESTS):
    #exceeded_num_runs = False

    if RUN_MODE == 'S3CAMX':
        run_description = '-- Running S3CAMX: ss-symex --\n'
        arg_list = [filename_arg, path, ss_symex_opt, PC, rep_opt, rep, struct_opt, struct]
    elif RUN_MODE == 'S3CAM':
        run_description = '-- Running S3CAM: ss-concrete --\n'
        arg_list = [filename_arg, path, ss_opt]
    elif RUN_MODE == 'SIM':
        global OUTPUT_DATA
        run_description = '-- Running Rand Simulations: --simulate --\n'
        if name == 'afc_FR':
            num_sims = '100'
        else:
            num_sims = '100000'
        arg_list = [filename_arg, path, sim_opt, num_sims, simple_output]

        #rs_output_log = '{}{}.random_sim'.format(result_dir, name)
        rs_output_log = run_summary_log
        #rs_err_log = '{}{}.random_sim_err'.format(result_dir, name)
        print run_description
        #sh.python(prog_name, *arg_list, _out=rs_output_log, _err=rs_err_log)
        sh.python(prog_name, *arg_list, _out=rs_output_log, _err_to_out=True)
        # Could've used the below &2 > &1 redirection. but wasn't aware earlier
        # sh.python(prog_name, *arg_list, _out=rs_output_log, _err_to_out=True)
        #f.append_data(rs_output_log, f.get_data(rs_err_log))
        continue

    print run_description
    f.append_data(run_summary_log, run_description)

    done = False
    test_ctr = 0
    time_ctr = 0.0
    exceeded_time = 0.0

    new_run = True
    while not done:
        if new_run:
            run_str = 'RUN {}:'.format(test_ctr)
            print run_str
            f.append_data(run_summary_log, run_str)

        #sh.python(prog_name, benchmark_path, _out=output_log, _err=process_stderr)
        # ./secam.py --filename ./examples/heater/heater.tst --ss-symex klee
        TIMEOUT_FLAG = False
        t0 = time.time()
        try:
            sh.python(prog_name,
                      *arg_list,
                      _out=process_stdout,
                      _err=process_stderr,
                      _timeout=TIMEOUT)
        except sh.TimeoutException:
            TIMEOUT_FLAG = True
            #print 'sub-run timed out!'
            to_str = '\n\ttime spent(s) = {0:.10f}'.format(TIMEOUT)
            f.append_data(run_summary_log, to_str)
            LAST_RESULT = False
            FAIL_CTR += 1
            # How to affect total time in case of a timeout?
            # currently, we ignore it altogether because we are also
            # counting passed and failed runs
            # T += TIMEOUT

        tf = time.time()

        tt = tf - t0
        f.append_data(output_log, STDOUT_DATA)
        STDOUT_DATA = ''

        time_ctr += tt
        exceeded_time = time_ctr >= TIMEOUT

        new_run = LAST_RESULT or exceeded_time or TIMEOUT_FLAG

        if new_run:
            if LAST_RESULT:
                f.append_data(run_summary_log, ' ✓\n')
                run_status = ' ✓ '
                print '\t>> sub-run succeeded'
            else:
                if TIMEOUT_FLAG:
                    run_status = ' ✗ (Killed: sub run timeout)'
                if exceeded_time:
                    run_status = ' ✗ (Run Timedout: {})'.format(time_ctr)
                print '\t>> sub-run failed {}'.format('(timedout)' if TIMEOUT_FLAG else '')
                f.append_data(run_summary_log, ' ✗\n')
                f.append_data(run_summary_log, '\t -- run timeout --\n')

            print run_status
            test_ctr += 1
            time_ctr = 0.0
        else:
            print '\t>> sub-run failed, restarting...'
            f.append_data(run_summary_log, ' ✗\n')

        #test_ctr = test_ctr+1 if LAST_RESULT else test_ctr
        #t0 = tf if LAST_RESULT else t0
        done = NUM_TESTS == test_ctr
        #exceeded_num_runs = test_ctr > MAX_TESTS

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
