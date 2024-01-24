from datetime import date,datetime
from dateutil import parser
question = print('What is the target date: ')
answer = input()
try:
    target_date = parser.parse(answer).date()
    print('Target_Date',target_date)
except ValueError:
    print('invalid date_format')

todays_date = datetime.now().strftime('%d-%m-%Y')
current_date = parser.parse(todays_date).date()
print(current_date)

days_left = target_date - current_date
print(days_left.days)