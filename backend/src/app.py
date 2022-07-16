
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
# Initialize the class Flask and Pymongo
app = Flask(__name__)
app.secret_key = 'mySecretkey'
app.config['MONGO_URI'] = 'mongodb://localhost/pythonMongodb'
mongodb = PyMongo(app)

db = mongodb.db.users


# Create user
@app.route('/users', methods=['POST'])
def createUsers():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongodb.db.users.insert_one(
            {
                'username': username,
                'email': email,
                'password': hashed_password
            }
        )
        response = jsonify({
            'id': str(id),
            'username': username,
            'email': email,
            'password': password
        })
        return response
    else:
        return not_found()
    return 'Create users'

# Read users

# Get users


@app.route('/users', methods=['GET'])
def getUsers():
    users = mongodb.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")

# Get a user


@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    user = mongodb.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


# Delete a user

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    mongodb.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User ' + id + 'was Deleted successfully'})
    return response

# Update a user


@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongodb.db.users.update_one({'_id':ObjectId(id)}, {'$set': {
            'username': username,
            'email': email,
            'password': hashed_password
        }})
        response = jsonify({'message': 'User'+ id + 'was updated succesfully'})
        response.status_code = 200
        return response
    else:
        return not_found()
        


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
