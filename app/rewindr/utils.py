from datetime import datetime, date, timedelta


def x_years_ago_time_bounds(x):
    now = datetime.now()
    x_years_ago = subtract_years(now, x)
    x_years_ago_plus_one_day = add_days(x_years_ago, 1)
    return to_timestamp(x_years_ago), to_timestamp(x_years_ago_plus_one_day)


def one_year_ago_today():
    now = datetime.now()
    return subtract_years(now, 1)


def one_year_ago_plus_one_day():
    return add_days(one_year_ago_today(), 1)


def subtract_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year=d.year - years, hour=0, minute=0, second=0, microsecond=0)
    except ValueError:
        return d - (date(d.year - years, 1, 1) - date(d.year, 1, 1))


def add_days(d, days):
    """Return a date that's `days` days after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination date, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(day=d.day + days, hour=0, minute=0, second=0, microsecond=0)
    except ValueError:
        return d + timedelta(days=days)


def to_timestamp(d):
    return int((d - datetime(1970, 1, 1)).total_seconds())