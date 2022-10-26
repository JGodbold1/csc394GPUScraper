from flask import Flask
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from os import path

# The current database connection is made
# with the assumption that it does not have
# a password and default port 5432
DB_HOST = 'test'
DB_USER = 'postgres'

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecret!"

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    get_db_conn()
    create_tables()

    return app

# connect to the database
def get_db_conn():
    conn = psycopg2.connect(dbname=DB_HOST, user=DB_USER)
    return conn

def create_tables():
    conn = psycopg2.connect(dbname=DB_HOST, user=DB_USER)
    cur = conn.cursor()

    # create accounts table
    cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20)
                )
                ''')
                
    cur.close()
    conn.commit()