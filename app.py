from flask import Flask, request, jsonify
from .config import Config
from flask_jwt_extended import JWTManager, jwt_required
from datetime import datetime
from .extension import db
from .model import User, Task, Log
from json import dumps

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

jwt = JWTManager(app)
client = app.test_client()


@app.route('/register', methods=['POST'])
def create_user():
    params = request.get_json()
    user = User(login=params.get('login'),
                password=params.get('password'))
    try:
        db.session.add(user)
        db.session.commit()
        token = user.get_token()
        return jsonify(msg='User successfully created',
                       user_login=user.login,
                       access_token=token), 201
    except AssertionError as exception_message:
        return jsonify(msg=f'Error: {exception_message}'), 400


@app.route('/login', methods=['POST'])
def login():
    params = request.get_json()
    try:
        user = User.authenticate(login=params.get('login'),
                                 password=params.get('password'))
        token = user.get_token()
        return jsonify(user_login=user.login,
                       access_token=token), 200
    except AssertionError as error_message:
        return f'Error: {error_message}', 400


# headers={'Authorization': f'Bearer {token}'} json={...}


@app.route('/get_tasks', methods=['GET'])
@jwt_required
def get_user_task():
    params = request.get_json()
    field_name = params.get('field_name', None)
    user = User.query.filter(User.login == params.get('username')).first()

    if not user:
        return {'message': 'No user with this username.'}, 400

    if field_name == 'status':
        user_task = Task.query.filter(Task.user_id == user.id).order_by(Task.status).all()
    elif field_name == 'finishdate':
        user_task = Task.query.filter(Task.user_id == user.id).order_by(Task.finishdate).all()
    else:
        user_task = Task.query.filter(Task.user_id == user.id).all()

    return jsonify([usr_tsk.serialize for usr_tsk in user_task]), 200


@app.route('/add_task', methods=['POST'])
@jwt_required
def add_user_task():
    params = request.get_json()
    username = params.get('username')
    user = User.query.filter(User.login == username).first()
    if not user:
        return {'message': 'No user with this username.'}, 400
    user_id = user.id
    name = params.get('name', '')
    description = request.args.get('description', 'Здесь будет описание')
    status = params.get('status', 1)

    if params.get('finishdate'):
        temp = params.get('finishdate')
        year = int(temp['year']) if temp.get('year') else None
        month = int(temp['month']) if temp.get('month') else None
        day = int(temp['day']) if temp.get('day') else None
        hour = int(temp['hour']) if temp.get('hour') else 0
        minute = int(temp['minute']) if temp.get('minute') else 0
        second = int(temp['second']) if temp.get('second') else 0

        date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        finishdate = dumps(date, default=str)
    else:
        finishdate = None

    add_new_task = Task(user_id=user_id,
                        name=name,
                        description=description,
                        status=status,
                        finishdate=finishdate
                        )

    add_log = Log(user_id=user_id,
                  time=datetime.utcnow(),
                  method='add new task',
                  changes=dumps(dict(name=name,
                                     description=description,
                                     status=status,
                                     finishdate=finishdate
                                     )
                                )
                  )

    try:
        db.session.add(add_new_task)
        db.session.add(add_log)
        db.session.commit()
        return jsonify(task=add_new_task.serialize), 201

    except AssertionError as exception_message:
        return jsonify(msg=f'Error: {exception_message}'), 400


@app.route('/edit_task', methods=['PUT'])
@jwt_required
def edit_user_task():
    params = request.get_json()
    username, task_id = params.get('username'), params.get('task_id')
    user = User.query.filter(User.login == username).first()
    user_id = user.id
    edit_task = Task.query.filter(Task.user_id == user_id,
                                  Task.id == task_id).one()
    log_storage = {}
    if params.get('name'):
        edit_task.name = params.get('name')
        log_storage['log_task_name'] = edit_task.name
    if params.get('description'):
        edit_task.description = params.get('description')
        log_storage['log_task_description'] = edit_task.description
    # status must be digit in right value - 1, 2, 3, 4
    if params.get('status'):
        edit_task.status = params.get('status')
        log_storage['log_task_status'] = edit_task.status
    # request.json.finishdate - must be json or dict, contains key: year, month, day, hour, minute
    if params.get('finishdate'):
        temp = params.get('finishdate')
        year = int(temp['year']) if temp.get('year') else None
        month = int(temp['month']) if temp.get('month') else None
        day = int(temp['day']) if temp.get('day') else None
        hour = int(temp['hour']) if temp.get('hour') else 0
        minute = int(temp['minute']) if temp.get('minute') else 0
        second = int(temp['second']) if temp.get('second') else 0

        added_time = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

        if edit_task.createdate > added_time:
            return jsonify(msg=f'Error: finish_time must be > created_time'), 400

        edit_task.finishdate = dumps(added_time, default=str)

        log_storage['log_task_finishdate'] = edit_task.finishdate

    # add check for change value and add only changed value
    add_log = Log(user_id=user_id,
                  time=datetime.utcnow(),
                  method='edit task',
                  changes=dumps(dict(name=log_storage.get('log_task_name'),
                                     description=log_storage.get('log_task_description'),
                                     status=log_storage.get('log_task_status'),
                                     finishdate=log_storage.get('log_task_finishdate')
                                     )
                                ))
    try:
        db.session.add(edit_task)
        db.session.add(add_log)
        db.session.commit()
        return jsonify(task=edit_task.serialize), 200

    except AssertionError as error_message:
        return f'Error: {error_message}', 400


@app.route('/view_log', methods=['GET'])
@jwt_required
def log_view():
    username = request.get_json().get('username')
    user = User.query.filter(User.login == username).first()
    user_id = user.id
    user_log = Log.query.filter(Log.user_id == user_id).all()
    return jsonify([user_lg.serialize for user_lg in user_log]), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')
