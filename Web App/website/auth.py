from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

# Create register page
@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 2:
            flash('Username must be more than two characters long.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 6:
            flash('Password must be longer than six characters.', category='error')
        else:
            # add user to database
            pass
    return render_template("register.html")

#  Create login page
@auth.route('/login', methods=['GET','POST'])
def login():
    return render_template("login.html")

# Logout to the home screen
@auth.route('/')
def logout():
    pass

# Create Admin Page
@auth.route('/admin')
def admin():
    return render_template("admin.html")