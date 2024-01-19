from datetime import datetime
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from flask_mail import Mail, Message

from . import app, db
from .forms import ContactForm, LoginForm, RegistrationForm
from .models import Event, Student, Registration, User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/donate")
def donate():
    return render_template("donate.html")


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


@app.route("/events")
def events():
    current_time = datetime.now()
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template("events.html", events=events, current_time=current_time)


@app.route("/register/<int:event_id>", methods=["GET", "POST"])
def register(event_id):
    form = RegistrationForm()
    event = Event.query.get_or_404(event_id)
    if form.validate_on_submit():
        student = Student(name=form.name.data, email=form.email.data)
        registration = Registration(student=student, event=event)
        db.session.add(student)
        db.session.add(registration)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("events"))
    return render_template("register.html", form=form, event=event)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))  # or 'admin' if user is admin
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/admin/')
@login_required
def admin():
    if current_user.is_admin:  # Ensure current user is admin
        return render_template('admin.html')
    return redirect(url_for('home'))  # Redirect non-admin users

