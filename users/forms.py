from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from ..models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # to create different validation rules you need to define a function for each field
    # with the pattern below
    # def validate_[field_name](self, [field_name]):
    def validate_username(self, username):
        # check if the username already exists in the DB
        user = User.query.filter_by(username=username.data).first()
        if(user):
            raise ValidationError('That username is taken. Please choose another one')
    
    def validate_email(self, email):
        # check if the username already exists in the DB
        user = User.query.filter_by(email=email.data).first()
        if(user):
            raise ValidationError('That email is taken. Please choose another one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    pic = FileField('Update Profile Pic', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    # to create different validation rules you need to define a function for each field
    # with the pattern below
    # def validate_[field_name](self, [field_name]):
    def validate_username(self, username):
        if(username.data != current_user.username):
            # check if the username already exists in the DB
            user = User.query.filter_by(username=username.data).first()
            if(user):
                raise ValidationError('That username is taken. Please choose another one')
    
    def validate_email(self, email):
        if(email.data != current_user.email):
            # check if the username already exists in the DB
            user = User.query.filter_by(email=email.data).first()
            if(user):
                raise ValidationError('That email is taken. Please choose another one')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        # check if the username already exists in the DB
        user = User.query.filter_by(email=email.data).first()
        if(user is None):
            raise ValidationError('There is no account with that email, you must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')