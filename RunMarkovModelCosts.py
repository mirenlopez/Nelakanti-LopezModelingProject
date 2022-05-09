import InputDataTreatment as DataT
import InputDataNoTreatment as DataNT
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support

# def print_comparative_outcomes(sim_outcomes_none, sim_outcomes_anticoag):
#     """ prints average increase in survival time, discounted cost, and discounted utility
#     under combination therapy compared to mono therapy
#     :param sim_outcomes_none: outcomes of a cohort simulated under mono therapy
#     :param sim_outcomes_anticoag: outcomes of a cohort simulated under combination therapy
#     """

therapy = P.Therapies.RAMPIRIL
none = P.Therapies.NONE

print('therapy cohort')
#  therapy cohort
Therapy = Cls.Cohort(id=1,
                      pop_size=DataT.POP_SIZE,
                      parameters=P.Parameters(therapy=therapy), transition_prob_matrix_one=DataT.trans_prob_matrix_one)

Therapy.simulate(n_time_steps=20)

Support.print_outcomes(sim_outcomes=Therapy.cohortOutcomes, therapy_name=P.Therapies.RAMPIRIL)

print ('no therapy cohort')
# no therapy cohort
NoTherapy = Cls.Cohort(id=1,
                      pop_size=DataNT.POP_SIZE,
                      parameters=P.Parameters(therapy=none), transition_prob_matrix_one=DataNT.trans_prob_matrix_one)

NoTherapy.simulate(n_time_steps=20)

Support.print_outcomes(sim_outcomes=NoTherapy.cohortOutcomes, therapy_name=P.Therapies.NONE)

Support.print_comparative_outcomes(sim_outcomes_none=NoTherapy.cohortOutcomes, sim_outcomes_anticoag=Therapy.cohortOutcomes)


Support.report_CEA_CBA(sim_outcomes_none=NoTherapy.cohortOutcomes, sim_outcomes_anticoag=Therapy.cohortOutcomes)

print("The highest level of willingness to pay is the ICER, which is 33,409.63. Interval= (24,145.15, 55,496.74)")

