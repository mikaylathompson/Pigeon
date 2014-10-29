from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, lm
from forms import LoginForm, SignupForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User

@lm.user_loader
def load_user(name):
    user = User.query.filter_by(name=name).first()
    return user

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Mikayla'}
    return render_template('index.html',
                    user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.username.data)
        if user is None:
            flash('User does not exist. Try again or sign up')
            return redirect('/login')
        login_user(user)
        g.user = user
        flash('Logging in %s with pass %s.'%
                (form.username.data, form.password.data))
        return redirect('/index')
    return render_template('login.html',
                            title='Login',
                            form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/index')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('Sign up: %s, %s'%(form.username.data, form.password.data))
        return redirect('/index')
    return render_template('signup.html',
                            title='Sign up',
                            form=form)
