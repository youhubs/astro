from . import app, db
from flask_admin import Admin
from .models import Event, Student, Registration
from flask_admin.contrib.sqla import ModelView


# Initialize Flask-Admin
admin = Admin(app, name='Astro', template_mode='bootstrap3')
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Registration, db.session))
