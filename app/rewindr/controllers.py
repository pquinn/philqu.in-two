from rewindr import *
from flask import render_template, Blueprint, url_for

mod_rewindr = Blueprint('mod_rewindr', __name__, url_prefix='/rewindr')

@mod_rewindr.route('/')
@mod_rewindr.route('/<username>')
def rewindr(username="phillmatic19"):
    artists = get_user_top_artists(username)
    albums = get_user_top_albums(username)
    return render_template('rewindr/index.html', username=username, artists=artists, albums=albums, active_page='rewindr')

@mod_rewindr.route('/lastyear/')
@mod_rewindr.route('/lastyear/<username>')
def rewindr_day(username="phillmatic19"):
    try:
        past_tracks_by_years = {
            'one': get_tracks_for_day(years_ago=1, username=username),
            'two': get_tracks_for_day(years_ago=2, username=username),
            'three': get_tracks_for_day(years_ago=3, username=username),
            'four': get_tracks_for_day(years_ago=4, username=username)
        }
        return render_template('rewindr/past.html',
                               username=username,
                               tracks=past_tracks_by_years,
                               active_page='past',
                               current_time=datetime.now())
    except ValueError as e:
        print e


@mod_rewindr.route('/today/')
@mod_rewindr.route('/today/<username>')
def rewindr_today(username="phillmatic19"):
    try:
        tracks = get_user_recent_tracks(username)
        now_playing = get_track_now_playing(username)
        return render_template('rewindr/today.html', username=username, now_playing=now_playing, tracks=tracks, active_page='today')
    except ValueError as e:
        print e
