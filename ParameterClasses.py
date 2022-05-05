from enum import Enum

import numpy as np

import InputDataNoTreatment as DataNT

import InputDataTreatment as DataT




class Therapies(Enum):
    """ mono vs. combination therapy """
    NONE = 0
    RAMPIRIL = 1


class Parameters:
    def __init__(self, therapy):

        # selected therapy
        self.therapy = therapy

        # initial health state
        self.initialHealthState = DataNT.CKDStates.STAGE1

        # annual treatment cost
        if self.therapy == Therapies.RAMPIRIL:
            self.annualTreatmentCost = DataT.RAMPIRIL_COST
        else:
            self.annualTreatmentCost = 0

        # transition probability matrix of the selected therapy
        self.probMatrix = []

        # calculate transition probabilities between stroke states
        if self.therapy == Therapies.NONE:
            # calculate transition probability matrix with anticoagulant
            self.probMatrix = DataNT.trans_prob_matrix_one

        elif self.therapy == Therapies.RAMPIRIL:
            # calculate transition probability matrix for the combination therapy
            self.probMatrix = DataT.trans_prob_matrix_one

        # annual state costs and utilities
        self.annualStateCosts = DataNT.ANNUAL_STATE_COST
        self.annualStateUtilities = DataNT.ANNUAL_STATE_UTILITY

        # discount rate
        self.discountRate = DataT.Discount


# def get_prob_matrix(trans_matrix):
#     """
#     :param trans_matrix: transition matrix containing counts of transitions between states
#     :return: transition probability matrix
#     """
#
#     # initialize transition probability matrix
#     trans_prob_matrix = DataNT.trans_prob_matrix_one
#
#     # # for each row in the transition matrix
#     # for row in trans_matrix:
#     #     # calculate the transition probabilities
#     #     prob_row = np.array(row)/sum(row)
#     #     # add this row of transition probabilities to the transition probability matrix
#     #     trans_prob_matrix.append(prob_row)
#     #
#     # return trans_prob_matrix
#
#
# def get_prob_matrix_anticoag(matrix_anticoag):
#     """
#     :param prob_matrix_mono: (list of lists) transition probability matrix under mono therapy
#     :param combo_rr: relative risk of the combination treatment
#     :returns (list of lists) transition probability matrix under combination therapy """
#
#     # create an empty list of lists
#     matrix_anticoag = DataNT.trans_prob_matrix_one
#
#     # for row in trans_matrix:
#     #     matrix_anticoag.append(np.zeros(len(row)))  # adding a row [0, 0, 0, 0]
#     #
#     # # populate the combo matrix
#     # # calculate the effect of combo-therapy on non-diagonal elements
#     # for s in range(len(matrix_anticoag)):
#     #     for next_s in range(len(Data.HealthStates)):
#     #         matrix_anticoag[s][next_s] = trans_matrix[s][next_s]
#     #
#     # matrix_anticoag[Data.HealthStates.POST_STROKE.value][Data.HealthStates.STROKE.value] = rr * trans_matrix[Data.HealthStates.POST_STROKE.value][Data.HealthStates.STROKE.value]
#     # matrix_anticoag[Data.HealthStates.POST_STROKE.value][Data.HealthStates.POST_STROKE.value] = 1 - matrix_anticoag[Data.HealthStates.POST_STROKE.value][Data.HealthStates.STROKE.value]
#     #
#     # return matrix_anticoag
#
#
# # # tests
# # matrix_mono = get_prob_matrix_mono(Data.TRANS_MATRIX)
# # matrix_combo = get_prob_matrix_combo(matrix_mono, Data.TREATMENT_RR)
# #
# # print(matrix_mono)
# # print(matrix_combo)
