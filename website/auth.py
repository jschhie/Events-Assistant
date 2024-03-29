from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash 

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = None

        # Check for empty inputs
        if (not username or not password):
            flash('Please enter your username and password.', category='error')
            return render_template("login.html", user=current_user)
       
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You are now logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home')) 
            else:
                flash('Wrong password.', category='error')
        else:
            flash('Username does not exist.', category='error')
            
    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['firstName']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username exists already.', category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7 or len(password1) > 20:
            flash('Password must be between 7 and 20 characters long.', category='error')
        else: 
            new_user = User(username=username, \
                            first_name=first_name, \
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('New account made! You are now logged in.', category='success')
            # after logging in, redirect User to the Home Page
            return redirect(url_for('views.home')) 

    return render_template("register.html", user=current_user)
