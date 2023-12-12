from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import sqlite3

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secret key
jwt = JWTManager(app)

def update_rating(user_id, content_id, rating):
    connection = sqlite3.connect('your_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO UserPreferences (UserID, ContentID, Rating)
        VALUES (?, ?, ?)
        ON CONFLICT(UserID, ContentID) DO UPDATE SET Rating = ?;
    ''', (user_id, content_id, rating, rating))
    connection.commit()
    connection.close()

@app.route('/open_api/updateRating', methods=['POST'])
@jwt_required()  # Requires a valid JWT for accessing this route
def update_rating_route():
    try:
        # Get the user_id from the JWT payload
        user_id = get_jwt_identity()['user_id']

        content_id = request.json.get('content_id')
        rating = request.json.get('rating')

        update_rating(user_id, content_id, rating)

        return jsonify({"message": "Rating updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
