WTF_CSRF_ENABLED = True
SECRET_KEY = '3427zcjk352jmfod772n3mldf7d72mnchgert'
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_DATABASE_URI = 'sqlite:////.test.db'