from flask import Blueprint, render_template
from . import get_db_conn

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')
