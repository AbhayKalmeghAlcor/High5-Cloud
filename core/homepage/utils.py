import datetime
from datetime import datetime as dt, timedelta, date
from math import ceil
from dateutil.relativedelta import relativedelta


def get_current_month_year(types):
    if types == "this_month":
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year

    if types == "last_month":
        today = datetime.date.today()
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        month = lastMonth.strftime("%m")
        year = lastMonth.strftime("%Y")

    return month, year


def get_quaterly_dates(types):
    current_date = dt.now()
    if types == "this_quarter":
        current_quarter = ceil(dt.now().month / 3.)

    if types == "last_quarter":
        current_quarter = ceil(dt.now().month / 3.) - 1

    first_date = dt(current_date.year, 3 * current_quarter - 2, 1)
    last_date = first_date + relativedelta(months=3, days=-1)
    first_date = first_date.date()
    last_date = last_date.date()

    return first_date, last_date


def get_last_six_month():
    six_months = date.today() + relativedelta(months=-6)
    current_date = dt.now()
    return six_months, current_date
