from flask import jsonify
from . import app  # Імпортуємо змінну app

@app.route('/')
def index():
    return "Welcome to the Flask App!"

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"})