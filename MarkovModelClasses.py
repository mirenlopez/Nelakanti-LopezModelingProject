import numpy as np

import SimPy.Markov as Markov
import SimPy.Plots.SamplePaths as Path
from InputDataNoTreatment import CKDStates
import SimPy.EconEval as Econ
import SimPy.Statistics as Stat


class Patient:
    def __init__(self, id, transition_prob_matrix_one, parameters):
        """ initiates a patient
        :param id: ID of the patient
        :param transition_prob_matrix_one: transition probability matrix
        """
        self.id = id
        self.transProbMatrix = transition_prob_matrix_one
        self.params = parameters
        self.stateMonitor = PatientStateMonitor(parameters=parameters)

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        # random number generator
        rng = np.random.RandomState(seed=self.id)
        # jump process
        markov_jump = Markov.MarkovJumpProcess(transition_prob_matrix=self.transProbMatrix)

        k = 0  # simulation time step

        # while the patient is alive and simulation length is not yet reached
        while self.stateMonitor.get_if_alive() and k < n_time_steps:

            # sample from the Markov jump process to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = markov_jump.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # update health state
            self.stateMonitor.update(time_step=k, new_state=CKDStates(new_state_index))

            # increment time
            k += 1


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, parameters):

        self.currentState = CKDStates.STAGE1    # current health state
        self.survivalTime = None                # survival time
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time_step, new_state):
        """
        update the current health state to the new health state
        :param time_step: current time step
        :param new_state: new state
        """

        # update survival time
        if new_state == CKDStates.STAGE5:
            self.survivalTime = time_step + 0.5  # corrected for the half-cycle effect

        # update cost and utility
        self.costUtilityMonitor.update(k=time_step,
                                       current_state=self.currentState,
                                       next_state=new_state)

        # update current health state
        self.currentState = new_state

    def get_if_alive(self):
        """ returns true if the patient is still alive """
        if self.currentState != CKDStates.STAGE5:
            return True
        else:
            return False

class PatientCostUtilityMonitor:

    def __init__(self, parameters):

        # model parameters for this patient
        self.params = parameters

        # total cost and utility
        self.totalDiscountedCost = 0
        self.totalDiscountedUtility = 0

    def update(self, k, current_state, next_state):
        """ updates the discounted total cost and health utility
        :param k: simulation time step
        :param current_state: current health state
        :param next_state: next health state
        """

        # update cost
        cost = 0.5 * (self.params.annualStateCosts[current_state.value] +
                      self.params.annualStateCosts[next_state.value])
        # update utility
        utility = 0.5 * (self.params.annualStateUtilities[current_state.value] +
                         self.params.annualStateUtilities[next_state.value])

        # add the cost of treatment
        if next_state == CKDStates.STAGE5:
            cost += 0.5 * self.params.annualTreatmentCost
        else:
            cost += 1 * self.params.annualTreatmentCost

        # update total discounted cost and utility (corrected for the half-cycle effect)
        self.totalDiscountedCost += Econ.pv_single_payment(payment=cost,
                                                           discount_rate=self.params.discountRate / 2,
                                                           discount_period=2 * k + 1)
        self.totalDiscountedUtility += Econ.pv_single_payment(payment=utility,
                                                              discount_rate=self.params.discountRate / 2,
                                                              discount_period=2 * k + 1)





class Cohort:
    def __init__(self, id, pop_size, transition_prob_matrix_one, parameters):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param transition_prob_matrix_one: transition probability matrix
        """
        self.id = id
        self.popSize = pop_size
        self.transitionProbMatrix = transition_prob_matrix_one
        self.params = parameters
        self.cohortOutcomes = CohortOutcomes()  # outcomes of this simulated cohort

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        """
        # populate the cohort
        patients = []  # list of patients
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              parameters=self.params, transition_prob_matrix_one=self.transitionProbMatrix)
            # add the patient to the cohort

            patients.append(patient)

        for patient in patients:
            patient.simulate(n_time_steps=n_time_steps)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patients=patients)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []             # patients' survival times
        self.meanSurvivalTime = None        # mean survival times
        self.nLivingPatients = None         # survival curve (sample path of number of alive patients over time)
        self.costs = []
        self.utilities = []
        self.statCost = None
        self.statUtility = None
        self.statSurvivalTime = None

    def extract_outcome(self, simulated_patients):
        """ extracts outcomes of a simulated patient
        :param simulated_patients: a list of simulated patients"""

        # record survival time and time until post stroke health state
        for patient in simulated_patients:
            if patient.stateMonitor.survivalTime is not None:
                self.survivalTimes.append(patient.stateMonitor.survivalTime)
        # if simulated_patient.stateMonitor.timeToStage5 is not None:
        #     self.timesToStage5.append(simulated_patient.stateMonitor.timeToPostStroke)
                self.costs.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
                self.utilities.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """

        # calculate mean survival time
        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)

        self.statSurvivalTime = Stat.SummaryStat(
            name='Survival time', data=self.survivalTimes)

        self.statCost = Stat.SummaryStat(
            name='Discounted cost', data=self.costs)
        self.statUtility = Stat.SummaryStat(
            name='Discounted utility', data=self.utilities)

        # survival curve
        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=initial_pop_size,
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
