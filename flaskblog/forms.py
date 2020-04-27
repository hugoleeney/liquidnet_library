from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()])

    password = StringField(
        'Password',
        validators=[DataRequired(), Length(min=4)])

    confirm_password = StringField(
        'Confirm Password',
        validators=[DataRequired(), Length(min=4), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()])

    password = StringField(
        'Password',
        validators=[DataRequired(), Length(min=4)])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')