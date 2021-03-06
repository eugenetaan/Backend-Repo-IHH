from db import *
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, make_response, Blueprint
from flask_cors import cross_origin
import sys

sys.path.append("../")

users_api = Blueprint("users", __name__)

# @users_api.route("/")
# def hello():
#     return "Hello here are the users"

@users_api.route("", methods=["GET"])
@cross_origin()
def get_users():
        try:
            userID = request.args.get("userID")
        except Exception as e:
            return {"err": "Invalid user id", "status": "failed"}, 400

        if not userID:
            try:
                data = list(db.Users.find({}, {"_id" : 0 }))
                response = {"status": "success", "data": data}
            except Exception as e:
                print(e)
                return {"err": str(e), "status": "failed"}, 400
            
        else:
            print(2)
            try:
                data = db.Users.find_one({"userID": userID}, {"_id" : 0 })
                print(data)
            except Exception as e:
                print(e)
                return {"err": str(e), "status": "failed"}, 400

            
            if data == None:
                return {"err": "No such User", "status": "failed"}, 400

            
        
        return make_response(response)
    


@users_api.route("/current", methods=["GET"])
@cross_origin()

def get_current_user():
    
    sessionData = db.Session.find_one({})
    if sessionData:
        current_userID = sessionData["userID"]
    else:
        return {"err": "No User Logged In", "status": "failed"}
    
    response = {"status": "success", "userID": current_userID}
    return make_response(response, 200)









