#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
CSymLoader.py
-------------
Loads the symbolic structure for the controller using either smt2 files or
using pathcrawler's trace. If using the trace, there is an option to load the
trace as a constraint tree enabling incremental constraint solving or a list
which is simpler to use. If instead only smt2 files are provided, a tree can
NOT be constructed, leaving the default option of a list.
Because the size of trace files can be quite large, and the current parser
[using pyparsing], is exceptionally slow, the function also pickles the
parsed tree/list structuresand saves it next to the trace file. This can then
be used in for later runs.
A modified trace file will trigger an automatic re-generation of the struct.
This is detected by md5 hashing.
'''

import pc_trace_parser as tp
import prep_trace as pt
import err
import fileOps as fops

import pickle



# A thin wrapper to Add a md5 hash of the source to the object being pickled
class HashWrapped(object):
    def __init__(self, data, md5sum):
        self.data = data
        self.md5sum = md5sum
        return


def load_sym_obj((cntrl_rep, trace_struct), file_path):
    if cntrl_rep == 'trace':

        paths = None
        # search for a pickled object
        pickle_file_path = file_path + '.pickled'
        if fops.file_exists(pickle_file_path):
            print 'found pickled paths!'
            pickled_paths = fops.get_data(pickle_file_path, 'rb')
            hash_wrapped_paths = pickle.loads(pickled_paths)
            if hash_wrapped_paths.md5sum == fops.compute_hash(file_path):
                print 'loading pickled paths!'
                paths = hash_wrapped_paths.data
            else:
                print 'pickled path is stale, will do fresh computation and overite!'

        if paths is None:
            assert(trace_struct == 'list' or trace_struct == 'tree')
            #self.csym_obj = tp.PathCrawlerTrace(path, 'list')
            print 'parsing trace as a {}...'.format(trace_struct)
            paths = tp.trace_file_to_paths(file_path)
            print 'done.'

            # pickle the parsed paths

            # NOTE: for some reasons the pickle.HIGHEST_PROTOCOL which is <2>
            # gives the below error. Using 1 instead.
            #pickled_paths = pickle.dumps(paths, pickle.HIGHEST_PROTOCOL)
            ####################################################
            #                   ERROR
            ####################################################
            # Traceback (most recent call last):
            # File "./secam.py", line 419, in <module>
            #   main()
            # File "./secam.py", line 415, in main
            #   run_secam(sys, prop, opts)
            # File "./secam.py", line 305, in run_secam
            #   current_abs, sampler = create_abstraction(sys, prop, opts)
            # File "./secam.py", line 161, in create_abstraction
            #   controller_sym_path_obj = CSL.load_sym_obj((opts.cntrl_rep, opts.trace_struct), controller_path_dir_path)
            # File "/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/CSymLoader.py", line 39, in load_sym_obj
            #   pickled_paths = pickle.dumps(paths, 2)
            # File "/usr/lib/python2.7/pickle.py", line 1374, in dumps
            #   Pickler(file, protocol).dump(obj)
            # File "/usr/lib/python2.7/pickle.py", line 224, in dump
            #   self.save(obj)
            # File "/usr/lib/python2.7/pickle.py", line 306, in save
            #   rv = reduce(self.proto)
            ###########################################################

            hash_wrapped_paths = HashWrapped(paths, fops.compute_hash(file_path))
            pickled_paths = pickle.dumps(hash_wrapped_paths, protocol=1)
            #pickled_paths = pickle.dumps(paths, 1)
            #pickle.dump(paths, open('delmepickle', 'wb'), 1)
            #exit()
            fops.write_data(pickle_file_path, pickled_paths, 'wb')

        csym_obj = pt.pathcrawler_obj(paths, trace_struct)

        # get path files, which are in smt2 format with the same extension
    elif cntrl_rep == 'smt2':
        # only list struct can be used!
        csym_obj = pt.get_conslist_from_smt2(file_path)
    else:
        raise err.Fatal('unhandled constraint input option!')

    return csym_obj
