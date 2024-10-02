import os
from flask import jsonify, send_from_directory
from . import app  # Імпортуємо змінну app

@app.route('/')
def index():
    return "Welcome to the Flask App!"

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')