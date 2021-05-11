from flask import render_template, Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Please enter a valid email'), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=29)])
    email = StringField('email', validators=[InputRequired(), Email(message='Please enter a valid email'), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])