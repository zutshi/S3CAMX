import numpy as np


def select(toy_id):
    if toy_id == 1:
        lower_bound = -8.0
    elif toy_id == 2:
        lower_bound = -20.0
    elif toy_id == 3:
        lower_bound = -23.5
    else:
        raise Exception('unknown toy id')

    error_set = [[-np.inf, -np.inf, -np.inf, -np.inf],
                 [np.inf, np.inf, np.inf, lower_bound]]

    initial_set = [[-5.0, 0.0, 0.0, 0.0],
                   [5.0, 0.0, 0.0, 0.0]]

    ci = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
          [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]]

    # Use for testing...reduces the search to just init state
    #ci = [[100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0],
    #      [100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0]]

    return initial_set, error_set, ci
