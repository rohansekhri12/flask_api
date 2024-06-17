from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with a random secret key
jwt = JWTManager(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.new_database
users_collection = db.user_info  # Collection for storing user information
authen_user_collection = db.authen_user  # Collection for storing user credentials

# User registration
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    if authen_user_collection.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 400
    authen_user_collection.insert_one({'username': username, 'password': password})
    return jsonify({'message': 'User registered successfully'}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = authen_user_collection.find_one({'username': username})
    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify(access_token=access_token)

# CRUD operations for users
@app.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    result = users_collection.insert_one(data)
    return jsonify({'message': 'User created successfully', 'id': str(result.inserted_id)}), 201

@app.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    if result.matched_count:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = list(users_collection.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
