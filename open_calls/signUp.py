from flask import request, jsonify, redirect
import sqlite3
import db_con
import bcrypt
from tools.logging import logger
import re

def handle_request():
    msg = ''
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        salted = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(10))
        print(salted)

        conn = sqlite3.connect("UserAccounts.db")
        cursor = conn.cursor()

        # Check if username or email already exists
        cursor.execute('SELECT * FROM accounts WHERE username = ? OR email = ?', (username, email))
        existing_account = cursor.fetchone()

        if existing_account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, ?, ?, ?, ?, ?)', (firstName, lastName, username, email, salted,))
            conn.commit()
            conn.close()
            return jsonify({'message': 'New user created!'})

    return redirect('/static/homePage.html')
