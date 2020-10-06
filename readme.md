**Install**

git clone https://github.com/SerSamyel/anna_test_api

**Run api**

python flask app.py run 

**Create user.**
Add new user in system and request authenticated token.

POST /register, json={'login':'user_one', 'password':'blabla'}

Response streamed [201 CREATED]
Headers([('Content-Type', 'application/json'), ('Content-Length', '312')])
{"access_token":"very long token", "msg":"User successfully created", "user_login":"user444"}

request:
login - must be between 5 and 20 characters
password - any, not empty

response:
token - access_token, default time to life 24 hours
user_login - login your user
msg - info message, error message

**Login user**
Update user token.

POST /login, json={'login': 'your_login', 'password': 'your_password'}

Response streamed [200 OK]
Headers([('Content-Type', 'application/json'), ('Content-Length', '312')])
{"access_token":"new token", "user_login":"user444"}


**Get user tasks**
Response json contained data: user_id, name, description, status, finishdate
Heed authorization with token in headers.
GET /get_tasks, json={'username':'user_one', 'field_name':'status'}, headers={'Authorization': f'Bearer {token}'}

Response streamed [200 OK]
Headers([('Content-Type', 'application/json'), ('Content-Length', '621')])
json = {{user_id, name, description, status, createdate, finishdate},... {user_id, name, description, status, finishdate}}

username - user, whose task will be shown
field_name - status, finishdate or None, ordered response for this field
name - Task name, must be string
status - Status task, must be integer - (1, Новая) (2, Запланированная), (3, в Работе), (4, Завершенная)
discription - Discription task, text
createdate - Date and time creation task
finishdate - date and time finishing task
    finishdate = {year=2000, month=12, day=31, hour=23, minute=59, second=second}
        hour, minute, second - default 0


**Create task.**
Create task for user. Need authorization.

POST /add_task 

json = {username, name, description, status, finishdate}

Response streamed [201 OK]
Headers([('Content-Type', 'application/json'), ('Content-Length', '621')])
json = {username, name, description, status, finishdate}


**Edit task.**
Edit task, heed authorization.

PUT /edit_task json = {username, task_id, name, description, status, finishdate}
    finishdate = {year=2000, month=12, day=31, hour=23, minute=59, second=second}

Response streamed [200 OK]
Headers([('Content-Type', 'application/json'), ('Content-Length', '621')])
json = {task_id, 'user_id' name description createdate status finishdate}


**Log.**
Action like POST and PUT - add oll sended data to table Log
user may send get request to response log data

GET /view_log json={username}

Response streamed [200 OK]
Headers([('Content-Type', 'application/json'), ('Content-Length', '1609')])
json = {{user_id, time, method, data}, ... {user_id, time, method, data}}
user_id - id for user in database
time - time create changes
method - post or edit
data = all data to change or add
    data = {name, description, status, finishdate}



**Errors.**
xxx - status code, exception_message - error description
200 - OK
400 - Bad Request
500 - Internal Server Error
msg=f'Error: {exception_message}', xxx

exception_message = {No login provided, Login is already in use,
                     Login must be between 5 and 20 characters,
                     Password not provided,
                     Password must be between 8 and 50 characters,
                     No user_id provided
                     etc...}