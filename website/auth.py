from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from . import db

# flask_login:: login, logout, signup functionality
from flask_login import login_user, login_required, logout_user, current_user

# Generate unique hash for each plaintext password
from werkzeug.security import generate_password_hash, check_password_hash 

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # check if user and password are valid
        user = User.query.filter_by(username=username).first()
        if user:
            # if username exists in database, check if passwords match
            if check_password_hash(user.password, password):
                print('logged in successfully')
                login_user(user, remember=True)
                # Login user, redirect to their home page of tasks
                return redirect(url_for('views.home')) 
            else:
                print('wrong password')
        else: # if username DNE in database
            print('username does not exist')
    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required # can only logout if user is currently logged in
def logout():
    logout_user()
    # after logging out, return to default login page
    return redirect(url_for('auth.login'))



@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['firstName']
        password1 = request.form['password1']
        password2 = request.form['password2']

        # confirm unique username first, same passwords okay
        user = User.query.filter_by(username=username).first()
        if user:
            print('username exists already')
        elif len(username) < 4:
            print('Username must be greater than 3 characters.')
        elif len(first_name) < 2:
            print('First Name must be greater than 1 character.')
        elif password1 != password2:
            print('Passwords don\'t match.')
        elif len(password1) < 7:
            print('Password must be greater than 6 characters.')
        else: # create and add new user into db
            new_user = User(username=username, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            print('new account made')
            # after logging in, redirect User to the Home Page
            return redirect(url_for('views.home')) 

    return render_template("register.html", user=current_user)