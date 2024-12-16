
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from passlib.hash import pbkdf2_sha256
from marshmallow import Schema, fields, ValidationError
import os


app = Flask(__name__)

# Конфігурація
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "jose"  # Секретний ключ JWT


db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# JWT обробники помилок
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}), 401

# Моделі
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Перевірте цей рядок

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

# Marshmallow Схеми
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(load_only=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()

class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)


user_schema = UserSchema()
category_schema = CategorySchema()
record_schema = RecordSchema()

# Ендпоінти
@app.route('/')
def home():
    return "IO-22 Shmatko Denys API!"


# Реєстрація користувача
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user_data = user_schema.load(data)
    if User.query.filter_by(email=user_data["email"]).first():
        return jsonify({"error": "User already exists"}), 400
    new_user = User(name=user_data["name"], email=user_data["email"], password=pbkdf2_sha256.hash(user_data["password"]))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Логін користувача
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get("email")).first()
    if user and pbkdf2_sha256.verify(data.get("password"), user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"error": "Invalid email or password"}), 401

# Отримання всіх користувачів
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True)), 200

# Видалення користувача
@app.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


# Створення категорії
@app.route('/category', methods=['POST'])
@jwt_required()
def create_category():
    data = request.json
    category_data = category_schema.load(data)
    new_category = Category(**category_data)
    db.session.add(new_category)
    db.session.commit()
    return jsonify(category_schema.dump(new_category)), 201

# Отримання всіх категорій
@app.route('/category', methods=['GET'])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify(category_schema.dump(categories, many=True)), 200

# Видалення категорії
@app.route('/category/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200


# Створення запису
@app.route('/record', methods=['POST'])
@jwt_required()
def create_record():
    data = request.json
    record_data = record_schema.load(data)
    new_record = Record(**record_data)
    db.session.add(new_record)
    db.session.commit()
    return jsonify(record_schema.dump(new_record)), 201

# Отримання всіх записів
@app.route('/record', methods=['GET'])
@jwt_required()
def get_records():
    records = Record.query.all()
    return jsonify(record_schema.dump(records, many=True)), 200

# Видалення запису
@app.route('/record/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_record(record_id):
    record = Record.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')