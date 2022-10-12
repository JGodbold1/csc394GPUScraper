from flask import Blueprint, render_template
from . import get_db_conn

views = Blueprint('views', __name__)

# home page is also the landing page (for when a user logs in)
@views.route('/')
def home():
    return render_template('home.html')

