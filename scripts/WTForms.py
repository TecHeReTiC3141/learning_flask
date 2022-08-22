from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,\
    EmailField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Email, Length, DataRequired, EqualTo


class LoginForm(FlaskForm):

    user = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3, max=50), DataRequired()])
    remember = BooleanField('Remember', default=False)
    submit = SubmitField('Send')


class RegisterForm(FlaskForm):

    name = StringField('UserName', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=3, max=50), DataRequired()])
    repeat_password = PasswordField('Repeat Password',
                                    validators=[Length(min=3, max=50), DataRequired(), EqualTo('password')])
    submit = SubmitField('Send')


class FeedbackForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send')
