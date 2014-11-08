from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, lm
from forms import LoginForm, SignupForm, NewMessageForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User, Message

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
    user = {'name': 'FAKEUSER'}
    return render_template('index.html',
                    user=user)

@app.route('/inbox')
@login_required
def inbox():
    me = g.user
    my_messages = Message.query.filter_by(destID = me.id).all()
    return render_template('inbox.html',
					user=me,
					messages=my_messages)


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
        return redirect(url_for('index'))
    return render_template('login.html',
                            title='Login',
                            form=form)

@app.route("/compose", methods=['GET', 'POST'])
@login_required
def compose():
    form = NewMessageForm()
    if form.validate_on_submit():
        # create a message object with the fields
        mess = Message()
        if (form.is_encrypted.data):
            # encrypt the messsage with destKey
            mess.text = "SOMETHING ENCRYPTED"
            mess.encrypt = True
        else:
             mess.text = form.message.data
             mess.encrypt = False
        dest = load_user(form.destination.data)
        if dest is None:
            flash('Destination does not exist.')
            return redirect(url_for('compose'))
        mess.destID = dest.id
        mess.originName = g.user.name
        db.session.add(mess)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('compose.html',
                    title='Compose Message',
                    form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('Sign up: %s, %s'%(form.username.data, form.password.data))
        return redirect(url_for('index'))
    return render_template('signup.html',
                            title='Sign up',
                            form=form)
