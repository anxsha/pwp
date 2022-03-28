import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import models
from database import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/new-employee', methods=('GET', 'POST'))
@login_required
def new_employee():
    if g.user.position != models.Position.coordinator:
        return "You are not an admin!"
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm-password']
            first_name = request.form['first-name']
            last_name = request.form['last-name']
            position = request.form['position']
            db = get_db()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif password != confirm_password:
                error = 'Passwords do not match'
            elif not first_name:
                error = 'First name is required'
            elif not last_name:
                error = 'Last name is required'

            if not position:
                position = models.Position.unauthorized

            if error is None:
                try:
                    hashed_password = generate_password_hash(password)
                    db_user = models.User(username=username, password=hashed_password, first_name=first_name,
                                          last_name=last_name, position=position)
                    db.add(db_user)
                    db.commit()
                except db.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    return redirect(url_for("auth.login"))

            flash(error)

        return render_template('auth/new-employee.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user:
        return redirect(url_for("home"))
    else:

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            error = None
            user = db.query(models.User).filter(models.User.username == username).first()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user.password, password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['username'] = username
                return redirect(url_for('home'))

            flash(error)

        return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = get_db().query(models.User).filter(models.User.username == username).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
