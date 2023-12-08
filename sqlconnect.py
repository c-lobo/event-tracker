import pymysql
import datetime
import calendar
from datetime import date, datetime

user = 'Cameron'
today = date.today()
monthNum = datetime.now().month
monthName = datetime.now().strftime("%B")
months = calendar.month_name[1:]

# creates connection to task database 'taskdb' and returns connection object
def mysqlconnect():
    conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'Slim3!',
        database = 'taskdb'
    )    
    
    return conn
