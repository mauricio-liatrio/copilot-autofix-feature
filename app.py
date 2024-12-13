from flask import Flask, request, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'sample.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
      
        query = f"SELECT * FROM users WHERE username = ? AND password = ?"
        print(f"Executing query for user: {username}")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return f"Welcome, {user[1]}!"
        else:
            return "Invalid username or password."

    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'])
