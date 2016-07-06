import traceback

from functools import wraps
from flask_login import login_user, logout_user, current_user, login_required
from flask import Flask, g, request, make_response, jsonify, render_template, session, redirect, url_for, send_from_directory, flash
from werkzeug import secure_filename

from ..lib import utils
from ..models import User, Role, Domain, DomainUser, Record, Server, History, Anonymous, Setting
from ..models2.DomainTemplate import *
from ..models2.DomainTemplateRecord import *

from ..views import *

@app.route('/templates', methods=['GET', 'POST'])
@app.route('/templates/list', methods=['GET', 'POST'])
@login_required
@admin_role_required
def templates():
    templates = DomainTemplate.query.all()
    return render_template('domaintemplate/list.html', templates=templates)

@app.route('/template/create', methods=['GET', 'POST'])
@login_required
@admin_role_required
def create_template():
    if request.method == 'GET':
        return render_template('domaintemplate/create.html')
    if request.method == 'POST':
        try:
            name = request.form.getlist('name')[0]
            description = request.form.getlist('description')[0]

            if ' ' in name or not name or not type:
                flash("Please correct your input", 'error')
                return redirect(url_for('create_template'))

            if DomainTemplate.query.filter(DomainTemplate.name == name).first():
                flash("A template with the name %s already exists!" % name, 'error')
                return redirect(url_for('create_template'))
            t = DomainTemplate(name=name,description=description)
            result = t.create()
            if result['status'] == 'ok':
                history = History(msg='Add domain template %s' % name, detail=str({'name': name, 'description': description}), created_by=current_user.username)
                history.add()
                return redirect(url_for('templates'))
            else:
                flash(result['msg'], 'error')
                return redirect(url_for('create_template'))
        except Exception, e:
            print traceback.format_exc()
            return redirect(url_for('error', code=500))
        return redirect(url_for('templates'))