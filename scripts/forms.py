from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2)])
    email = EmailField("Email", validators=[DataRequired(), Email(
        message=("Not a valid email address."))])
    message = TextAreaField("Message", validators=[DataRequired(), Length(
        min=4, message="Your message is too short")])
    submit = SubmitField("Send Message")
