from flask import request, jsonify, redirect
import sqlite3
import jwt
import bcrypt
from tools.token_tools import create_token
from tools.logging import logger

def handle_request():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({"error": "Both username and password are required"}), 400

        connection = sqlite3.connect('UserAccounts.db')
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
                logger.info("Login successful")
                token = create_token(user)
                return jsonify({"token": token, "username": username})
            else:
                logger.warning("Incorrect username or password")
                return jsonify({"error": "Incorrect username or password"}), 401

        except sqlite3.Error as e:
            logger.error("Error executing SQL query: %s", e)
            return jsonify({"error": "Internal Server Error"}), 500

        finally:
            connection.close()

    return redirect('/static/homePage.html')

