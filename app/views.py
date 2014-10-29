from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm


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
