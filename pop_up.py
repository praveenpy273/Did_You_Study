from datetime import date,datetime
from dateutil import parser
import tkinter as tk
from tkinter import messagebox, simpledialog
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
window.withdraw() #Hide main window

# For daily tracker using loop to iterate over days left to achieve target
for day in range(days_left_to_achieve_target):
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
        
print('Revised total hours: ', total_hours)
still_days_left_to_achieve_target = total_hours / 3

print('Revised days left: ', still_days_left_to_achieve_target)


if still_days_left_to_achieve_target > days_left_to_achieve_target:
    trend =  still_days_left_to_achieve_target - days_left_to_achieve_target
    print(trend)
    if trend > 10:
        messagebox.showwarning('Warning','What are you doing, work hard or forget!')
    else:
        messagebox.showwarning(Warning,'Need to pick up!')
else:
    messagebox.showinfo('Info','Good going!')
window.deiconify() # Show the window briefly
window.destroy()
