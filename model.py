import bcrypt
import datetime
from .extension import db
from sqlalchemy.orm import validates
from flask_jwt_extended import create_access_token


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    logs = db.relationship('Log', backref='user', lazy=True)

    def __init__(self, login, password):
        self.login = login
        self.password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')

    def __repr__(self):
        return f"{self.id=} {self.login=} {self.password=}"

    def get_token(self, expire_time=24):
        expire_delta = datetime.timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, login, password):
        user = User.query.filter(User.login == login).first()
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise AssertionError("No user with this password")
        return user

    @validates('login')
    def validate_login(self, key, login):
        if not login:
            raise AssertionError('No login provided')

        usr = User.query.filter(User.login == login).first()

        if usr:
            raise AssertionError('Login is already in use')

        if len(login) < 5 or len(login) > 20:
            raise AssertionError('Login must be between 5 and 20 characters')

        return login

    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise AssertionError('Password not provided')

        if 8 > len(password) > 50:
            raise AssertionError('Password must be between 8 and 50 characters')

        return password

    @property
    def serialize(self):
        return {
            'login': self.login,
            'password': self.password
        }


class Task(db.Model):
    __tablename__ = 'task'
    CHOICE = {1: 'Новая',
              2: 'Запланированная',
              3: 'в Работе',
              4: 'Завершенная'
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text)
    createdate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    status = db.Column(db.String(64), nullable=False)
    finishdate = db.Column(db.DateTime)

    def __init__(self, user_id, name, description, status, finishdate):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.status = Task.CHOICE[int(status)]
        self.finishdate = datetime.datetime.fromisoformat(finishdate[1:-1]) if finishdate else None

    def __repr__(self):
        return f"{self.id=} {self.user_id} {self.name=} {self.createdate=}"

    @validates('user_id')
    def validate_user_id(self, key, user_id):
        if not user_id:
            return AssertionError('No user_id provided')

        if str(user_id).isalpha():
            return AssertionError('User_id must be digit')

        if not User.query.filter(User.id == user_id).first():
            return AssertionError('No user with this id')

        return user_id

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            return AssertionError('No name provided')
        if len(name) > 128:
            return AssertionError('Name must be lesser then 128')

        return name

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            return AssertionError('No description provided')

        return description

    @validates('status')
    def validates_status(self, key, status):
        if not status:
            return AssertionError('No status provide')
        if status not in ('Новая', 'Запланированная', 'в Работе', 'Завершенная'):
            return AssertionError('Status must be select in standard values')

        return status

    @property
    def serialize(self):
        return {
            'task_id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'createdate': self.createdate,
            'status': self.status,
            'finishdate': self.finishdate
        }


class Log(db.Model):
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    method = db.Column(db.Text, nullable=False)
    changes = db.Column(db.JSON, nullable=False)

    def __init__(self, user_id, time, method, changes):
        self.user_id = user_id
        self.time = time
        self.method = method
        self.changes = changes

    def __repr__(self):
        return f"{self.id=} {self.user_id} {self.time=} {self.method=} {self.changes=}"

    @validates('user_id')
    def validate_log_user_id(self, key, user_id):
        if not user_id:
            return AssertionError('No user_id provided')

        if not User.query.filter(User.id == user_id).first():
            return AssertionError('No user with this id')
        return user_id

    @validates('time')
    def validate_time(self, key, time):
        if not time:
            return AssertionError('No time provided')
        return time

    @validates('method')
    def validate_method(self, key, method):
        if not method:
            raise AssertionError('No method provided')
        return method

    @validates('changes')
    def validates_changes(self, key, changes):
        if not changes:
            AssertionError('No data provided')
        return changes

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'time': self.time,
            'method': self.method,
            'data': self.changes
        }

