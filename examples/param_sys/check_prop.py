########################
# Property Checker
########################

import scipy.linalg as lg

# number of satelites
NUM_SATS = 2
# num space dimensions: 3-d space
DIM = 3

# Tolderance, how close can the satelites come?
TOL = 10.0 # 10.0 for no good reason. Modify as necessary


# should be able to check the property on both concrete and abstract
# states?
def check_prop(plant_states):
    ps = plant_states
    assert(NUM_SATS == 2)
    num_states = len(ps)/NUM_SATS
    # compute displacement for satelites
    #return distance(ps[i:i+DIM], ps[i+num_states:i+num_states+DIM])
    return distance(ps[0:DIM], ps[num_states:num_states+DIM])


def distance(x, y):
    return lg.norm(x-y, ord=2)
