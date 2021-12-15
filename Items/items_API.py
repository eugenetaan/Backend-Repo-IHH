from db import *
from flask_cors import cross_origin
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, make_response
from flask import Blueprint
import sys

sys.path.append("../")

items_api = Blueprint("items", __name__)

# @items_api.route("/")
# def hello():
#     return "Here you can find all the items that other people are sharing!"

@items_api.route('', methods=["GET", "POST"])
@cross_origin()
def all_items():

    if request.method == "GET":

        try:
            data = list(db.items.find({},{"_id": 0}).sort("itemID", 1))
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

        itemID = int(data.get('itemID'))
        itemName = str(data.get('itemName')).capitalize()
        description = str(data.get("description"))
        remarks = str(data.get("remarks"))
        userName = str(data.get('userName'))
        userID = str(data.get("userID"))
        photo = str(data.get("photo"))
        status = data.get('status')
        tags = data.get('tags')

        body = {
            "itemID": itemID,
            "itemName": itemName,
            "userName": userName,
            "userID" : userID,
            "description" : description,
            "remarks" : remarks,
            "photo" : photo,
            "status" : status,
            "tags" : tags
        }

        #check if item_ID already exist in DB
        if list(db.items.find({"itemID": itemID})):
            return jsonify({"message": "Duplicate itemID", "status": "failure"})

        receipt = db.items.insert_one(body)
        body["_id"] = str(receipt.inserted_id)

        return make_response({"message": body, "status": "success"}, 200)



@items_api.route('/item', methods=["GET", "PUT", "DELETE"])
@cross_origin()
def item():

    if request.method == "GET":

        try:
            itemID = int(request.args.get("itemID"))
            matched_itemNames = (request.args.get("itemName")).capitalize()
        except Exception as e:
            return {"err": "Invalid item id", "status": "failed"}, 400

        try:
            if itemID:
                data = db.items.find_one({"itemID": int(itemID)}, {"_id" : 0})
                print(data)
            elif matched_itemNames:
                data = list(db.items.find({"itemName": matched_itemNames}, {"_id" : 0}))
        except Exception as e:
            return {"err": str(e), "status": "failed"}, 40

        if data == None or data == [] or data == {}:
            return {"err": "No items found", "status": "failed"}, 400

        response = {"status": "success", "data": data}
        return make_response(response)
    
    elif request.method == "PUT":
        data = request.get_json()
        itemID = int(request.args.get('itemID'))
        olditem = db.items.find_one({"itemID": itemID})
        
        userID = str(data.get('userID')) if data.get('userID') else olditem.get('userID')
        userName = str(data.get('userName')) if data.get('userName') else olditem.get('userName')
        description = str(data.get('description')) if data.get('description') else olditem.get('description')
        itemName = str(data.get('itemName')).capitalize() if data.get('itemName') else olditem.get('itemName')
        remarks = data.get('remarks') if data.get('remarks') else olditem.get('remarks')
        photo = data.get('photo') if data.get('photo') else olditem.get('photo')
        status = data.get('status') if data.get('status') else olditem.get('status')
        tags = data.get('tags') if data.get('tags') else olditem.get('tags')

        body = {
            "itemID": itemID,
            "itemName": itemName,
            "userName": userName,
            "userID" : userID,
            "description" : description,
            "remarks" : remarks,
            "photo" : photo,
            "status" : status,
            "tags" : tags
        }

        result = db.items.update_one({"itemID": itemID }, {'$set': body})
        if int(result.matched_count) > 0:
            return make_response({'message': "Item updated"}, 200)
        else:
            return make_response({'err': "Item not updated"}, 204)

    elif request.method == "DELETE" :
        try:
            itemID = request.args.get('itemID')
        except:
            return {"err": "Invalid itemID", "status": "failed"}, 400

        db.items.delete_one({"itemID": itemID})
        response = {"status": "success"}
        return make_response(response, 200)
        




@items_api.route('/item/category', methods=["GET"])
@cross_origin()
def get_category():
    try:
        tag_to_search = request.args.get("tag")
    except Exception as e:
        return {"err": "Invalid item id", "status": "failed"}, 400
    

    filter_by_tags_pipeline = [
        { "$addFields" : {"has_category" : { "$in" : [tag_to_search, "$tags"]}}},
        { "$match" : { "has_category" : True}},
        { "$project" : { "_id" : 0 , "has_category" : 0}}
    ]

    data = list(db.items.aggregate(filter_by_tags_pipeline))


    if data == [] or data == None:
        return {"err": "No items with category", "status": "success"}, 400

    response = {"status": "success", "data": data}
    return make_response(response)




# {
#     "itemID" : 2,
#     "itemName": "Mop",
#     "userName": "Jane",
#     "userID" : 1,
#     "description" : "Mop",
#     "remarks" : "Nil",
#     "photo" : "uri",
#     "status" : 0,
#     "tags" : ["appliances"]
# }


# status : 0,1,2
        

            



