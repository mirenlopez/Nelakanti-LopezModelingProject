import SimPy.RandomVariateGenerators as RVGs
from ParameterClasses import *  # import everything from the ParameterClass module
import InputDataNoTreatment as Data
import InputDataNoTreatment as DataNT

class Parameters:
    """ class to include parameter information to simulate the model """

    def __init__(self, therapy):

        self.therapy = therapy              # selected therapy
        self.initialHealthState = Data.CKDStates     # initial health state
        self.annualTreatmentCost = 0        # annual treatment cost
        self.transRateMatrix = []                # transition probability matrix of the selected therapy
        self.annualStateCosts = []          # annual state costs
        self.annualStateUtilities = []      # annual state utilities
        self.discountRate = Data.Discount   # discount rate


class ParameterGenerator:
    """ class to generate parameter values from the selected probability distributions """

    def __init__(self, therapy):

        self.therapy = therapy
        self.probMatrixRVG = []     # list of dirichlet distributions for transition probabilities
        # self.lnRelativeRiskRVG = None  # normal distribution for the natural log of the treatment relative risk
        self.annualStateCostRVG = []  # list of gamma distributions for the annual cost of states
        self.annualStateUtilityRVG = []  # list of beta distributions for the annual utility of states
        self.annualTreatmentCostRVG = None   # gamma distribution for treatment cost

        # create Dirichlet distributions for transition probabilities
        j = 0
        for probs in Data.trans_prob_matrix_one:
            # note:  for a Dirichlet distribution all values of the argument 'a' should be non-zero.
            # setting if_ignore_0s to True allows the Dirichlet distribution to take 'a' with zero values.
            self.probMatrixRVG.append(RVGs.Dirichlet(
                a=probs, if_ignore_0s = True))
            j += 1
        i = 0
        for probs in DataNT.trans_prob_matrix_one:
            # note:  for a Dirichlet distribution all values of the argument 'a' should be non-zero.
            # setting if_ignore_0s to True allows the Dirichlet distribution to take 'a' with zero values.
            self.probMatrixRVG.append(RVGs.Dirichlet(
                a=probs, if_ignore_0s = True))
            i += 1

        # create gamma distributions for annual state cost
        for cost in Data.ANNUAL_STATE_COST:

            # if cost is zero, add a constant 0, otherwise add a gamma distribution
            if cost == 0:
                self.annualStateCostRVG.append(RVGs.Constant(value=0))
            else:
                # find shape and scale of the assumed gamma distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 5
                fit_output = RVGs.Gamma.fit_mm(mean=cost, st_dev=cost / 5)
                # append the distribution
                self.annualStateCostRVG.append(
                    RVGs.Gamma(a=fit_output["a"],
                               loc=0,
                               scale=fit_output["scale"]))

        # create a gamma distribution for annual treatment cost
        if self.therapy == Therapies.RAMPIRIL:
            annual_cost = Data.RAMPIRIL_COST
        else:
            annual_cost = 0.00001
        fit_output = RVGs.Gamma.fit_mm(mean=annual_cost, st_dev=annual_cost / 5)
        self.annualTreatmentCostRVG = RVGs.Gamma(a=fit_output["a"],
                                                 loc=0,
                                                 scale=fit_output["scale"])



    def get_new_parameters(self, rng):
        """
        :param rng: random number generator
        :return: a new parameter set
        """

        # create a parameter set
        param = Parameters(therapy=self.therapy)

        # calculate transition probabilities
        prob_matrix = []    # probability matrix without background mortality added
        # for all health states
        for s in Data.CKDStates:
            # if the current state is not death
            if s not in [Data.CKDStates.STAGE5]:
                # sample from the dirichlet distribution to find the transition probabilities between hiv states
                # fill in the transition probabilities out of this state
                prob_matrix.append(self.probMatrixRVG[s.value].sample(rng))

        # calculate transition probabilities between hiv states
        if self.therapy == Therapies.RAMPIRIL:
            # calculate transition probability matrix for the mono therapy
            param.transRateMatrix = Data.trans_prob_matrix_one

        elif self.therapy == Therapies.NONE:
            # calculate transition probability matrix for the combination therapy
            param.transRateMatrix = DataNT.trans_prob_matrix_one

        # sample from gamma distributions that are assumed for annual state costs
        for dist in self.annualStateCostRVG:
            param.annualStateCosts.append(dist.sample(rng))

        # sample from the gamma distribution that is assumed for the treatment cost
        param.annualTreatmentCost = self.annualTreatmentCostRVG.sample(rng)



        # return the parameter set
        return param

