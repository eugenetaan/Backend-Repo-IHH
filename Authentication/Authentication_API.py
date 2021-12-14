from db import *
from flask import Flask, jsonify, request, make_response
import sys
import jwt
import datetime
import pymongo
from functools import wraps
from flask import Blueprint
from flask import current_app

sys.path.append("../")

auth_api = Blueprint("auth", __name__)

@auth_api.route("/")
def hello():
    return "Hello World"


@auth_api.route("/register", methods=["POST"])

def register():
    formData = request.get_json()
    try:
        if formData:
            userID = formData["userID"]
            passwordHash = formData["passwordHash"]
            email = formData["email"]
            displayName = formData["displayName"]
            room = formData["room"]
            telegramHandle = formData["telegramHandle"]
    except:
        return jsonify({"message": "bad request", "status": "failure"})
    
    db.Users.insert_one({"userID": userID,
                        "passwordHash": passwordHash,
                        "email": email,
                        })
    db.Profiles.insert_one({"userID": userID,
                            "displayName": displayName,
                            "room": room,
                            "telegramHandle": telegramHandle,
                            # default photo is below
                            "profilePictureURI": "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=identicon"
                            })

    return jsonify({"message": "User successfully registered", "status": "success"})


@auth_api.route('/login', methods=['POST'])

def login():
    credentials = request.get_json()
    userID = credentials['userID']
    passwordHash = credentials['passwordHash']

    if not db.Users.find({'userID': userID, 'passwordHash': passwordHash}).limit(1):
        return jsonify({'message': 'Invalid credentials'}), 403

    db.Session.update({'userID': userID, 'passwordHash': passwordHash}, {'$set': {
                      'userID': userID, 'passwordHash': passwordHash, 'createdAt': datetime.datetime.now()}}, upsert=True)

    token = jwt.encode({'userID': userID,
                        'passwordHash': passwordHash  # to change timedelta to 15 minutes in production
                        }, current_app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token}), 200


@auth_api.route('/logout', methods=['GET'])
def logout():
    userID = request.args.get('userID')
    try:
        db.Session.remove({"userID": userID})
    except:
        return jsonify({'message': 'An error occurred'}), 500
    return jsonify({'message': 'You have been successfully logged out'}), 200






#Form Data Example
# {
#     "userID": "A0XXXXXXE",
#     "passwordHash": "RandomStr",
#     "email": "eXXXXX@u.nus.edu",
#     "displayName": "UserName",
#     "room": "7-101",
#     "telegramHandle": "telehandle",
# }

#login data
# {
#     "userID": "A0XXXXXXE",
#     "passwordHash": "RandomStr",
# }
