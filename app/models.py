from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(64), unique=False)
    regid    = db.Column(db.String(10))
    devices  = db.relationship('DeviceInfo', backref = 'owner', lazy='dynamic')

    def __init__(self, name, password, regid):
        self.username = name
        self.password = password
        self.regid = regid

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def loadUserByID(cls, id):
        user = None
        if id is not None and id != '':
            user = cls.query.get(int(id))
        return user

    def __repr__(self):
        return '<User %r : %r>' % (self.username, self.regid)

class DeviceInfo(db.Model):
    regid = db.Column(db.String(10), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    device_name = db.Column(db.String(10),  nullable = False)
    device_manufacture = db.Column(db.String(10),  nullable = False)
    device_imei = db.Column(db.String(10))

    def __init__(self, regid, user_id, device_name, manufacture, imei):
        self.regid = regid
        self.user_id = user_id
        self.device_name = device_name
        self.device_manufacture = manufacture
        self.device_imei = imei

    def __repr__(self):
        return '<%r %r %r %r>' %(self.regid, self.device_manufacture, self.device_name, self.device_imei)

    def __str__(self):
        return '%r - %r \n%r' %(self.device_manufacture, self.device_name, self.device_imei)
