from enum import Enum

# simulation settings
POP_SIZE = 2000         # cohort population size
SIM_TIME_STEPS = 10    # length of simulation (years)

class CKDStates(Enum):
    """ CKD stages of patients """
    STAGE1 = 0
    STAGE2 = 1
    STAGE3 = 2
    STAGE4 = 3
    STAGE5 = 4


# transition matrix

trans_prob_matrix_one = [
    [0.9067,  0.0538,    0.0258,  0.0106,  0.0031],   # Stage 1
    [0,       0.8876,    0.0645,  0.0367,  0.0112],    # Stage 2
    [0,         0,       0.8915,  0.0825,  0.026],    # Stage 3
    [0,         0,         0,     0.6689,  0.3311],    # Stage 4
    [0,         0,         0,        0,       1]      # Stage 5
    ]

trans_prob_matrix_five = [
    [0.6126,  0.1741,    0.1094,  0.0401,  0.0638],   # Stage 1
    [0,       0.5508,    0.2019,  0.0828,  0.1645],    # Stage 2
    [0,         0,       0.5631,  0.1288,  0.3081],    # Stage 3
    [0,         0,         0,     0.0596,  0.9404],    # Stage 4
    [0,         0,         0,        0,       1]      # Stage 5
    ]

trans_prob_matrix_ten = [
    [0.3753,  0.2026,    0.1638,  0.0554,  0.2029],   # Stage 1
    [0,       0.3033,    0.2250,  0.0765,  0.3952],    # Stage 2
    [0,         0,       0.317,   0.0802,  0.6028],    # Stage 3
    [0,         0,         0,     0.0036,  0.9964],    # Stage 4
    [0,         0,         0,        0,       1]      # Stage 5
    ]