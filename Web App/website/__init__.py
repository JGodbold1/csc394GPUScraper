from flask import Flask
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from os import path

# The current database connection is made
# with the assumption that it does not have
# a password and default port 5432
# DB_NAME = 'gpuapp_db' #ls nov 6 EC2CHANGE
# DB_USER = 'postgres' #ls nov 6 EC2CHANGE
# DB_PASS = 'postgres' #ls - nov 6 - added for localhost debugging EC2CHANGE
#ls 11/08/2022 adding EC2 elements
DB_HOST = 'db-hw3.cyxa8bcyeg3o.us-east-1.rds.amazonaws.com'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS =  'he1pMEplease'
DB_PORT = 5432
DEFAULT_ADMIN_PASS = generate_password_hash('allswellthatendswell')

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
    #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS) ls 11/08/2022 disabling for deployment
    conn = psycopg2.connect(host = DB_HOST, dbname=DB_NAME, user=DB_USER, password = DB_PASS, port = DB_PORT)
    return conn

def create_tables():
    #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS)ls 11/08/2022 disabling for deployment
    conn = psycopg2.connect(host = DB_HOST, dbname=DB_NAME, user=DB_USER, password = DB_PASS, port = DB_PORT)
    cur = conn.cursor()


    cur.execute('DROP TABLE IF EXISTS USERS CASCADE')
    cur.execute('DROP TABLE IF EXISTS GPUS CASCADE')
    cur.execute('DROP TABLE IF EXISTS FAVORITES CASCADE')
    # create users table
    cur.execute('''
                CREATE TABLE IF NOT EXISTS USERS (
                    id          SERIAL UNIQUE PRIMARY KEY,
                    username    VARCHAR(32)  NOT NULL UNIQUE,
                    password    VARCHAR(255) NOT NULL,
                    isAdmin     BOOL DEFAULT FALSE
                )
                ''')
    # create gpu table
    cur.execute('''
                CREATE TABLE IF NOT EXISTS GPUS (
                    gpu_id          SERIAL UNIQUE PRIMARY KEY,
                    store           TEXT,
                    gpu             TEXT,
                    manufacturer    TEXT,
                    memory          SMALLINT,
                    price           FLOAT,
                    link            TEXT
                    )
                    ''')
                
    # create favorites table
    cur.execute('''
                CREATE TABLE IF NOT EXISTS FAVORITES (
                    id          INTEGER,
                    username    VARCHAR(32),
                    CONSTRAINT fk_gpu FOREIGN KEY (id) REFERENCES GPUS(gpu_id),
                    CONSTRAINT fk_username FOREIGN KEY (username) REFERENCES USERS(username)
                )
                ''')

    cur.execute('''
                INSERT INTO USERS (username, password, isAdmin)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
                ''', ('dkulis', DEFAULT_ADMIN_PASS, True))

    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Micro Center', 'GTX 3050', 'Asus', 8, 429.99, false)''')
    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Micro Center', 'GTX 3050', 'MSI', 8, 339.99, true)''')
    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Micro Center', 'GTX 3050', 'EVGA', 8, 329.99, true)''')
    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Micro Center', 'GTX 3060', 'Nvidia', 12, 379.99, true)''')
    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Micro Center', 'GTX 3060', 'Nvidia', 12, 399.99, true)''')
    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Best Buy', 'GTX 3080', 'Asus', 8, 429.99, false)''')
    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Best Buy', 'GTX 3080ti', 'MSI', 8, 339.99, true)''')
    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Best Buy', 'GTX 3070', 'EVGA', 8, 329.99, true)''')
    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Best Buy', 'GTX 3070 Super', 'Nvidia', 12, 379.99, true)''')
    cur.execute('''
                INSERT INTO GPUS (store, gpu, manufacturer, memory, price, inStock) 
                VALUES('Best Buy', 'GTX 3060', 'EVGA', 12, 399.99, true)''')
                
    cur.close()
    conn.commit()