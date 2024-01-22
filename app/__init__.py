from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import DevelopmentConfig  # or another config depending on your environment

from app.session_service import init_session_lifetime

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize other extensions
init_session_lifetime(app)

# Import models, views, and other components
from . import forms, models, routes, admin
