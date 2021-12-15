from db import *
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, make_response, Blueprint
from flask_cors import cross_origin
import sys

sys.path.append("../")

profiles_api = Blueprint("profiles", __name__)

# @profiles_api.route("/")
# def hello():
#     return "Hello here are the users"

@profiles_api.route("", methods=["GET"])
@cross_origin()
def get_profiles():
        try:
            userID = request.args.get("userID")
        except Exception as e:
            return {"err": "Invalid user id", "status": "failed"}, 400

        if not userID:
            try:
                data = list(db.Profiles.find({},{"_id": 0}).sort("block", 1))
                response = {"status": "success", "data": data}
            except Exception as e:
                print(e)
                return {"err": str(e), "status": "failed"}, 400
            
        else:
            try:
                data = db.Profiles.find_one({"userID": userID}, {"_id" : 0})
            except Exception as e:
                return {"err": str(e), "status": "failed"}, 400

            if data == None:
                return {"err": "No such profile", "status": "failed"}, 400

            response = {"status": "success", "data": data}
        
        return make_response(response)
    

@profiles_api.route("/edit", methods=["PUT"])
@cross_origin()
def edit_profile():

    data = request.get_json()
    userID = request.args.get("userID")
    oldUser = db.Profiles.find_one({"userID": userID})

    if not userID:
        return {"err": "No such user", "status": "failed"}, 400

    current_userID = db.Session.find_one({})["userID"]

    if current_userID != userID:
        return make_response({'message': "Invalid user", "status" : "failed"}, 200)
    
    userName = str(data.get('userName')) if data.get('userName') else oldUser.get('userName')
    room = str(data.get('room')) if data.get('room') else oldUser.get('room')
    telegramHandle = str(data.get('telegramHandle')) if data.get('telegramHandle') else oldUser.get('telegramHandle')
    profilePictureURI = str(data.get("profilePictureURI")) if data.get("profilePictureURI") else oldUser.get("profilePictureURI")

    body = {
        "userID": userID,
        "userName": userName,
        "room": room,
        "telegramHandle": telegramHandle,
        "profilePictureURI": profilePictureURI
    }

    result = db.Profiles.update_one({"userID": userID }, {'$set': body})
    if int(result.matched_count) > 0:
        return make_response({'message': "Profile updated"}, 200)
    else:
        return make_response({'err': "Profile not updated"}, 204)




    