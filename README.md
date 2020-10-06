**Install**

git clone https://github.com/SerSamyel/anna_test_api

**Run api**

python flask app.py run 

**Create user.**
+ul Add new user in system and request authenticated token.

POST /register      
    json={'login':'user_one', 'password':'blabla'}

    Response streamed [201 CREATED]
    Headers([('Content-Type', 'application/json'), ('Content-Length', '312')])
    json = {"access_token":"very long token", "msg":"User successfully created", "user_login":"user444"}

    login - must be between 5 and 20 characters
    password - any, not empty
    token - access_token, default time to life 24 hours
    user_login - login your user
    msg - error message

**Login user**
    Update user token.

POST /login        
    json={'login':'username', 'password':'user_password'}

    Response streamed [200 OK]
    Headers([('Content-Type', 'application/json'), ('Content-Length', '312')])
    json = {"access_token":"token", "user_login":"user"}


**Get user tasks**
    Response json contained data: user_id, name, description, status, finishdate
    Heed authorization with token in headers.

GET /get_tasks     
    json={'username':'username', 'field_name':'ordered_field'}, headers={'Authorization': f'Bearer {token}'}

    Response streamed [200 OK]
    Headers([('Content-Type', 'application/json'), ('Content-Length', '621')])
    json = {{user_id, name, description, status, createdate, finishdate},... {user_id, name, description, status, finishdate}}

    username - user, whose task will be shown
    field_name - status, finishdate or None, ordered response for this field
    name - Task name, must be string
    status - Status task, must be integer - (1, Новая) (2, Запланированная), (3, в Работе), (4, Завершенная)
    discription - Discription task, text
    createdate - Date and time creation task (added default, then task created)
    
    finishdate - date and time finishing task
    
        finishdate = {year=2000, month=12, day=31, hour=23, minute=59, second=second}
    
    hour, minute, second - default 0


**Create task.**
    Create task for user. Need authorization.

POST /add_task     
    json = {'username':''username, 'name':'task_name', 'description':'task desctiption', 'status':'integer with default', 'finishdate':{year, month, day, hour, minute, second}}

    Response streamed [201 OK]
    Headers([('Content-Type', 'application/json'), ('Content-Length', '621')])
    json = {username, name, description, status, finishdate}
    status - 1(New task), 2(Planned), 3(In work), 4(Complete)
    finishdate = {year, month, day, hour, minute, second}


**Edit task.**
    Edit task, heed authorization.

PUT /edit_task     
    json = {'username':'username', 'task_id':'task_id_int', 'name':'edit_name', 'description':'edit_desc', 'status':'edit_stat', 'finishdate':{year, month, day, hour, minute, second}}

    Response streamed [200 OK]
    Headers([('Content-Type', 'application/json'), ('Content-Length', '621')])
    json = {task_id, user_id, name, descriptio, createdate, status, finishdate}
    
    finishdate = {year, month, day, hour, minute, second}

**Log.**
    Action like POST and PUT - add oll sended data to table Log
    User may send get request to response log data

GET /view_log      
    json={'username':'username'}

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


**DB.**
IF your need to create db manually or use advanced functionality.

    Create a migration repository:
        python manage.py db init

    Generate an initial migration:
        python manage.py db migrate -m "Initial migration."
        
    Apply the migration to the database:
        python manage.py db upgrade
    
    Downgrade DB:
        python manage.py db downgrade
    
    Help:
        python manage.py db --help
        
