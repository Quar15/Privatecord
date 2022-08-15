from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

from privatecord.models import MasterUser

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=7)])
    confirmPassword = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=7), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        # Check if user with that username exists
        u = MasterUser.query.filter_by(username=username.data).first()
        if u:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        # Check if user with that email exists
        u = MasterUser.query.filter_by(email=email.data).first()
        if u:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')