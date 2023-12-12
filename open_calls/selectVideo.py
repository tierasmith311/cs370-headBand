from flask import jsonify
from flask_json import json_response
import sqlite3
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

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

def train_model(conn):
    try:
        query = 'SELECT * FROM UserPreferences'
        df = pd.read_sql_query(query, conn)

        # Data Preprocessing
        X = df[['Rating', 'LikeVideoCount', 'DislikeVideoCount']]  # Add other relevant features
        y = df['Selected']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model Selection and Training
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Model Evaluation
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")

        return model
    except Exception as e:
        print(f"Error training model: {e}")
        return None
    
def select_video(model, input_data):
    # Replace this with your logic for selecting the next video based on the trained model
    # input_data represents the features for a particular video
    # You can use the model.predict() method to make predictions

    # For demonstration, let's assume a simple logic where we predict based on a threshold
    if model.predict([input_data[['Rating', 'LikeVideoCount', 'DislikeVideoCount']]])[0] == 1:
        return {"message": "Video selected based on the model"}
    else:
        return {"message": "Video not selected based on the model"}

def handle_request():
    try:
        conn = sqlite3.connect("math_content.db")
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM UserPreferences')
        df = pd.read_sql_query(cursor, conn)

        # Train the model
        model = train_model(df)

        # Select the next video based on the model
        selected_video = select_video(model, df.iloc[0])  # Assuming df.iloc[0] is the first row for demonstration

        return jsonify(selected_video)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        conn.close()
