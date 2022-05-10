import InputDataTreatment as D
import MultiCohortClasses as Cls
import MultiCohortSupport as Support
import NealClasses as P

N_COHORTS = 200  # number of cohorts
POP_SIZE = 100 # population size of each cohort

# create a multi-cohort to simulate under no therapy
multiCohortNo = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=POP_SIZE,
    therapy=P.Therapies.NONE
)

multiCohortNo.simulate(sim_length=D.SIM_TIME_STEPS)

# create a multi-cohort to simulate under rampiril therapy
multiCohortRampiril = Cls.MultiCohort(
    ids=range(N_COHORTS, 2*N_COHORTS),
    pop_size=POP_SIZE,
    therapy=P.Therapies.RAMPIRIL
)

multiCohortRampiril.simulate(sim_length=D.SIM_TIME_STEPS)

# print the estimates for the mean survival time and mean time to AIDS
Support.print_outcomes(multi_cohort_outcomes=multiCohortNo.multiCohortOutcomes,
                       therapy_name=P.Therapies.NONE)
Support.print_outcomes(multi_cohort_outcomes=multiCohortRampiril.multiCohortOutcomes,
                       therapy_name=P.Therapies.RAMPIRIL)

# # draw survival curves and histograms
# Support.plot_survival_curves_and_histograms(multi_cohort_outcomes_mono=multiCohortNo.multiCohortOutcomes,
#                                             multi_cohort_outcomes_combo=multiCohortRampiril.multiCohortOutcomes)

# print comparative outcomes
Support.print_comparative_outcomes(multi_cohort_outcomes_mono=multiCohortNo.multiCohortOutcomes,
                                   multi_cohort_outcomes_combo=multiCohortRampiril.multiCohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(multi_cohort_outcomes_mono=multiCohortNo.multiCohortOutcomes,
                       multi_cohort_outcomes_combo=multiCohortRampiril.multiCohortOutcomes)