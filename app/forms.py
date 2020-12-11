from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, Length, EqualTo, Email, DataRequired, ValidationError
import re
from flask import request

## Custom Validators ##

def validate_email(FlaskForm, field):
    if not (re.search('''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''', field.data)) or (len(field.data) > 300):
        raise ValidationError('Please enter a valid email')

def validate_username(FlaskForm, field):
    if len(field.data) < 4:
        raise ValidationError('Username must be a minimum 4 characters')

def validate_password_length(FlaskForm, field):
    if len(field.data) < 8:
        raise ValidationError('Password must be a minimum 8 characters')

def validate_passwords_match(FlaskForm, field):
    if field.data != request.form.get('password'):
        raise ValidationError('Both password must match')

## Custom Validators End ##

class AdminRegister(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(max=300), validate_email])
    username = StringField(validators=[InputRequired(), validate_username])
    password = PasswordField(validators=[InputRequired(), validate_password_length])
    confirm_password = PasswordField(validators=[InputRequired(), validate_passwords_match])


class AdminLogin(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(max=300)])
    password = PasswordField(validators=[InputRequired()])

class AdminPasswordResetForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(max=300), validate_email])

class AdminSetNewPassword(FlaskForm):
    password = PasswordField(validators=[InputRequired(), validate_password_length])
    confirm_password = PasswordField(validators=[InputRequired(), validate_passwords_match])