from flask import request, g, render_template, redirect, url_for, session
from flask_json import FlaskJSON, JsonError, json_response, as_json, jsonify
from tools.token_tools import create_token
import sqlite3
import db_con
import bcrypt
from tools.logging import logger
import re

def handle_request():
    msg = ''
    if request.method == 'POST'and 'GET' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        salted = bcrypt.hashpw( bytes(password,  'utf-8' ) , bcrypt.gensalt(10))
        print(salted)
        email = request.form['email']
        conn = sqlite3.connect("UserAccounts.db")

        # Create the 'accounts' table if it doesn't exist
        db_con.create_accounts_table(conn)

        cursor = conn.cursor()
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, ?, ?, ?)', (username, salted, email,))
            conn.commit()
            return jsonify({'message' : 'new user created!'})
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return redirect('/static/homePage.html')
    