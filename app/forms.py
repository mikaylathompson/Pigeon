from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(Form):
    username = StringField('username', [DataRequired()])
    password = PasswordField('password', [DataRequired()])

class SignupForm(Form):
    username = StringField('username', [DataRequired()])
    password = PasswordField('password',
            [DataRequired(), EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('confirm')

class NewMessageForm(Form):
    destination = StringField('dest', [DataRequired()])
    message = StringField('message', [DataRequired()])


