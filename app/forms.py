from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Required, EqualTo

class LoginForm(Form):
    username = StringField('username', [Required()])
    password = PasswordField('password', [Required()])

class SignupForm(Form):
    username = StringField('username', [Required()])
    password = PasswordField('password', 
            [Required(), EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('confirm')


