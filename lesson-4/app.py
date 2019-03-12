from flask import Flask, render_template, redirect
from flask import request, url_for, make_response, session
import sqlite3
import pandas as pd
import numpy as np
from collections import Counter
import time
from datetime import datetime
from uuid import uuid4

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
# sess = Session()

users = [
    {
        'username': 'alice',
        'password': 'aaaa'
    },
        {
        'username': 'bob',
        'password': 'bbbb'
    }
]

posts = [
    {
        'username': 'alice',
        'date': datetime.now(),
        'message': 'Hello World!' 
    }
]

fail_attempts = Counter()
ban_dict = {}

users_df = pd.DataFrame.from_dict(users)
posts_df = pd.DataFrame.from_dict(posts)

print (users_df)

with sqlite3.connect("users.db") as conn:
    users_df.to_sql('users', conn, index=False, if_exists='replace')
    posts_df.to_sql('posts', conn, index=False, if_exists='replace')

# df_from_db = pd.read_sql_query('select * from users', conn)
# print (df_from_db)

@app.route('/login')
def root():
    session['uuid'] = str(uuid4())
    if 'uname' in request.cookies:
        return render_template('welcome.html', username=request.cookies['uname'])
    return render_template('index.html', message='')

@app.route('/verify', methods=['POST'])
def login():
    print ('uuid', session['uuid'])
    if request.remote_addr in ban_dict:
        if ban_dict[request.remote_addr] > time.time() - 300:
            return render_template('index.html', message='You are banned!')
        else:
            del ban_dict[request.remote_addr]
            del fail_attempts[request.remote_addr]

    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember')
    session['username'] = username   
    print (username, password, remember)
    user_match = []
    ### read from list of dict
    # for user in users:
    #     if username == user['username'] and password == user['password']:
    #         user_match.append((username, password))

    # read from DB
    with sqlite3.connect("users.db") as conn:
        cur = conn.cursor()
        query = "select username, password from users u where u.username = '" + username + "' and u.password = '" + password + "'"
        print(query)
        cur.execute(query)
        user_match = cur.fetchall()

    ### read from DB with pandas
    # df = pd.read_sql_query('select * from users', conn)
    # user_match = df[(username == df['username']) & (password == df['password'])]
    
    if len(user_match) > 0:
        post_df = pd.read_sql_query('select * from posts', conn)
        resp = make_response(render_template('welcome.html', 
        username=username,
        tables=[post_df.to_html(classes='data')],
        titles=post_df.columns.values))
        if remember:
            resp.set_cookie('uname', username, 3600)
        return resp

    fail_attempts[request.remote_addr] += 1
    if fail_attempts[request.remote_addr] >= 5:
        ban_dict[request.remote_addr] = time.time()
    print (fail_attempts)
    print (ban_dict) 
    return render_template('index.html', message='Wrong username or password')

@app.route('/welcome')
def method_name():
   return 'WELCOME!'


@app.route('/post', methods=['POST'])
def post():
    message = request.form.get('message')
    print ('message:', message)
    with sqlite3.connect("users.db") as conn:
        cur = conn.cursor()
        query = "insert into posts (username, date, message) values (?, ?, ?)"
        print(query)
        cur.execute(query, (session['username'], datetime.now(), message))
        post_df = pd.read_sql_query('select * from posts', conn)
        print (post_df)
        resp = make_response(render_template('welcome.html',
        username=session['username'],
        tables=post_df.values,
        titles=post_df.columns.values))
    return resp
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)