from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, IntegerField, StringField, PasswordField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed

from app.models import User

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(label='Current Password', validators=[DataRequired(message="This field is required."), Length(min=4, max=10, message='The password must be between 4 and 10 characters.')])
    new_password = PasswordField(label='New Password', validators=[DataRequired(message="This field is required."), Length(min=4, max=10, message='The password must be between 4 and 10 characters.')])
    confirm_password = PasswordField(label='Confirm New Password', validators=[DataRequired(message="This field is required."), Length(min=4, max=10, message='The password must be between 4 and 10 characters.'), EqualTo('new_password', message='New password and confirmation do not match.')])
    submit = SubmitField("Change Password")

    def validate_current_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Incorrect current password. Please try again.')

class TodoForm(FlaskForm):
    title = StringField("Enter a task here", validators=[DataRequired(message="This field is required.")])
    description = StringField("Describe your task", validators=[DataRequired(message="This field is required.")])
    submit = SubmitField("Save")

class FeedbackForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(message="This field is required.")])
    text = TextAreaField(label='Write your review here', validators=[DataRequired(message="This field is required.")])
    rating = IntegerField(label='Rate it from 1 to 5', validators=[DataRequired(message="This field is required."), NumberRange(min=1, max=5, message="Rating must be between 1 and 5.")])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(message="This field is required."), 
                                                         Length(min=4, max=14, message='Username must be between 4 and 14 characters.'),
                                                         Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots, or underscores')])
    email = EmailField('Email', validators=[DataRequired(message="This field is required."), Email(message="Invalid email.")])
    password =  PasswordField(label='Password', validators=[DataRequired(message="This field is required."), Length(min=6, message='Password must be more than 6 characters long')])
    confirm_password =  PasswordField(label='Confirm password', validators=[DataRequired(message="This field is required."), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign up')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Username already exists. Choose a different one.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already exists. Please use a different one.')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(message="This field is required."), Email(message="Invalid email.")])
    password = PasswordField(label='Password', validators=[DataRequired(message="This field is required."), Length(min=6, message='Password must be more than 6 characters long')])
    remember = BooleanField(label='Remember me')
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
        Length(min=4, max=14, message='Username must be between 4 and 14 characters.'), 
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots, or underscores')
    ])
    email = EmailField('Email', validators=[DataRequired("Enter a valid email")])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=240)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

