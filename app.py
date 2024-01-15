from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///astro_robotics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Database Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    registrations = db.relationship('Registration', backref='student', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    registrations = db.relationship('Registration', backref='event', lazy=True)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Routes and view functions will be added here
# Continuing with the Flask application code

# Import necessary Flask extensions and modules
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email

# Flask-WTF forms for registration and event management
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()]) # Use StringField for simplicity
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


# Initialize Flask-Admin
admin = Admin(app, name='Astro Robotics Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Registration, db.session))

# Home Page Route
@app.route('/')
def home():
    return render_template('home.html')

# About Page Route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Here, you'll process the form data, like sending an email or storing it in a database
        # For now, I'll just print the data to the console
        print(f"Name: {form.name.data}, Email: {form.email.data}, Message: {form.message.data}")
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

# Events Page Route
@app.route('/events')
def events():
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template('events.html', events=events)

# Registration Route
@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register(event_id):
    form = RegistrationForm()
    event = Event.query.get_or_404(event_id)
    if form.validate_on_submit():
        student = Student(name=form.name.data, email=form.email.data)
        registration = Registration(student=student, event=event)
        db.session.add(student)
        db.session.add(registration)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('events'))
    return render_template('register.html', form=form, event=event)

# Additional routes for admin functionalities can be added as needed

# The templates and static files (CSS and JavaScript) need to be created next.


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will now be executed within the app context
    app.run(debug=True, port=5001)

