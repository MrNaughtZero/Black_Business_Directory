from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators, FileField, TextAreaField, HiddenField, MultipleFileField, SelectField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo

class UserRegister(FlaskForm):
    profile_img = FileField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired(), Email('Invalid Email'), Length(max=300)])
    username = StringField(validators=[InputRequired(), Length(max=300)])
    password = PasswordField(validators=[InputRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class UserLogin(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(max=300)])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField('Login')
