import pylast
from datetime import date, datetime
from app import app

API_KEY = app.config.get("LASTFM_KEY")
API_SECRET = app.config.get("LASTFM_SECRET")

# need to authenticate to write
username = "phillmatic19"
#password_hash = pylast.md5("password here")

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

def get_top_artists():
    return network.get_top_artists()

def get_user_top_albums(username):
    return network.get_user(username).get_top_albums()

def get_user_top_artists(username):
    return network.get_user(username).get_top_artists()

def get_user_recent_tracks(username="phillmatic19"):
    try:
        return network.get_user(username).get_recent_tracks(limit=25)
    except Exception as e:
        return []

def get_tracks_for_day(years_ago=1, username="phillmatic19"):
    dates = x_years_ago_time_bounds(years_ago)
    from_date = dates[0]
    to_date = dates[1]
    # print "from_date", from_date
    # print "to_date", to_date
    try:
        return network.get_user(username).get_recent_tracks(limit=25, time_from=from_date, time_to=to_date)
    except Exception as e:
        return []

def x_years_ago_time_bounds(x):
    now = datetime.now()
    x_years_ago = subtract_years(now, x)
    x_years_ago_plus_one_day = add_days(x_years_ago, 1)
    return x_years_ago, x_years_ago_plus_one_day

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
        return d + (date(d.day + days, 1, 1) - date(d.day, 1, 1))

def to_timestamp(d):
    return (d - datetime(1970, 1, 1)).total_seconds()
