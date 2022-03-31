from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")



@auth.route('/logout')
def logout():
    return render_template("logout.html") # temp



@auth.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")