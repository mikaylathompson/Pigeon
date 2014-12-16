from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app, db, lm
from forms import LoginForm, SignupForm, NewMessageForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User, Message
import datetime

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
    return render_template('index.html')

@app.route('/api/publickey/<name>', methods=['GET'])
def publickey(name):
    user = load_user(name)
    if user is not None:
        return jsonify({'status': 'true', 'user': user.name, 'publickey': user.publickey})
    return jsonify({'status': 'false', 'user': name})

@app.route('/api/users', methods=['GET'])
def users():
    return jsonify({'users': [{'name':u.name, 'id':u.id} for u in User.query.all()]})

@app.route('/api/messages', methods=['GET'])
def messages():
    return jsonify({'messages': [m.json() for m in Message.query.all()]})

@app.route('/api/messages/<name>', methods=['GET'])
def user_message(name):
    if load_user(name) is None:
        return jsonify({'status': 'false', 'error': 'User does not exist.'})
    return jsonify({'user': name,
        	'messages': [m.json() for m in Message.query.filter_by(destName = name).all()]})

@app.route('/api/compose', methods=['POST'])
def api_compose():
    if not request.json:
        return jsonify({'status': 'false', 'error': 'Not JSON'})
    mess = Message()
    try:
        mess.text = request.json['text']
        mess.destName = request.json['destName']
        mess.originName = request.json['originName']
    except KeyError:
        return jsonify({'status': 'false', 'error': 'Missing fields.'})
    if load_user(mess.destName) is None or load_user(mess.originName) is None:
        return jsonify({'status': 'false', 'error': 'Users do not exist.'})
    mess.read = False
    mess.sent = datetime.datetime.now()
    db.session.add(mess)
    db.session.commit()
    return jsonify({'status': 'true'})

@app.route('/api/signup', methods=['POST'])
def api_signup():
    if not request.json:
        return jsonify({'status': 'false'})
    user = User()
    try:
        user.name = request.json['name']
        user.passhash = request.json['passhash']
        user.publickey = request.json['publickey']
        user.privatekey = request.json['privatekey']
    except KeyError:
        return jsonify({'status': 'false'})
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 'true'})

