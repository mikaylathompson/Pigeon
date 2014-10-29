from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm, SignupForm


@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Mikayla'}
    return render_template('index.html',
                    user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Logging in %s with pass %s.'%
                (form.username.data, form.password.data))
        return redirect('/index')
    return render_template('login.html',
                            title='Login',
                            form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('Sign up: %s, %s'%(form.username.data, form.password.data))
        return redirect('/index')
    return render_template('signup.html',
                            title='Sign up',
                            form=form)
