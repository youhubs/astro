from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


# Flask-WTF forms for registration and event management
class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")


class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    date = StringField(
        "Date", validators=[DataRequired()]
    )  # Use StringField for simplicity
    submit = SubmitField("Submit")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")
