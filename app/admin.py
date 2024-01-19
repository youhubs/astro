import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash

from . import app, db
from .models import Event, Student, Registration, User

# Initialize Flask-Admin
admin = Admin(app, name="Astro", template_mode="bootstrap3")
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Registration, db.session))
admin.add_view(ModelView(User, db.session))


def create_admin_user():
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_password = os.environ.get('ADMIN_PASSWORD', '12345')
    # Check if admin user exists
    admin_user = User.query.filter_by(username=admin_username).first()
    if not admin_user:
        # Create an admin user (make sure to hash the password, never store it in plain text)
        hashed_password = generate_password_hash(admin_password, method='sha256')
        new_admin = User(username=admin_username, password_hash=hashed_password, is_admin=True)
        db.session.add(new_admin)
        db.session.commit()



