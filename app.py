from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- Основной маршрут для корневого URL ---
@app.route('/')
def home():
    return "Welcome to the Expense Tracker API!"

# --- Остальные маршруты (пользователи, категории и записи) ---
users = []
categories = []
records = []

@app.route('/user', methods=['POST'])
def create_user():
    user = request.json
    user['id'] = len(users) + 1
    users.append(user)
    return jsonify(user), 201

@app.route('/user/<int:user_id>', methods=['GET', 'DELETE'])
def manage_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if request.method == 'GET':
        return jsonify(user)
    users.remove(user)
    return '', 204

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/category', methods=['POST'])
def create_category():
    category = request.json
    category['id'] = len(categories) + 1
    categories.append(category)
    return jsonify(category), 201

@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(categories)

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = next((c for c in categories if c['id'] == category_id), None)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    categories.remove(category)
    return '', 204


# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')