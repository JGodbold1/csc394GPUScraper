import functools
from time import sleep
import psycopg2
from website.amazonscrapper import runSearch
from website.db_insert import insert_to_db
from website.db_conn import get_db_conn
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


# connect to the database using credentials contained within main.py

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


# User registration
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db_conn()
        cur = conn.cursor()
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        hashed_password = generate_password_hash(password1)  # type: ignore

        # check if account exists already
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cur.fetchone()
        # show errors upon failed validation checks
        if account:
            flash('User already exists!', category='error')
        elif len(username) < 2:  # type: ignore
            flash('Username must be more than two characters long.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 6:  # type: ignore
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
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_conn()
        cur = conn.cursor()
        error = None
        cur.execute('SELECT * FROM USERS WHERE username  = %s', (username,))
        user = cur.fetchone()
        # print(user)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            if user[3]:
                session['user_id'] = user[0]
                session['username'] = 'admin'
                session['password'] = user[2]
            else:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['password'] = user[2]
            # print(session)
            return redirect(url_for('views.home'))

        flash(error)

    return render_template('login.html')


"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        print("route - login - request method POST: User Name: " + \
              session['username'])
        password = request.form.get('password')
        conn = get_db_conn()
        cur = conn.cursor()

        # cur.execute('SELECT * FROM users WHERE username = %s;', (session['username'],))
        cur.execute('SELECT * FROM USERS WHERE username  = %s;',
                    (session['username'],))  # ls 11-1-2022 make logical or
        account = cur.fetchone()
        if account:
            if check_password_hash(account[2], password):  # type: ignore
                flash(
                    f'Logged in as {session["username"]}.', category='success')
                sleep(.3)
                if account[3]:
                    session['username'] = 'admin'
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')

            session['user_id'] = account[0]
        else:
            flash('User does not exist.', category='error')
        # print(session['username'])

    return render_template("login.html")
"""


# Logout to home screen, flash message on logout
@auth.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.clear()
    flash('Logged out.')
    return redirect(url_for('auth.login'))


# Create Admin Page


@auth.route('/admin')
def admin():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT user_id, username, isAdmin FROM USERS;')
    users = cur.fetchall()
    return render_template("admin.html", user=users)


# grab form data from home page form and print on results


@auth.route('/search', methods=['POST', 'GET'])
def search():
    conn = get_db_conn()
    cur = conn.cursor()
    if request.method == 'POST':
        #path = 'website/gpu.csv'
        path = 'gpu.csv'
        term = request.form['searchbar']
        # print(term)
        # runSearch(term, path)
        # insert_to(path)_db
        cur.execute('''
                   SELECT gpu_id, store, gpu, manufacturer, memory, price, link FROM GPUS
                   WHERE gpu like %s''',
                    (('%'+term+'%',)))
        # cur.execute('''
        #            SELECT store, gpu, manufacturer, memory, price FROM GPUS
        #            WHERE gpu = %s''',
        #            (term,))
        # conn.commit()
        data = list(set(cur.fetchall()))
        #print(data)
        cur.close()
        conn.commit()
        return render_template("results.html", list=data)

    return render_template('home.html')
    # cur.execute('SELECT store, gpu, manufacturer, memory, price FROM GPUS')
    # glist = cur.fetchall()
    # return render_template("action.php")
    # add users to the database


@ auth.route('/add_user', methods=['POST', 'GET'])  # type: ignore
def add_user():
    conn = get_db_conn()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cur = conn.cursor()
        cur.execute('SELECT * FROM USERS WHERE username = %s', (username,))
        account = cur.fetchone()
        # show errors upon failed validation checks
        if account:
            flash('User already exists!', category='error')
        elif len(username) < 2:
            flash('Username must be more than two characters long.', category='error')
        elif len(password) < 6:
            flash('Password must be longer than six characters.', category='error')
        elif role != 'true' and role != 'false':
            flash("Role must either be 'true' or 'false'.", category='error')
        else:
            # add user to database after passing validation checks
            cur.execute('INSERT INTO USERS (username, password, isAdmin)'
                        'VALUES (%s,%s,%s)',
                        (username, generate_password_hash(password), role))
            conn.commit()
            flash('User created.', category='success')

        return redirect(url_for('auth.admin'))


# update users in the database


@ auth.route('/update/<string:id>', methods=['POST', 'GET'])
def update(id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM USERS WHERE user_id = %s', (id,))
    data = cur.fetchall()
    #print(data[0])

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role'].lower()

        if len(username) < 2:
            flash('Username must be more than two characters long.', category='error')
        elif 0 < len(password) < 6:
            flash('Password must be longer than five characters.', category='error')
        elif role != 'true' and role != 'false':
            flash("Role must be set to true or false.", category='error')
        else:
            # ls need try catch blcok to handle duplicate key values
            if len(password) == 0:
                try:
                    test = cur.execute('''
                            UPDATE USERS u SET
                            username = %s, isAdmin = %s
                            WHERE user_id = %s
                            ''', (username, role, id))
                    print(test.__str__)
                    conn.commit()
                    flash('User updated.', category='success')
                except:
                    print("Crash! duplicate key found")
                    flash('Username has already been taken.', category='error')
                return redirect(url_for('auth.admin'))
            else:
                try:
                    test = cur.execute('''
                            UPDATE USERS u SET
                            username = %s, password = %s, isAdmin = %s
                            WHERE user_id = %s
                            ''', (username, generate_password_hash(password), role, id))
                    print(test.__str__)
                    conn.commit()
                    flash('User updated.', category='success')
                except:
                    print("Crash! duplicate key found")
                    flash('Username has already been taken.', category='error')
                return redirect(url_for('auth.admin'))

    return render_template('update.html', user=data[0])


# remove users from the database


@ auth.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete(id):
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute('DELETE FROM USERS WHERE user_id = %s', (id,))
    conn.commit()
    flash('User deleted.', category='error')
    return redirect(url_for('auth.admin'))


@auth.route('/add_fav', methods = ['POST', 'GET'])
def add_fav():
        print("addingin" + id + "to favorits")