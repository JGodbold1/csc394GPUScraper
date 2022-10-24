from flask import Flask
import psycopg2
from os import path

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecret!"

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    get_db_conn()

    return app

# connect to the database
def get_db_conn():
    conn = psycopg2.connect('dbname=test user=postgres')
    return conn