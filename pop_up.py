from datetime import date, datetime, timedelta
from dateutil import parser
import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import math
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
    print('trend is: ', negative_trend)
    
    if negative_trend < -10:
        messagebox.showwarning('Warning','What are you doing, work hard or forget!')
    else:
        messagebox.showwarning(Warning,'Need to pick up!')
else:
    messagebox.showinfo('Info','Good going!')
    possitive_trend =  still_days_left_to_achieve_target > days_left_to_achieve_target
    
data = {'Date': current_date, 'Hours_studied' : hours_ques, 'Initial_target_days': days_left_to_achieve_target,
         'Revised_Days_Left' : still_days_left_to_achieve_target}


df = pd.DataFrame([data],index = [0])
print(df)

window.deiconify() # Show the window briefly
window.destroy()
