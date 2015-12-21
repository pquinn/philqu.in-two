import os
from flask import Flask
from flask import render_template, redirect
from rewindr import *

app = Flask(__name__)

app.debug = True

@app.route('/')
def slashn():
    return redirect('/n')

@app.route('/n')
def index():
    return render_template('index.html')

@app.route('/rewindr')
def rewindr():
    artists = get_user_top_artists()
    return render_template('rewindr/index.html', artists=artists)

@app.route('/rewindr/today')
@app.route('/rewindr/today/<username>')
def rewinder_day(username="phillmatic19"):
    tracks = get_user_recent_tracks(username)
    return render_template('rewindr/playlist.html', tracks=tracks)

if __name__ == '__main__': app.run();
