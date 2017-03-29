import spotipy
from fuzzywuzzy import fuzz

MATCH_TOLERANCE = 0.85
TRACK_RESULTS_COUNT = 20
MAX_SEARCHES = 5

spotify = spotipy.Spotify()


def get_track_link(track_name, artist_name, album_name):
    return _find_track(track_name, artist_name, album_name)


def _find_track(target_track_name, target_artist_name, target_album_name):
    link = None
    spotify_id = None
    found = False
    searches = 0
    api_calls = 0
    while searches < MAX_SEARCHES and not found:
        current_offset = searches * TRACK_RESULTS_COUNT
        results = spotify.search(q=target_track_name, limit=TRACK_RESULTS_COUNT, offset=current_offset, type='track')
        api_calls += 1
        track_results = results['tracks']['items']
        for track_result in track_results:
            artist_name = track_result['artists'][0]['name']
            album_name = track_result['album']['name']
            if fuzz.ratio(artist_name, target_artist_name) > MATCH_TOLERANCE \
                    and fuzz.ratio(album_name, target_album_name) > MATCH_TOLERANCE:
                link = track_result['external_urls']['spotify']
                spotify_id = track_result['id']
                found = True
                break
        searches += 1

    print "find tracks api calls: {}".format(api_calls)
    return TrackInfo(target_artist_name, target_track_name, target_album_name, link, spotify_id)


class TrackInfo:

    def __init__(self, artist_name, track_name, album_name, spotify_link, spotify_id):
        self.artist_name = artist_name
        self.track_name = track_name
        self.album_name = album_name
        self.spotify_link = spotify_link
        self.spotify_id = spotify_id
