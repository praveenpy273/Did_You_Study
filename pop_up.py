from datetime import date
from dateutil import parser
question = print('What is the target date: ')
answer = input()
try:
    target_date = parser.parse(answer).date()
    print('Parsed_Date',target_date)
except ValueError:
    print('invalid date_format')
