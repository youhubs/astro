from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from . import app, db
from .models import Event, Student, Registration

# Initialize Flask-Admin
admin = Admin(app, name="Astro", template_mode="bootstrap3")
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Registration, db.session))
