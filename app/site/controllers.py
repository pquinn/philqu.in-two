from flask import app, render_template, redirect, Blueprint

mod_site = Blueprint('site', __name__)

@mod_site.route('/')
def slashn():
    return redirect('/n')

@mod_site.route('/n/')
def index():
    return render_template('site/index.html')
