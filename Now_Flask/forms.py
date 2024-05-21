from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20, message="Username must be between 3 and 20 characters") ])
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20, message="Password must be between 6 and 20 characters") ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20, message="Password must be between 6 and 20 characters") ])
    submit = SubmitField('Login')


class ResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20, message="Password must be between 6 and 20 characters") ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Password')

class AccountUpdateForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'webp', 'jpeg'])])
    submit = SubmitField('Update Profile Picture')