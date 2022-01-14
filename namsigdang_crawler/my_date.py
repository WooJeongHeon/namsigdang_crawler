import datetime
import calendar


def my_date_today():
    return datetime.date.today()  # 2019-04-07


def day_of_the_week():
    return calendar.day_name[my_date_today().weekday()]  # Sunday


def my_date():
    return str(my_date_today()) + "-" + str(day_of_the_week())


def today_date():
    return str(datetime.datetime.now())  # 2019-04-07 16:45:15.103445


def today_year():
    return datetime.datetime.today().year  # 현재 연도 가져오기


def today_month():
    return datetime.datetime.today().month  # 현재 월 가져오기
