import numpy as np

import psim
import csim
import fileOps as fp
import utils as U


# For efficiency, Consider named tuples instead? or something else?
class System(object):
    def __init__(self, controller_path, num_dims, plant_config_dict,
                 delta_t, controller_path_dir_path, controller_object_str,
                 path, plant_pvt_init_data, min_smt_sample_dist,
                 ci_grid_eps, pi_grid_eps, comp_scheme):

        self.comp_scheme = comp_scheme
        self.controller_path = controller_path
        self.controller_object_str = controller_object_str
        self.num_dims = num_dims
        self.plant_pvt_init_data = plant_pvt_init_data
        # split plant_config into sys,opt, and props. Also, cleanup names and
        # make them uniform with controller names
        self.plant_config_dict = plant_config_dict

        self.delta_t = delta_t
        self.controller_path_dir_path = controller_path_dir_path
        self.path = path

        # TODO: sampling_dist along with abstraction params need to be
        # separated and the plat abs dict needs to go!
        self.min_smt_sample_dist = min_smt_sample_dist

        self.ci_grid_eps = ci_grid_eps
        self.pi_grid_eps = pi_grid_eps

        self.sanity_check = U.assert_no_Nones

        return

    def init_sims(self, plt_lib, psim_args):
        self.plant_sim = psim.simulator_factory(
            self.plant_config_dict,
            self.path,
            plt=plt_lib,
            plant_pvt_init_data=self.plant_pvt_init_data,
            parallel=False,
            sim_args=psim_args)# TAG:MSH
        if self.controller_path is None:
            self.controller_sim = csim.DummyController(self.num_dims)
        else:
            self.controller_sim = csim.ControllerSO(
                fp.construct_path(self.controller_path, self.path),
                self.num_dims)
        self.controller_sim.compute = self.controller_sim.call

    def __repr__(self):
        s = vars(self)
        return ','.join(map(str, s.items()))
