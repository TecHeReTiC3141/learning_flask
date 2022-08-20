from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField,\
    EmailField, PasswordField, BooleanField
from wtforms.validators import Email, Length, DataRequired

class LoginForm(FlaskForm):

    user = EmailField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3, max=50), DataRequired()])
    remember = BooleanField('Remember', default=False)
    submit = SubmitField('Send')
