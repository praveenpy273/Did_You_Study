from datetime import date, datetime, timedelta
from dateutil import parser
import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import math
import os
import matplotlib.pyplot as plt

question = print('What is the target date: ')
answer = input()
try:
    target_date = parser.parse(answer).date()
    print('Target_Date',target_date)
except ValueError:
    print('invalid date_format')

todays_date = datetime.now().strftime('%d-%m-%Y')
current_date = parser.parse(todays_date).date()
print('Today is: ', current_date)

days_left = target_date - current_date
days_left_to_achieve_target = days_left.days
print('Days left to achieve target: ', days_left.days)
total_hours = days_left_to_achieve_target * 3
print('Total hours to acheive target: ', total_hours)
window = tk.Tk()
window.attributes('-topmost', True)
window.withdraw() #Hide main window


# Prompting users for their input

daily_ques = messagebox.askquestion('Did you study today? ', icon = 'info')
print("User's response", daily_ques)
if daily_ques == 'yes':
    hours_ques = simpledialog.askinteger('Good!', 'How many hours did you study? ', parent=window)


    if hours_ques < 3:
        total_hours += hours_ques
    else:
        total_hours -= hours_ques
else:
    total_hours += 3
    hours_ques = 0

        
print('Revised total hours: ', total_hours)
still_days_left_to_achieve_target = math.ceil(total_hours / 3)

print('Revised days left: ', still_days_left_to_achieve_target)


if still_days_left_to_achieve_target > days_left_to_achieve_target:
    negative_trend =  days_left_to_achieve_target - still_days_left_to_achieve_target
    positive_trend = 0
    print('trend is: ', negative_trend)
    
    if negative_trend < -10:
        messagebox.showwarning('Warning','What are you doing, work hard or forget!')
    else:
        messagebox.showwarning(Warning,'Need to pick up!')
else:
    messagebox.showinfo('Info','Good going!')
    positive_trend =  days_left_to_achieve_target - still_days_left_to_achieve_target
    negative_trend = 0
    
data = {'Date': [current_date], 'Hours_studied' : [hours_ques], 'Initial_target_days': [days_left_to_achieve_target],
         'Revised_Days_Left' : [still_days_left_to_achieve_target], 
         'Negative_Trend': [negative_trend] if negative_trend else [0],
         'Positive_Trend': [positive_trend] if positive_trend else [0]}


df = pd.DataFrame(data)
print(df)


# Saving datafrafe to csv file
csv_file = 'test_study_tracker.csv'

# Check if the file exists if not create the file
if not os.path.isfile(csv_file):
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False, header=True)
# else:
#     df_loaded = pd.read_csv(csv_file)
#     if current_date in df_loaded['Date'].values:
#         df_loaded.loc[df_loaded['Date'] == str(current_date), 'Hours_studied'] = hours_ques

#     else:
#         new_data = {'Date': [current_date], 'Hours_studied' : [hours_ques], 'Initial_target_days': [days_left_to_achieve_target],
#          'Revised_Days_Left' : [still_days_left_to_achieve_target], 
#          'Negative_Trend': [negative_trend] if negative_trend else [0],
#          'Positive_Trend': [positive_trend] if positive_trend else [0]}
        
#         new_df = pd.DataFrame(new_data)
#         df_loaded = pd.concat([df_loaded, new_df], ignore_index=True)
#         print('df_loaded after concat: ', df_loaded)
#         df_loaded['Date'] = df_loaded['Date'].astype(str)
# df_loaded.to_csv(csv_file, index=False, header=True)
        

df_loaded = pd.read_csv(csv_file)

# Displaying the progress in plot
plt.figure(figsize=(12,8))

#plotting hours studied
plt.subplot(3,1,1)
plt.plot(df_loaded['Date'], df_loaded['Hours_studied'], marker='o', label='Hours Studied')
          
plt.title('Daily Hours Studied')
plt.xlabel('Date')
plt.ylabel('Hours Studied')
plt.legend()

#plotting target days movement

plt.subplot(3,1,2)
plt.plot(df_loaded['Date'], df_loaded['Revised_Days_Left'], marker='o', label='Revised_Days_Left')
plt.title('Target Days')
plt.xlabel('Date')
plt.ylabel('Revised_Days_Left')
plt.legend()
#plotting possitive and negative trend

plt.subplot(3,1,3)
plt.plot(df_loaded['Date'], df_loaded['Negative_Trend'], marker='o', label='Negative_Trend')
plt.plot(df_loaded['Date'], df_loaded['Positive_Trend'], marker='o', label='Positive_Trend')
plt.title('Study_tracker trend')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()

plt.tight_layout # Adjust layout for better appearance
plt.show()

window.deiconify() # Show the window briefly
window.destroy()



