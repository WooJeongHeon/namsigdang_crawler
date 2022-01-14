import datetime
import calendar

my_date = datetime.date.today()  # 2019-04-07
day_of_the_week = calendar.day_name[my_date.weekday()]  # Sunday
my_date = str(my_date) + "-" + str(day_of_the_week)
today_date = str(datetime.datetime.now())  # 2019-04-07 16:45:15.103445