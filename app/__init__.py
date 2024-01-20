from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///astro_robotics.db"

# Configuration for Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # e.g., 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465  # e.g., 465 for Gmail with SSL
app.config["MAIL_USERNAME"] = "xueyouhu@gmail.com"
app.config["MAIL_PASSWORD"] = "Tigerhu123"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True  # Use SSL for security

mail = Mail(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from . import admin, forms, models, routes
