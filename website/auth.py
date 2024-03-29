from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('User does not exist', category='error')
            return redirect(url_for('auth.login'))

    return render_template("login.html", user=current_user)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('User already exists', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 2 characters', category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 2:
            flash('Password must be at least 2 characters', category='error')
        else:
            new_user = User(name=name, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)