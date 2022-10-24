from time import sleep
from . import get_db_conn
from flask import Blueprint, render_template, request, session, redirect, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)
# connect to the database using credentials contained within main.py
conn = get_db_conn()

# User registration
@auth.route('/register', methods=['GET','POST'])
def register():
    cur = conn.cursor()

    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        hashed_password = generate_password_hash(password1)

        # check if account exists already
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cur.fetchone()
        # show errors upon failed validation checks
        if account:
            flash('User already exists!', category='error')
        elif len(username) < 2:
            flash('Username must be more than two characters long.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 6:
            flash('Password must be longer than six characters.', category='error')
        else:
            # add user to database after passing validation checks
            cur.execute('INSERT INTO users (username, password)'
                        'VALUES (%s, %s)',
                        (username, hashed_password))
            conn.commit()
            # redirects upon success to prevent POST request issues
            return redirect(url_for('auth.account_created'))

    return render_template('register.html')

@auth.route('/account_created')
def account_created():
    return render_template('account_created.html')

#  Create login page
@auth.route('/login', methods=['GET','POST'])
def login():
    cur = conn.cursor()

    if request.method == 'POST':
        session['username'] = request.form['username']
        password = request.form.get('password')

        cur.execute('SELECT * FROM users WHERE username = %s;', (session['username'],))
        account = cur.fetchone()
        if account:
            if check_password_hash(account[2], password):
                flash(f'Logged in as {session["username"]}.', category='success')
                sleep(.3)
                if account[3] == 'admin':
                    session['username'] = 'admin'
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('User does not exist.', category='error')
        
    return render_template("login.html")

# Logout to home screen, flash message on logout
@auth.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    flash('Logged out.')
    return render_template('home.html')

# Create Admin Page
@auth.route('/admin')
def admin():
    cur = conn.cursor()
    cur.execute('SELECT VERSION();')
    version = cur.fetchone()
    cur.execute('SELECT id, username, role FROM users;')
    users = cur.fetchall()
    return render_template("admin.html", user=users, version=version)