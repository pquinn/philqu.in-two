import os
from flask import Flask, render_template

# Import SQLAlchemy
#from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
if 'APP_SETTINGS' in os.environ:
    print 'loading config from \'APP_SETTINGS\': ' + os.environ['APP_SETTINGS']
    app.config.from_object(os.environ['APP_SETTINGS'])
else:
    print 'no \'APP_SETTINGS\' found; loading config.DevelopmentConfig'
    app.config.from_object('config.DevelopmentConfig')

# Define the database object which is imported
# by modules and controllers
# db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
   return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.rewindr.controllers import mod_rewindr as rewindr
from app.site.controllers import mod_site as site

# Register blueprint(s)
app.register_blueprint(site)
app.register_blueprint(rewindr)
# app.register_blueprint(xyz_module)