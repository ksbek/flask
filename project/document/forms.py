# project/document/forms.py


from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from project.models import Document

class DocumentForm(Form):
    title = TextField(
        'title',
        validators=[DataRequired()])
    subtitle = TextField(
        'subtitle',
        validators=[DataRequired()])
    notes = TextField(
        'notes',
        validators=[DataRequired()])
