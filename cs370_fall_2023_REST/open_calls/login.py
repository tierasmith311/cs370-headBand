from flask import request, g, render_template, url_for, redirect
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import sqlite3
from tools.logging import logger
from werkzeug.security import generate_password_hash, check_password_hash
def handle_request():
    print("you have successfully logged in")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = sqlite3.connect('UserAccounts.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=?', (username,))
        user = cursor.fetchone()
        connection.close()
        if user and check_password_hash(user[2], password):
            print("you have successfully logged in")
        else:
            print("user doesnt exist")
    return render_template('login.html')
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