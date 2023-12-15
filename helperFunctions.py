# function takes in the name of the month 
# creates a dictionary with month number 
# as key and names as values
# then it creates a list out of the 
# dictionary values finally it indexes 
# the list with the name given 

import calendar
import datetime
from datetime import datetime
import calendar



months = calendar.month_name[1:]
monthName = datetime.now().strftime("%B")
monthNum = datetime.now().month


def name2num(x):
    year = {}
    for idx, month in enumerate(months):
        year[idx+1] = month.capitalize()
    mNums = list(year.values())
    y = mNums.index(x) + 1
        
    return y

