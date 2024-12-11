from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "IO-22 Shmatko Denys API!"

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
    # Если категория создается с user_id, она будет пользовательской
    if 'user_id' in category:
        category['type'] = 'user'
    else:
        category['type'] = 'global'
    categories.append(category)
    return jsonify(category), 201

@app.route('/category', methods=['GET'])
def get_categories():
    user_id = request.args.get('user_id')
    if user_id:
        user_id = int(user_id)
        filtered_categories = [c for c in categories if c['type'] == 'global' or c.get('user_id') == user_id]
        return jsonify(filtered_categories)
    return jsonify(categories)

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = next((c for c in categories if c['id'] == category_id), None)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    categories.remove(category)
    return '', 204

@app.route('/record', methods=['POST'])
def create_record():
    record = request.json
    record['id'] = len(records) + 1
    records.append(record)
    return jsonify(record), 201

@app.route('/record/<int:record_id>', methods=['GET', 'DELETE'])
def manage_record(record_id):
    record = next((r for r in records if r['id'] == record_id), None)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    if request.method == 'GET':
        return jsonify(record)
    records.remove(record)
    return '', 204

@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({'error': 'user_id or category_id parameter required'}), 400

    filtered_records = records
    if user_id:
        filtered_records = [r for r in filtered_records if r['user_id'] == int(user_id)]
    if category_id:
        filtered_records = [r for r in filtered_records if r['category_id'] == int(category_id)]

    return jsonify(filtered_records)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
