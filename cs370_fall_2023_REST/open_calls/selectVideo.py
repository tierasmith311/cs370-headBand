from flask import request, g, render_template, url_for, redirect
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import sqlite3
from tools.logging import logger
from werkzeug.security import generate_password_hash, check_password_hash

def handle_request():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute()#this is where i have to use SELECT from the database
    video = cursor.fetchone()
    connection.close()
