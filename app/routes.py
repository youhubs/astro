from datetime import datetime
from flask import flash, render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from flask_mail import Mail
from werkzeug.security import generate_password_hash

from . import app, db
from .forms import ContactForm, ChangePasswordForm, CsrfProtectForm, ProfileForm, LoginForm, RegistrationForm
from .models import Event, EventRegistration, User

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
        print(f"Name: {form.name.data}, Email: {form.email.data}, Message: {form.message.data}")
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


@app.route("/events")
def events():
    current_time = datetime.now()
    form = CsrfProtectForm()  # Create a form instance for CSRF protection
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template("events.html", events=events, form=form, current_time=current_time)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('login')) 
        else:# or 'admin' if user is admin
            flash('Invalid username or password', 'error') 
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register_event/<int:event_id>', methods=['POST'])
@login_required
def register_event(event_id):
    # Check if the user is already registered for the event
    existing_registration = EventRegistration.query.filter_by(
        user_id=current_user.user_id,
        event_id=event_id
    ).first()

    if existing_registration:
        flash('You are already registered for this event.', 'error') 
    else:
        # Create a new event registration
        new_registration = EventRegistration(user_id=current_user.user_id, event_id=event_id)
        db.session.add(new_registration)
        db.session.commit()
        flash('You have successfully registered for the event.', 'success') 
    return redirect(url_for('events'))  # Redirect back to the events page


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = ProfileForm(obj=current_user)
    change_password_form = ChangePasswordForm() 
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        # ... update other fields as necessary ...
        db.session.commit()
        flash('Your profile has been updated successfully.', 'success') 
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    if change_password_form.validate_on_submit():
        # Handle password change...
        if current_user.verify_password(change_password_form.old_password.data):
            current_user.password = change_password_form.new_password.data
            db.session.commit()
            flash('Your password has been updated successfully.', 'success') 
        else:
            flash('Invalid old password.')
        return redirect(url_for('account'))
    else:
        # Query registered events for the current user
        user_registrations = EventRegistration.query.filter_by(user_id=current_user.user_id).all()
        # Pass the events to the template
        return render_template('account.html', 
                            user=current_user, 
                            form=form, 
                            change_password_form=change_password_form, 
                            user_registrations=user_registrations)