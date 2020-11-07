from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, message='Select a stronger password.')]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
