import SimPy.Markov as Markov
import SimPy.Plots.SamplePaths as Path
from AtrFibInputData import HealthStates


class Patient:
    def __init__(self, id, transition_prob_matrix):
        """ initiates a patient
        :param id: ID of the patient
        :param transition_prob_matrix: transition probability matrix
        """
        self.id = id
        self.transProbMatrix = transition_prob_matrix
        self.stateMonitor = PatientStateMonitor()

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
            self.stateMonitor.update(time_step=k, new_state=HealthStates(new_state_index))

            # increment time
            k += 1


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self):

        self.currentState = HealthStates.WELL    # current health state
        self.survivalTime = None                 # survival time
        self.timeToPostStroke = None             # time to post-stroke

    def update(self, time_step, new_state):
        """
        update the current health state to the new health state
        :param time_step: current time step
        :param new_state: new state
        """

        # update survival time
        if new_state == HealthStates.DEATH:
            self.survivalTime = time_step + 0.5  # corrected for the half-cycle effect

        # update time until death
        if self.currentState != HealthStates.POST_STROKE and new_state == HealthStates.POST_STROKE:
            self.timeToPostStroke = time_step + 0.5  # corrected for the half-cycle effect

        # update current health state
        self.currentState = new_state

    def get_if_alive(self):
        """ returns true if the patient is still alive """
        if self.currentState != HealthStates.DEATH:
            return True
        else:
            return False


class Cohort:
    def __init__(self, id, pop_size, transition_prob_matrix):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param transition_prob_matrix: transition probability matrix
        """
        self.id = id
        self.popSize = pop_size
        self.transitionProbMatrix = transition_prob_matrix
        self.cohortOutcomes = CohortOutcomes()  # outcomes of this simulated cohort

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        """
        # populate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              transition_prob_matrix=self.transitionProbMatrix)
            # simulate
            patient.simulate(n_time_steps)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []             # patients' survival times
        self.timesToPostStroke = []         # patients' times to post stroke
        self.meanSurvivalTime = None        # mean survival times
        self.meanTimeToPostStroke = None    # mean time to post stroke
        self.nLivingPatients = None         # survival curve (sample path of number of alive patients over time)

    def extract_outcome(self, simulated_patient):
        """ extracts outcomes of a simulated patient
        :param simulated_patient: a simulated patient"""

        # record survival time and time until post stroke health state
        if simulated_patient.stateMonitor.survivalTime is not None:
            self.survivalTimes.append(simulated_patient.stateMonitor.survivalTime)
        if simulated_patient.stateMonitor.timeToPostStroke is not None:
            self.timesToPostStroke.append(simulated_patient.stateMonitor.timeToPostStroke)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """

        # calculate mean survival time
        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)
        # calculate mean time to Post Stroke
        self.meanTimeToPostStroke = sum(self.timesToPostStroke)/len(self.timesToPostStroke)

        # survival curve
        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=initial_pop_size,
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
