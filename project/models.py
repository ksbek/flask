# project/models.py


import datetime

from project import db, bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, name, password, paid=False, admin=False):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'email': self.email
        }

    def __repr__(self):
        return self.name

class Document(db.Model):

    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    editor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, nullable=False)
    modified_on = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=False)

    author = relationship("User", foreign_keys="[Document.author_id]")
    editor = relationship("User", foreign_keys="[Document.editor_id]")

    def __init__(self, author_id, editor_id, title, subtitle, notes):
        self.author_id = author_id
        self.editor_id = editor_id
        self.title = title
        self.subtitle = subtitle
        self.notes = notes
        self.created_on = datetime.datetime.now()
        self.modified_on = datetime.datetime.now()

    def serialize(self):
        return {
            'id': self.id, 
            'title': self.title,
            'subtitle': self.subtitle,
            'notes': self.notes,
            'author': self.author.name,
            'editor': self.editor.name,
            'created_on': self.created_on.strftime('%d/%m/%Y'),
            'modified_on': self.modified_on.strftime('%d/%m/%Y')
        }