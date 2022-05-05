import InputDataNoTreatment as D
import SimPy.Plots.Histogram as Hist
import SimPy.Plots.SamplePaths as Path
from MarkovModelClasses import Cohort

# create a cohort
myCohort = Cohort(id=1,
                  pop_size=D.POP_SIZE,
                  transition_prob_matrix_one=D.trans_prob_matrix_one)

# simulate the cohort over the specified time steps
myCohort.simulate(n_time_steps=500)

# plot the sample path (survival curve)
Path.plot_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Time-Step (Year)',
    y_label='Number Survived')
#
# plot the histogram of survival times
Hist.plot_histogram(
    data=myCohort.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1)

# print the patient survival time
print('Mean survival time (years):',
      myCohort.cohortOutcomes.meanSurvivalTime)
# # # print mean time to Post Stroke
# print('Mean time until Post Stoke (years)',
#        myCohort.cohortOutcomes.meanTimeToPostStroke)
