import numpy as np

import err


class parse_config():
    def __init__(self, config_dict, T):
        # ##!!##logger.debug('parsing abstraction parameters')
        if config_dict['type'] == 'string':
            try:
                grid_eps_str = config_dict['grid_eps']
                # remove braces
                grid_eps_str = grid_eps_str[1:-1]
                self.eps = np.array([float(eps) for eps in grid_eps_str.split(',')])

                pi_grid_eps_str = config_dict['pi_grid_eps']
                # remove braces
                pi_grid_eps_str = pi_grid_eps_str[1:-1]

                self.refinement_factor = float(config_dict['refinement_factor'])
                self.num_samples = int(config_dict['num_samples'])
                self.delta_t = float(config_dict['delta_t'])
                self.N = int(np.ceil(T / self.delta_t))

                # Make the accessed data as None, so presence of spurious data can be detected in a
                # sanity check

                config_dict['grid_eps'] = None
                config_dict['pi_grid_eps'] = None
                config_dict['refinement_factor'] = None
                config_dict['num_samples'] = None
                config_dict['delta_t'] = None
            except KeyError, key:
                raise err.Fatal('expected abstraction parameter undefined: {}'.format(key))
        else:
            for attr in config_dict:
                setattr(self, attr, config_dict[attr])
            self.N = int(np.ceil(T / self.delta_t))
            self.refinement_factor = 2.0

        return
