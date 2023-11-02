from flask import request, g, render_template, url_for, redirect
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import sqlite3
import bcrypt
from tools.logging import logger
from werkzeug.security import generate_password_hash, check_password_hash
def handle_request():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        salted = bcrypt.hashpw( bytes(password,  'utf-8' ) , bcrypt.gensalt(10))
        print(salted)
        connection = sqlite3.connect('UserAccounts.db')
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
            user = cursor.fetchone()
        except sqlite3.Error as e:
            print("Error executing SQL query:", e)
            user = None
        finally:
            connection.close()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user[2]):
                print("Login successful")
            else:
                print("Password is incorrect")
        else:
            print("user doesnt exist")
    return redirect('/static/homePage.html')
    #logger.debug("Login Handle Request")
    #use data here to auth the user

    #password_from_user_form = request.form['password']
    #user = {
     #       "sub" : request.form['firstname'] #sub is used by pyJwt as the owner of the token
     #      }
    #if not user:
    #    return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

    #return json_response( token = create_token(user) , authenticated = True)

#json