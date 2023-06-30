from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2)])
    email = EmailField("Email", validators=[DataRequired(), Email(
        message=("Not a valid email address."))])
    message = TextAreaField("Message", validators=[DataRequired(), Length(
        min=4, message="Your message is too short")])
    submit = SubmitField("Send Message")

class LoginForm(FlaskForm):
    email=EmailField("Email", validators=[DataRequired(), Email(message=("Not a valid email address"))])
    password=PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2)])
    email=EmailField("Email", validators=[DataRequired(), Email(message=("Not a valid email address"))])
    password=PasswordField("Password", validators=[DataRequired(), Length(min=8,  message="Your password is too short")])
    submit = SubmitField("Register")