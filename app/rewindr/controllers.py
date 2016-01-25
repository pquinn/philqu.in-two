from rewindr import *
from flask import render_template, request, abort, session, redirect, url_for, Blueprint

mod_rewindr = Blueprint('mod_rewindr', __name__, url_prefix='/rewindr')

@mod_rewindr.route('/', methods=['GET', 'POST'])
def rewindr():
    if (request.method == 'POST'):
        username = request.form['username']
        if username:
            session['username'] = username
            artists = get_user_top_artists(username)
            albums = get_user_top_albums(username)
            return render_template('rewindr/index.html',
                                   username=username,
                                   artist_items=artists,
                                   album_items=albums)
        else:
            return abort(400)
    else:
        return render_template('rewindr/index.html')

@mod_rewindr.route('/clear/')
def clear_session_username():
    session['username'] = None
    return redirect(url_for('mod_rewindr.rewindr'))

@mod_rewindr.route('/lastyear/')
def rewindr_day():
    username = session['username']
    if username:
        try:
            one = get_tracks_for_day(years_ago=1, username=username)
            two = get_tracks_for_day(years_ago=2, username=username)
            three = get_tracks_for_day(years_ago=3, username=username)
            four = get_tracks_for_day(years_ago=4, username=username)
            past_tracks_by_years = {
                1: one,
                2: two,
                3: three,
                4: four
            }
            return render_template('rewindr/past.html',
                                   username=username,
                                   track_dict=past_tracks_by_years,
                                   active_page='past',
                                   current_time=datetime.now())
        except ValueError as e:
            print e
    else:
        return redirect_to_home()


@mod_rewindr.route('/today/')
def rewindr_today():
    username = session['username']
    if username:
        try:
            tracks = get_user_recent_tracks(username)
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