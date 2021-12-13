from db import *
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, make_response
from flask import Blueprint
import sys

sys.path.append("../db")

users_api = Blueprint("users", __name__)

users_api.route("/")
def hello():
    return "Hello here are the users"

users_api.route("/users", methods=["GET"])

def get_users():
        try:
            userID = request.args.get("userID")
        except Exception as e:
            return {"err": "Invalid user id", "status": "failed"}, 400

        if not userID:
            try:
                data = list(db.users.find({"_id": 0}).sort("block", 1))
                response = {"status": "success", "data": data}
            except Exception as e:
                print(e)
                return {"err": str(e), "status": "failed"}, 400
            
        else:
            try:
                data = list(db.users.find_one({"userID": userID}))
            except Exception as e:
                return {"err": str(e), "status": "failed"}, 400

            if len(data) == 0:
                raise Exception("User not found")

            response = {"status": "success", "data": data}
        
        return make_response(response)
    
    






