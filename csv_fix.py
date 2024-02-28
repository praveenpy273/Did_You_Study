import pandas as pd
from dateutil import parser
from datetime import timedelta
import math

file = 'test_study_tracker.csv'
csv_df = pd.read_csv(file)
start_date = '30-1-2024'
target_date = input()
org_target_date = parser.parse(target_date).date()
parsed_start_date = parser.parse(start_date).date()
print(parsed_start_date)

initial_hours_left = ((org_target_date- parsed_start_date).days) * 3
csv_df_copy = csv_df.copy()
for i in range(len(csv_df_copy)):
    csv_df_copy.loc[i, 'Actual_Hours_Left']= initial_hours_left - csv_df_copy.loc[i, 'Hours_studied']
    csv_df_copy.loc[i, 'Revised_Days_Left'] = math.ceil(csv_df_copy.loc[i, 'Actual_Hours_Left']/ 3)
    csv_df_copy.loc[i, 'Initial_target_days'] = (org_target_date - pd.to_datetime(csv_df_copy.loc[i, 'Date']).date()).days
    print(type(csv_df_copy.loc[i, 'Revised_Days_Left']))
    print(type(csv_df_copy.loc[i, 'Initial_target_days']))
    diff = (csv_df_copy.loc[i, 'Initial_target_days'] - csv_df.loc[i, 'Revised_Days_Left'])
    print(diff,type(diff))
    csv_df_copy.loc[i, 'Trend'] = int(csv_df_copy.loc[i, 'Initial_target_days'] - csv_df.loc[i, 'Revised_Days_Left'])
    csv_df_copy.loc[i, 'Likely_Target_Date'] = org_target_date - timedelta(int(diff))
    initial_hours_left = csv_df_copy.loc[i, 'Actual_Hours_Left']
csv_df.update(csv_df_copy)
print(csv_df)
csv_df.to_csv(file,index=False, header=True)