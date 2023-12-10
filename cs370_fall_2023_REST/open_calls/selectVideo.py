from flask import request, g, render_template, url_for, redirect, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import sqlite3
import random
from tools.logging import logger
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, parse_qs
import pandas as pd


def get_embed_url(youtube_url):
    # Parse the original YouTube URL
    if youtube_url.startswith("https://youtu.be/"):
        # Split the URL by '/' and take the last part as the video ID
        parts = youtube_url.split('/')
        video_id = parts[-1]

        video_idParts = video_id.split('?')
        newVideo_id = video_idParts[0]

        if video_id:
            # Create the embed URL
            embed_url = f"https://www.youtube.com/embed/{newVideo_id}"
            return embed_url
    
    return None

# Example usage:
def select():
    conn = sqlite3.connect("math_content.db")
    sql_query = "SELECT * FROM your_table;"
    df = pd.read_sql(sql_query, conn)
    
    conn.close()
    
def handle_request():
    try:
        conn = sqlite3.connect("math_content.db")
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM math_content WHERE "3rdgrade" IS NOT NULL')
        sum_of_3rdgrade = cursor.fetchone()[0]

        if sum_of_3rdgrade > 0:
            random_number = random.randint(0, sum_of_3rdgrade - 1)  
            cursor.execute('SELECT "3rdgrade" FROM math_content;')
            url = cursor.fetchall()

            if 0 <= random_number < len(url):
                youtube_url = url[random_number][0]
                embed_url = get_embed_url(youtube_url)
                if embed_url:
                    return jsonify({"embed_url": embed_url})
            return jsonify({"error": "Invalid YouTube URL"})

        return jsonify({"error": "No video found"})
    except Exception as e:
        return jsonify({"error": "error!"})
    finally:
        cursor.close()
        conn.close()

