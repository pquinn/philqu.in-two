from rewindr import *
from flask import render_template, request, abort, session, redirect, url_for, Blueprint
from datetime import datetime

START_YEAR = 2010

mod_rewindr = Blueprint('mod_rewindr', __name__, url_prefix='/rewindr')


@mod_rewindr.route('/', methods=['GET', 'POST'])
def rewindr():
    if request.method == 'POST':
        username = request.form['username']
        if username:
            session['username'] = username
            return redirect_to_home()
        else:
            return abort(400)
    elif request.method == 'GET':
        username = session.get('username')
        if username:
            artists = get_user_top_artists(username)
            albums = get_top_albums(username)
            return render_template('rewindr/index.html',
                                   artist_items=artists,
                                   album_items=albums)
        else:
            return render_template('rewindr/index.html')
    else:
        return render_template('rewindr/index.html')


@mod_rewindr.route('/clear/')
def clear_session_username():
    # choosing to clear just the username instead of the whole session
    session['username'] = None
    return redirect(url_for('mod_rewindr.rewindr'))


@mod_rewindr.route('/past/')
def rewindr_day():
    username = session.get('username')
    if username:
        current_year = datetime.now().year
        past_tracks_by_years = {}
        for year in range(current_year - 1, START_YEAR, -1):
            years_ago = current_year - year
            try:
                past_tracks_by_years[years_ago] = get_tracks_for_day(years_ago=years_ago, username=username)
            except ValueError as e:
                print e

        return render_template('rewindr/past.html',
                               track_dict=past_tracks_by_years,
                               current_time=datetime.now())
    else:
        return redirect_to_home()


@mod_rewindr.route('/today/')
def rewindr_today():
    username = session.get('username')
    if username:
        try:
            tracks = get_recent_tracks(username)
            now_playing = get_track_now_playing(username)
            return render_template('rewindr/today.html',
                                   username=username,
                                   now_playing=now_playing,
                                   tracks=tracks,
                                   active_page='today')
        except ValueError as e:
            print e
    else:
        return redirect_to_home()


def redirect_to_home():
    return redirect(url_for('mod_rewindr.rewindr'))