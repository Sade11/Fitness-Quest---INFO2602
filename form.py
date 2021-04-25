from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length
#from wtforms.fields.html5 import EmailField


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
