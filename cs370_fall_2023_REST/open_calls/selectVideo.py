from flask import request, g, render_template, url_for, redirect
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import sqlite3
from tools.logging import logger
from werkzeug.security import generate_password_hash, check_password_hash

def handle_request():
    print("select video is being called")
    conn = sqlite3.connect("tools/math_content.sql")

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "Entertainment Content - Sheet1" WHERE Slime = ?', ('SomeValue',))

    url = cursor.fetchone()
    conn.close()
    if url:
        print("video has chosen successfully")
        print(url[0])
        return json_response(url[0])
    else:
        return json_response({"error" : "no video found"})
