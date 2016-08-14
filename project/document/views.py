# project/document/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import current_user, login_required

from project.models import Document, User
# from project.email import send_email
from project import db, bcrypt
from .forms import DocumentForm
import json
import simplejson

################
#### config ####
################

document_blueprint = Blueprint('document', __name__,)


################
#### routes ####
################

@document_blueprint.route('/documents', methods=['POST', 'PUT'])
@login_required
def new():
    form = DocumentForm(request.form)
    user = User.query.filter_by(email=current_user.email).first()
    if user:
        if request.method == 'PUT':
            id = request.form["id"]
            notes = request.form["notes"]
            document = Document.query.filter_by(id=id).update({"notes": notes, "editor_id": user.id})
            db.session.commit()
            result = {
                'success': True,
                'data': Document.query.get(id).serialize()
            }
        elif form.validate_on_submit():
            document = Document(
                title=form.title.data,
                subtitle=form.subtitle.data,
                notes=form.notes.data,
                author_id=user.id,
                editor_id=user.id
            )
            db.session.add(document)
            db.session.commit()
            result = {
                'success': True,
                'data': document.serialize()
            }
        else:
            result = {
                'success': False,
                'message': 'Create document was unsuccessful'
            }
    else:
        result = {
            'success': False,
            'message': 'Create document was unsuccessful'
        }
    return simplejson.dumps(result)

@document_blueprint.route('/documents/<id>', methods=['GET'])
@login_required
def show(id):
    document=Document.query.get(id)
    result = {
        'success': True,
        'data': document.serialize()
    }
    return simplejson.dumps(result)

@document_blueprint.route('/documents', methods=['GET'])
@login_required
def index():
    rows=Document.query.all()
    return render_template('document/index.html', rows=rows)

@document_blueprint.route('/documents/list', methods=['GET'])
@login_required
def list():
    rows=Document.query.all()
    result = {
        'success': True,
        'data': [i.serialize() for i in rows]
    }
    return simplejson.dumps(result)