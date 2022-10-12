from flask import Blueprint, render_template
from . import get_db_conn

views = Blueprint('views', __name__)

@views.route('/')
def home():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('home.html', users=users)
