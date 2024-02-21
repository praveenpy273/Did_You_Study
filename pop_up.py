from datetime import date, datetime, timedelta
from dateutil import parser
import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import math
import os
import matplotlib.pyplot as plt

def get_target_date():
    while True:
        try:
            question = print('What is the target date: ')
            answer = input()
            parsed_date = parser.parse(answer).date()
            today_date = date.today()
            if parsed_date >= today_date:
                return parsed_date
            else:
                print("Error: target Date cannot be less than today's date")         
        except ValueError:
            print('invalid date_format')
            return None

def likely_target_date(trgt,org_days_left,act_days_left):
    difference_after_yesterday_hours = act_days_left - org_days_left
    likely_target_acheive_date = trgt + timedelta(difference_after_yesterday_hours)
    return likely_target_acheive_date


def find_actual_hours(hours_ques,org_hrs,min_study_hours = 3): 
    if hours_ques == 0:
        act_hrs = org_hrs + min_study_hours
    elif 0 < hours_ques < min_study_hours:
        act_hrs = org_hrs + (min_study_hours-hours_ques)
    elif hours_ques >= min_study_hours:
        act_hrs = org_hrs - hours_ques
    
    return act_hrs


def find_trend(org_days_left,actual_days_left, trend = 0):
    diff = actual_days_left - org_days_left
    if diff == 0:
        trend = 0
    elif diff > 0:
        trend -= diff
    else:
        trend += diff

    return trend


def main():
    
    target_date = get_target_date()
    todays_date = datetime.now().date()
    # todays_date = parser.parse(todays_date).date()
    yesterday = todays_date-timedelta(days=1)
    print('Yesterday was: ', yesterday)

    days_left = target_date - yesterday
    org_days_left = days_left.days
    print('Days left to achieve target: ', days_left.days)
    original_hours_left = org_days_left * 3 #calculates the hours left to acheive target
    print('Total hours to acheive target: ', original_hours_left)
    window = tk.Tk()
    window.attributes('-topmost', True)
    window.withdraw() #Hide main window

    # Prompting users for their input

    daily_ques = messagebox.askquestion('Did you study yesterday? ', icon = 'info')
    print("User's response", daily_ques)
    if daily_ques == 'yes':
        hours_ques = simpledialog.askinteger('Good!', 'How many hours did you study? ', parent=window) # hours studied yesterday
        actual_hours_left = find_actual_hours(hours_ques,original_hours_left)

    else:
        hours_ques = 0
        actual_hours_left = find_actual_hours(hours_ques,original_hours_left)
            
    print('Revised total hours: ', actual_hours_left) # hours left after adjusting yesterday's 

    actual_days_left = math.ceil(actual_hours_left / 3)

    
    likely_target_acheive_date = likely_target_date(target_date,org_days_left,actual_days_left)
    print(likely_target_acheive_date)

    data = {'Date': [yesterday], 'Hours_studied' : [hours_ques], 'Original_Target_Date' : [target_date],
            'Likely_Target_Date': [likely_target_acheive_date],
            'Initial_target_days': [org_days_left],
            'Revised_Days_Left' : [actual_days_left],
            'Hours_left_for_target': [original_hours_left],
            'Actual_Hours_Left' : find_actual_hours(hours_ques,original_hours_left),
            'Trend': [find_trend(org_days_left,actual_days_left)]}

    df = pd.DataFrame(data)
    print(df)

    # Saving datafrafe to csv file
    csv_file = 'test_study_tracker.csv'

    # Check if the file exists if not create the file
    if not os.path.isfile(csv_file):
        print('file not found!, hence a new file created')
        df.to_csv(csv_file, index=False, mode='a', header=True)
        df_loaded = pd.read_csv(csv_file)
        # df_loaded.to_csv(csv_file, index=False, header=True)
    else:
        print('file found!')
        df_loaded = pd.read_csv(csv_file)
        print('Before concat: ', df_loaded)
        l = len(df_loaded) #length of existing dataframe
        print('hours_studied:', hours_ques)
        print('rows in df: ', l)

        
        if str(yesterday) in df_loaded['Date'].astype(str).values: #if the entry for a date is already there and want to adjust the hours
            print('file found!, but date already exists')
            date_condition = df_loaded['Date'].astype(str) == str(yesterday)

            df_loaded.loc[date_condition, ['Hours_studied']] = hours_ques

            actual_hours = find_actual_hours(hours_ques,df_loaded['Actual_Hours_Left'].iloc[l-2])
            actual_days_left = math.ceil(actual_hours/3)

            df_loaded.loc[date_condition, ['Actual_Hours_Left']] = actual_hours
            df_loaded.loc[date_condition, ['Revised_Days_Left']] = actual_days_left
            df_loaded.loc[date_condition, ['Likely_Target_Date']] = likely_target_date(target_date,org_days_left,actual_days_left)
            df_loaded.loc[df_loaded['Date'].astype(str) == str(yesterday), ['Trend']] = \
                find_trend(org_days_left,actual_days_left)
            
        else:
            l = len(df_loaded) #length of existing dataframe
            print('hours_studied:', hours_ques)
            print('rows in df: ', l)
        
            actual_hours_left = find_actual_hours(hours_ques,df_loaded['Actual_Hours_Left'].iloc[l-1])
            print('else block', actual_hours_left)

            actual_days_left = math.ceil(actual_hours_left/3)
            likely_target_acheive_date = likely_target_date(target_date,org_days_left,actual_days_left)

            # creating data for new rows
            new_data = {'Date': [yesterday], 'Hours_studied' : [hours_ques], 'Original_Target_Date' : [target_date],
            'Likely_Target_Date': [likely_target_acheive_date],
            'Initial_target_days': [org_days_left],
            'Revised_Days_Left' : [actual_days_left],
            'Hours_left_for_target': [original_hours_left],
            'Actual_Hours_Left' : [actual_hours_left],
            'Trend' :find_trend(org_days_left,actual_days_left)}

            
            new_df = pd.DataFrame(new_data)
            df_loaded['Date'] = df_loaded['Date'].astype(str)
            new_df['Date'] = new_df['Date'].astype(str)
            common_columns = df_loaded.columns.intersection(new_df.columns)#finding common columns
            
            # concattenating 2 dataframes
            df_loaded = pd.concat([df_loaded[common_columns],new_df[common_columns]],ignore_index=True)
            print('After concat: ', df_loaded)
        
        df_loaded.to_csv(csv_file, index=False, header=True)
            
        func_trend = find_trend(org_days_left,actual_days_left)

        if 0 > func_trend > -10:
            messagebox.showwarning(Warning,'Need to pick up!')

        elif func_trend <= -10:
            messagebox.showwarning('Warning','What are you doing, work hard or forget!')

        else:
            messagebox.showinfo('Info','Good going!')


        # Displaying the progress in plot
        plt.figure(figsize=(12,8))

        #plotting hours studied
        plt.subplot(3,1,1)
        plt.plot(df_loaded['Date'], df_loaded['Hours_studied'], marker='o', label='Hours Studied')
                
        plt.title('Daily Hours Studied')
        plt.xlabel('Date')
        plt.ylabel('Hours Studied')
        plt.legend()

        plt.tight_layout() # Adjust layout for better appearance

        #plotting target days movement
        plt.subplot(3,1,2)
        plt.plot(df_loaded['Date'], df_loaded['Revised_Days_Left'], marker='o', label='Revised_Days_Left')
        plt.title('Target Days')
        plt.xlabel('Date')
        plt.ylabel('Revised_Days_Left')
        plt.legend()

        plt.tight_layout # Adjust layout for better appearance

        #plotting possitive and negative trend
        plt.subplot(3,1,3)
        plt.plot(df_loaded['Date'], df_loaded['Trend'], marker='o',label='Trend')
        plt.title('Study_tracker trend')
        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.legend()

        plt.tight_layout # Adjust layout for better appearance
        plt.show()

        window.deiconify() # Show the window briefly
        window.destroy()


if __name__ == '__main__':
    main()
