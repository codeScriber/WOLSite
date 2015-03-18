from flask_wtf import Form
from wtforms import StringField, BooleanField,PasswordField
from app.customFieldsAndWidgets import StringFieldWithAF
from wtforms.validators import DataRequired

class LoginForm(Form):
    user_name = StringFieldWithAF('user_name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
