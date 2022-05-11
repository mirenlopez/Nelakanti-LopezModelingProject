import InputDataTreatment as D
import MultiCohortClasses as Cls
import MultiCohortSupport as Support
import NealClasses as P
import SimPy.Plots.Histogram as Hist
import SimPy.Plots.SamplePaths as Path

N_COHORTS = 200          # number of cohorts
therapy = P.Therapies.RAMPIRIL  # selected therapy
notherapy = P.Therapies.NONE

# create multiple cohort
multiCohort_notherapy = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=D.POP_SIZE,
    therapy=notherapy)

multiCohort_therapy = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=D.POP_SIZE,
    therapy=therapy)

multiCohort_notherapy.simulate(sim_length=D.SIM_TIME_STEPS)
multiCohort_therapy.simulate(sim_length=D.SIM_TIME_STEPS)

# # plot the sample paths
# Path.plot_sample_paths(
#     sample_paths=multiCohort.multiCohortOutcomes.survivalCurves,
#     title='Survival Curves',
#     x_label='Time-Step (Year)',
#     y_label='Number Survived',
#     transparency=0.5)

# # plot the histogram of average survival time
# Hist.plot_histogram(
#     data=multiCohort.multiCohortOutcomes.meanSurvivalTimes,
#     title='Histogram of Mean Survival Time',
#     x_label='Mean Survival Time (Year)',
#     y_label='Count')

# print the outcomes of this simulated cohort
Support.print_outcomes(multi_cohort_outcomes=multiCohort_notherapy.multiCohortOutcomes,
                       therapy_name=notherapy)
Support.print_outcomes(multi_cohort_outcomes=multiCohort_therapy.multiCohortOutcomes,
                       therapy_name=therapy)
