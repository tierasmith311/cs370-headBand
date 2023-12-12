from flask import Flask, request, jsonify
import sqlite3


# Assuming you have a table named 'UserPreferences'
# Modify the SQL statement based on your table structure
def remove_topic(user_id, topic):
    try:
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()

        # Assuming you have a table named 'UserPreferences' with 'UserID' and 'Topics' columns
        cursor.execute('DELETE FROM UserPreferences WHERE UserID = ? AND Topics = ?', (user_id, topic))
        conn.commit()

        return {"message": f"Topic '{topic}' removed successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

def remove_topic_route():
    try:
        user_id = request.json.get('user_id')
        topic = request.json.get('topic')

        if not user_id or not topic:
            return jsonify({"error": "Both user_id and topic are required"}), 400

        result = remove_topic(user_id, topic)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# hi michelle

# for the project

# are you doing the written format