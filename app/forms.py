from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, Email, Length, EqualTo

class AdminRegister(FlaskForm):
    email = StringField(validators=[InputRequired(), Email('Invalid Email'), Length(max=300)])
    username = StringField(validators=[InputRequired(), Length(max=300)])
    password = PasswordField(validators=[InputRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AdminLogin(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(max=300)])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField('Login')
