from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields, ValidationError
from datetime import datetime
import os

app = Flask(__name__)

# Load configuration from file
app.config.from_pyfile('config.py', silent=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    records = db.relationship("Record", backref="user", lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(10), nullable=False, default='global')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    records = db.relationship("Record", backref="category", lazy=True)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

# Marshmallow Schemas
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(dump_only=True)
    user_id = fields.Int(dump_only=True)

class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)

# Error handling
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(e.messages), 400

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

# Endpoints
user_schema = UserSchema()
category_schema = CategorySchema()
record_schema = RecordSchema()

@app.route('/')
def home():
    return "IO-22 Shmatko Denys API!"

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    try:
        user_data = user_schema.load(data)
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

@app.route('/user/<int:user_id>', methods=['GET', 'DELETE'])
def manage_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return user_schema.dump(user)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True))

@app.route('/category', methods=['POST'])
def create_category():
    data = request.json
    try:
        category_data = category_schema.load(data)
        new_category = Category(**category_data)
        db.session.add(new_category)
        db.session.commit()
        return category_schema.dump(new_category), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

@app.route('/category', methods=['GET'])
def get_categories():
    user_id = request.args.get('user_id', type=int)
    if user_id:
        categories = Category.query.filter((Category.type == 'global') | (Category.user_id == user_id)).all()
    else:
        categories = Category.query.all()
    return jsonify(category_schema.dump(categories, many=True))

@app.route('/category/<int:category_id>', methods=['GET', 'DELETE'])
def manage_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'GET':
        return category_schema.dump(category), 200
    db.session.delete(category)
    db.session.commit()
    return '', 204

@app.route('/record', methods=['POST'])
def create_record():
    data = request.json
    try:
        record_data = record_schema.load(data)
        new_record = Record(**record_data)
        db.session.add(new_record)
        db.session.commit()
        return record_schema.dump(new_record), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

@app.route('/record/<int:record_id>', methods=['GET', 'DELETE'])
def manage_record(record_id):
    record = Record.query.get_or_404(record_id)
    if request.method == 'GET':
        return record_schema.dump(record)
    db.session.delete(record)
    db.session.commit()
    return '', 204

@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    query = Record.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter_by(category_id=category_id)
    records = query.all()
    return jsonify(record_schema.dump(records, many=True))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')