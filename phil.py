import os
from flask import Flask
from flask import render_template, redirect

app = Flask(__name__)

@app.route('/')
def slashn():
    return redirect('/n')

@app.route('/n')
def index():
    return render_template('index.html')
