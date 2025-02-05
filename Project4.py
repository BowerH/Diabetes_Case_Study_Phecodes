import pandas as pd

# exclusion range 249-250.99
################################
################################
# Cases: 18,300
# Control: 9,397
# Excluded: 10,246 + 2,263 = 12,509
################################
################################
# Path to the fastq_to_dataframe file
phecodemap =pd.read_csv("/Users/hannah/Tech/BIOL6150/Phecode_map.csv", sep=",",encoding="ISO-8859-1")
tempcohort= pd.read_csv("/Users/hannah/Tech/BIOL6150/ParticipantEHR.tsv", sep="\t")
#established_type_two= cohort[cohort.duplicated(subset=['Participant_ID', 'Value'], keep=False)]
## this joins the phecode and the cohort together, so I can look at exlcusion data.
cohort = pd.merge(tempcohort, phecodemap, left_on='ICD10CM', right_on='icd10cm')
cohort['phecode'] = cohort['phecode'].astype(float) #changing the phecode to a float so I can filter by it, just a formality

# getting the control, everything that is NOT(~) in the exclusion range
controltemp = cohort[~(cohort['phecode'] >= 249) & (cohort['phecode'] <= 250.99)]
control = controltemp[~controltemp.duplicated('ParticipantID', keep=False)] #remove duplicates

### both of the excluded ones,
excludedtemp1 = cohort[(cohort['phecode'] >= 249) & (cohort['phecode'] <= 250.99)& (cohort['phecode'] != 250.2)]
excluded1 = excludedtemp1[~excludedtemp1.duplicated('ParticipantID', keep=False)]

#this phecode is the one for t2d, need it to filter from only this dataset.
type2diabetes = cohort[cohort['phecode'] == 250.2]

### finding the final only 1 instance
count1 = type2diabetes.groupby('ParticipantID').size()
single_entry_participants = count1[count1 == 1].index
finalonly1instance = cohort[cohort['ParticipantID'].isin(single_entry_participants) & (cohort['phecode'] == 250.2)]


### finding the cases
unique_date_counts = type2diabetes.groupby('ParticipantID')['Date'].nunique().reset_index()
participants_with_multiple_dates = unique_date_counts[unique_date_counts['Date'] >= 2]['ParticipantID']
tempppp = type2diabetes[type2diabetes['ParticipantID'].isin(participants_with_multiple_dates) & (type2diabetes['phecode'] == 250.2)]
cases= tempppp.drop_duplicates(subset=['ParticipantID'])


print()