from app import app, lm
from flask import render_template, redirect, url_for, g,flash, request, abort
from .forms import LoginForm ,RegisterForm
from .models import *
from flask_login import current_user,logout_user,login_user


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated() and not current_user.is_anonymous():
        return render_template('index.html', title='Index')
    else:
        return redirect('/login')


@lm.user_loader
def load_user(id):
    u = User.loadUserByID(id)
    return u

@app.before_request
def before_request():
    g.user = current_user

def checkedUser(userName, password):
    u = User.query.filter_by(username=userName).first()
    if u is not None and u.verifyPassword(password):
        return u
    else:
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = checkedUser(form.user_name.data, form.password.data)
        if  u is not None:
            login_user(u, form.remember_me)
            return redirect(url_for('index'))
        else:
            flash("Invalid user name or password")
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated() and not current_user.is_anonymous():
        logout_user()
        return redirect('login')
    else:
        abort(500)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.user_name.data).first()
        if u is not None:
            flash("User %s already exists" % form.user_name.data)
        elif form.password.data != form.retype_password.data:
            flash("password fields must match!")
        else:
            if current_user.is_authenticated() and not current_user.is_anonymous():
                logout_user()
                u = User(form.user_name.data, form.password.data)
                User.session.add(u)
                User.session.commit()
                login_user(u, remember=form.remember_me.data)
                return redirect(url_for('index'))
    return render_template('register.html', title='Please Register', form=form)


@app.route('/device_login/<user>/<regid>', methods=['POST'])
def updateRegID(user, regid):
    json = request.get_json(force=True)
    if json is None:
        abort(500)
    else:
        u = User.query.filter_by(username=user).first()
        if u is None:
            abort(404)
        if not json.has_key('pass'):
            return abort(500, "no password supplied")
        if u.password != getHashedPass(json['pass']):
            abort(401)
        di = DeviceInfo.query.filter_by(user_id=u.id, regid=regid).first()
        if di is not None:
            return '', 304
        if not json.has_key('device_name') or not json.has_key('device_manufacture'):
            abort(500, "no device name or device manufacture supplied")
        device_name = json['device_name']
        device_manufacture =  json['device_manufacture']
        user_id = u.id
        di = DeviceInfo(regid, user_id, device_name, device_manufacture, None)
        if json.has_key('imei'):
            di.device_imei = json['imei']
        db.session.add(di)
        db.session.commit()
        return '', 200
