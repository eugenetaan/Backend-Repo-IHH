from db import *
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, make_response
from flask import Blueprint
import sys

sys.path.append("../db")

items_api = Blueprint("items", __name__)

items_api.route("/")
def hello():
    return "Here you can find all the items that other people are sharing!"

items_api.route('/items', methods=["GET", "POST"])

def all_items():

    if request.method == "GET":

        try:
            data = list(db.items.find({"_id": 0}).sort("itemID", 1))
            response = {"status": "success", "data": data}
        except Exception as e:
            print(e)
            return {"err": str(e), "status": "failed"}, 400
        return make_response(response)

    elif request.method == "POST":
        try:
            data = request.get_json()
        except Exception as e:
            print(e)
            return {"err": str(e), "status": "failed"}, 400

        itemID = str(data.get('itemID'))
        itemName = str(data.get('itemName'))
        description = str(data.get("description"))
        remarks = str(data.get("remarks"))
        userName = str(data.get('Lender'))
        userID = str(data.get("userID"))

        body = {
            "itemID": itemID,
            "itemName": itemName,
            "user": userName,
            "userID" : userID,
            "description" : description,
            "remarks" : remarks
        }

        receipt = db.User.insert_one(body)
        body["_id"] = str(receipt.inserted_id)

        return make_response({"message": body, "status": "success"}, 200)



items_api.route('/item', methods=["GET", "PUT", "DELETE"])

def item():

    if request.method == "GET":

        try:
            itemID = request.args.get("itemID")
        except Exception as e:
            return {"err": "Invalid item id", "status": "failed"}, 400

        try:
            data = list(db.items.find_one({"itemID": itemID}))
        except Exception as e:
            return {"err": str(e), "status": "failed"}, 400

        if len(data) == 0:
            raise Exception("Item not found")

        response = {"status": "success", "data": data}
        return make_response(response)
    
    elif request.method == "PUT":
        data = request.get_json()
        itemID = data.get('itemID')
        olditem = db.items.find_one({"itemID": itemID})
        
        try:
            data = list(db.items.find({"itemID": int(id)}, {"_id": 0}))
        except Exception as e:
            return {"err": str(e), "status": "failed"}, 400

        
        if len(data) == 0:
            raise Exception("Item not found")


        userID = str(data.get('userID')) if data.get('userID') else olditem.get('userID')
        userName = str(data.get('userName')) if data.get('userName') else olditem.get('userName')
        description = str(data.get('description')) if data.get('description') else olditem.get('description')
        itemName = int(data.get('itemName')) if data.get('itemName') else olditem.get('itemName')
        remarks = data.get('remarks') if data.get('remarks') else olditem.get('remarks')

        body = {
            "itemID": itemID,
            "itemName": itemName,
            "user": userName,
            "userID" : userID,
            "description" : description,
            "remarks" : remarks
        }

        result = db.Posts.update_one({"itemID": itemID }, {'$set': body})
        if int(result.matched_count) > 0:
            return make_response({'message': "Item updated"}, 200)
        else:
            return make_response({'err': "Item not updated"}, 204)

    elif request.method == "DELETE" :
        try:
            itemID = request.args.get('itemID')
        except:
            return {"err": "Invalid itemID", "status": "failed"}, 400

        db.Posts.delete_one({"_id": itemID})
        response = {"status": "success"}
        return make_response(response, 200)
        














# {
#     "itemID" : 1,
#     "itemName": "Vaccum",
#     "user": "Jane",
#     "userID" : 1,
#     "description" : "Vaccum Cleaner",
#     "remarks" : "Nil"
# }




        

            



