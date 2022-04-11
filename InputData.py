from enum import Enum

# simulation settings
POP_SIZE = 2000         # cohort population size
SIM_TIME_STEPS = 50    # length of simulation (years)

class HealthStates(Enum):
    """ health states of patients """
    WELL = 0
    POST_STROKE = 1
    DEATH = 2


# transition matrix

trans_prob_matrix = [
    [0.95,  0.035,    0.015],   # WELL
    [0,     0.94,    0.06],     # POST_STROKE
    [0,     0,          1]      # DEATH
    ]

