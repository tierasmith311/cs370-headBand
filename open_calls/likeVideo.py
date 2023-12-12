from flask import request, g, render_template, url_for, redirect, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import sqlite3
import random
from tools.logging import logger
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, parse_qs

def update_like_count(user_id, content_id):
    connection = sqlite3.connect('your_database.db')
    cursor = connection.cursor()

    # Check if the user has preferences for the content
    cursor.execute('SELECT * FROM UserPreferences WHERE UserID = ? AND ContentID = ?', (user_id, content_id))
    existing_preference = cursor.fetchone()

    if existing_preference:
        # Update the LikeVideoCount in the existing preference
        cursor.execute('UPDATE UserPreferences SET LikeVideoCount = LikeVideoCount + 1 WHERE UserID = ? AND ContentID = ?', (user_id, content_id))
    else:
        # If the user does not have a preference for the content, insert a new row
        cursor.execute('INSERT INTO UserPreferences (UserID, ContentID, LikeVideoCount) VALUES (?, ?, 1)', (user_id, content_id))

    connection.commit()
    connection.close()


def like_video():
    try:
        # Assuming the user_id and content_id are sent in the request data
        user_id = request.json.get('user_id')
        content_id = request.json.get('content_id')

        # Perform the necessary actions to update the like count in the UserPreferences table
        update_like_count(user_id, content_id)

        return jsonify({"message": "Video liked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500