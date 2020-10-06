from .app import client
# test for CLEAR DB or TEST DB !


def test_create_user():
    user_login = 'test_user'
    user_password = 'blablabla'

    new_user = client.post('/register', json={'login': user_login,
                                              'password': user_password})
    assert new_user._status_code == 201
    assert new_user.json.get('access_token') is not None
    assert new_user.json.get('user_login') == user_login


def test_login_user():
    user_login = 'test_user'
    user_password = 'blablabla'

    login = client.post('/login', json={'login': user_login,
                                        'password': user_password})
    assert login._status_code == 200
    assert login.json.get('access_token') is not None
    assert login.json.get('user_login') == user_login
    assert login.headers["Content-Type"] == "application/json"


def test_create_task():
    user_login = 'test_user'
    user_password = 'blablabla'
    new_user = client.post('/login', json={'login': user_login,
                                           'password': user_password})
    token = new_user.json.get('access_token')
    header_token = f'Bearer {token}'
    new_task = client.post('/add_task', json={'username': user_login,
                                              'name': 'TEST TASK',
                                              'description': 'MY BEAUTY TEST',
                                              'status': 4,
                                              'finishdate': {'year': 2020,
                                                             'month': '10',
                                                             'day': 7,
                                                             'hour': 20,
                                                             'minute': 30}},
                           headers={'Authorization': header_token})
    assert new_task._status_code == 201
    assert new_task.json.get('msg') is None


def test_get_task():
    user_login = 'test_user'
    user_password = 'blablabla'
    new_user = client.post('/login', json={'login': user_login,
                                           'password': user_password})
    token = new_user.json.get('access_token')
    header_token = f'Bearer {token}'

    get_task = client.get('/get_tasks', headers={'Authorization': header_token},
                          json={'username': user_login})
    assert get_task._status_code == 200
    assert get_task.headers["Content-Type"] == "application/json"


def test_edit_task():
    user_login = 'test_user'
    user_password = 'blablabla'
    new_user = client.post('/login', json={'login': user_login,
                                           'password': user_password})
    token = new_user.json.get('access_token')
    header_token = f'Bearer {token}'

    edit_task = client.put('/edit_task',headers={'Authorization': header_token},
                           json={'username': user_login, 'task_id': 1, 'finishdate': {'year': 2020,
                                                                                      'month': '10',
                                                                                      'day': 7,
                                                                                      'hour': 20,
                                                                                      'minute': 30}})
    assert edit_task._status_code == 500


def test_view():
    user_login = 'test_user'
    view = client.get('/view_log', json={'username': user_login})
    assert view._status_code == 200
