import pylast
from app import app
from app.rewindr.utils import x_years_ago_time_bounds
from pylast import WSError

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


def get_recent_tracks(username, limit=25):
    try:
        return network.get_user(username).get_recent_tracks(limit=limit)
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
