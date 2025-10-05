import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key'  # Used by Flask for session management and CSRF protection
# why this file is important:
# This file contains the configuration settings for the Flask application, including the database connection URI and other
# essential parameters that control the behavior of the app.    
# It is imported in the main application file (app.py) to set up the app's configuration.
    DEBUG = False