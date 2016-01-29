import pylast
from pylast import PlayedTrack, WSError
from datetime import date, datetime
from app import app

API_KEY = app.config.get("LASTFM_KEY")
API_SECRET = app.config.get("LASTFM_SECRET")

# need to authenticate to write
#username = "phillmatic19"
#password_hash = pylast.md5("password here")

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)


def get_top_artists():
    return network.get_top_artists()


def get_top_albums(username):
    return network.get_user(username).get_top_albums()


def get_user_top_artists(username):
    return network.get_user(username).get_top_artists()


def get_recent_tracks(username):
    try:
        return network.get_user(username).get_recent_tracks(limit=25)
    except Exception as e:
        return []


def get_track_now_playing(username):
    try:
        return network.get_user(username).get_now_playing()
    except Exception as e:
        return {}


def get_tracks_for_day(username, limit=10, years_ago=1):
    dates = x_years_ago_time_bounds(years_ago)
    from_date = dates[0]
    to_date = dates[1]
    user = network.get_user(username)
    tracks = user.get_recent_tracks(limit=limit, cacheable=False, time_from=from_date, time_to=to_date)
    # return _get_track_links(tracks)
    return tracks


def _get_track_links(tracks):
    linked = []
    for t in tracks:
        linked_track = TrackWithLink(t)
        try:
            link = network.get_track_play_links([t.track])
            linked_track.link(link)
        except WSError as e:
            print e

        linked.append(linked_track)

    return linked


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
        return d + (date(d.day + days, 1, 1) - date(d.day, 1, 1))


def to_timestamp(d):
    return int((d - datetime(1970, 1, 1)).total_seconds())


class TrackWithLink:

    def __init__(self, track):
        self._link = None
        self._track = track

    @property
    def link(self):
        return self._link

    def link(self, link):
        self._link = link

    def track(self):
        return self._track
