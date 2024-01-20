import os
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.security import generate_password_hash

from . import app, db
from .models import Event, EventRegistration, User


class MyAdminIndexView(AdminIndexView):
    """Create customized index view class"""
    def is_accessible(self):
        return current_user.is_authenticated


def create_admin_user():
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_password = os.environ.get('ADMIN_PASSWORD', '12345')
    # Check if admin user exists
    admin_user = User.query.filter_by(username=admin_username).first()
    if not admin_user:
        # Create an admin user (make sure to hash the password, never store it in plain text)
        hashed_password = generate_password_hash(admin_password, method='sha256')
        new_admin = User(username=admin_username, email='houstonastrorobotics@gmail.com', password_hash=hashed_password, is_admin=True)
        db.session.add(new_admin)
        db.session.commit()


# Initialize Flask-Admin
admin = Admin(app, name="Astro", template_mode="bootstrap3", index_view=MyAdminIndexView())
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(EventRegistration, db.session))
admin.add_view(ModelView(User, db.session))

