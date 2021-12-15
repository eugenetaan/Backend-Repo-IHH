from db import *
from flask import Flask, jsonify, request, make_response
from flask_cors import cross_origin
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
@cross_origin()
def hello():
    return "Hello World"


@auth_api.route("/register", methods=["POST"])
@cross_origin()

def register():
    formData = request.get_json()
    try:
        if formData:
            userID = formData["userID"]
            passwordHash = formData["passwordHash"]
            email = formData["email"]
            userName = formData["useryName"]
            room = formData["room"]
            telegramHandle = formData["telegramHandle"]
            userPhoto = formData.get("userPhoto") if formData.get("userPhoto") else "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=identicon"
    except:
        return jsonify({"message": "bad request", "status": "failure"})


    # DB uses userID as unique index so check if already inside
    if list(db.Users.find({"userID": userID})) or list(db.Profiles.find({"userID": userID})):
        return jsonify({"message": "User Already Registered", "status": "failure"}), 400
    
    db.Users.insert_one({"userID": userID,
                        "passwordHash": passwordHash,
                        "email": email,
                        })
    db.Profiles.insert_one({"userID": userID,
                            "userName": userName,
                            "room": room,
                            "telegramHandle": telegramHandle,
                            # default photo is below
                            "profilePictureURI": userPhoto
                            })

    return jsonify({"message": "User successfully registered", "status": "success"})


@auth_api.route('/login', methods=['POST'])
@cross_origin()
def login():
    credentials = request.get_json()
    userID = credentials['userID']
    passwordHash = credentials['passwordHash']

    if not list(db.Users.find({'userID': userID, 'passwordHash': passwordHash})):
        return jsonify({'message': 'Invalid credentials'}), 403

    db.Session.update({'userID': userID, 'passwordHash': passwordHash}, {'$set': {
                      'userID': userID, 'passwordHash': passwordHash, 'createdAt': datetime.datetime.now()}}, upsert=True)

    token = jwt.encode({'userID': userID,
                        'passwordHash': passwordHash  # to change timedelta to 15 minutes in production
                        }, current_app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token}), 200


@auth_api.route('/logout', methods=['GET'])
@cross_origin()
def logout():
    userID = request.args.get('userID')
    try:
        db.Session.remove({"userID": userID})
    except:
        return jsonify({'message': 'An error occurred'}), 500
    return jsonify({'message': 'You have been successfully logged out'}), 200






# Form Data Example
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
