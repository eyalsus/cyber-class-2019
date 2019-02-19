from flask import Flask, render_template, redirect, request, url_for
import sqlite3
import pandas as pd

app = Flask(__name__)

users = [
    {
        'username': 'alice',
        'password': '1234'
    }
]

df = pd.DataFrame.from_dict(users)

print (df)


conn = sqlite3.connect("users.db")
df.to_sql('users', conn, index=False, if_exists='replace')

df_from_db = pd.read_sql_query('select * from users', conn)
print (df_from_db)

@app.route('/login')
def root():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    print (username, password)
    for user in users:
        if username == user['username'] and password == user['password']:
            return render_template('welcome.html')
    return render_template('index.html')

@app.route('/welcome')
def method_name():
   return 'WELCOME!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)