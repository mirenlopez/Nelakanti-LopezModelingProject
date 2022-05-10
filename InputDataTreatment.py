from enum import Enum

# simulation settings
POP_SIZE = 2000         # cohort population size
SIM_TIME_STEPS = 10    # length of simulation (years)
RAMPIRIL_COST = 7313   # yearly cost of rampiril
Discount = 0.03
ALPHA = 0.05

class CKDStates(Enum):
    """ CKD stages of patients """
    STAGE1 = 0
    STAGE2 = 1
    STAGE3 = 2
    STAGE4 = 3
    STAGE5 = 4


# transition matrix

trans_prob_matrix_one = [
    [0.9245,  0.045,    0.0205,  0.008,  0.002],   # Stage 1
    [0,       0.91,    0.0546,  0.028,  0.0074],    # Stage 2
    [0,         0,       0.9187,  0.064,  0.0173],    # Stage 3
    [0,         0,         0,     0.78,  0.22],    # Stage 4
    [0,         0,         0,        0,       1]      # Stage 5
    ]

trans_prob_matrix_five = [
    [0.670053,  0.151008,    0.085437,  0.04752,  0.042108],   # Stage 1
    [0,       0.617427,    0.160578,  0.108933,  0.10857],    # Stage 2
    [0,         0,      0.605604, 0.186714,  0.203412],    # Stage 3
    [0,         0,         0,     0.349668,  0.620664],    # Stage 4
    [0,         0,         0,        0,       1]      # Stage 5
    ]

trans_prob_matrix_ten = [
    [0.442158,  0.18777,    0.12639,  0.103521,  0.133914],   # Stage 1
    [0,      0.377517,    0.173679,  0.180906,  0.260832],    # Stage 2
    [0,         0,       0.343466,   0.251856,  0.251856],    # Stage 3
    [0,         0,         0,     0.331188,  0.657624],    # Stage 4
    [0,         0,         0,        0,       1]      # Stage 5
    ]

ANNUAL_STATE_UTILITY = [
    .859,
    .854,
    .749,
    .634,
    0
    ]

ANNUAL_STATE_COST = [
    12340,
    18335,
    24458,
    42531,
    0
    ]