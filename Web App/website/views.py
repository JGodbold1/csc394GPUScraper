from flask import Blueprint, render_template, session, flash, redirect, url_for
from . import get_db_conn

views = Blueprint('views', __name__)

# home page
@views.route('/')
def home():
    return render_template('home.html')

