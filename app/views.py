from app import app, lm
from flask import render_template, redirect, url_for, g,flash, request, abort
from .forms import LoginForm
from .models import *
from flask_login import current_user,login_required,logout_user,login_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Index')


@lm.user_loader
def load_user(id):
    u = User.loadUserByID(id)
    return u

@app.before_request
def before_request():
    g.user = current_user

def checkedUser(userName, passHash):
    u = None
    u = User.query.filter_by(username=userName).first()
    if u is not None and u.password == passHash:
        return u
    else:
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = checkedUser(form.user_name.data, getHashedPass(form.password.data))
        if  u is not None:
            login_user(u, form.remember_me)
            return redirect(url_for('index'))
        else:
            flash("Invalid user name or password")
    return render_template('login.html',
                           title='Sign In',
                           form=form)

def getHashedPass(password):
    return password

@app.route('/device_login/<user>/<regid>', methods=['POST'])
def updateRegID(user, regid):
    json = request.get_json(force=True)
    if json is None:
        abort(500)
    else:
        u = User.query.filter_by(username=user).first()
        if u is None:
            abort(404)
        di = DeviceInfo.query.filter_by(user_id=u.id, regid=regid).first()
        if di is not None:
            return '', 304
        if not json.has_key('device_name') or not json.has_key('device_manufacture'):
            abort(500)
        device_name = json['device_name']
        device_manufacture =  json['device_manufacture']
        user_id = u.id
        di = DeviceInfo(regid, user_id, device_name, device_manufacture, None)
        if json.has_key('imei'):
            di.device_imei = json['imei']
        db.session.add(di)
        db.session.commit()
        login_user(u)
        return '', 200
