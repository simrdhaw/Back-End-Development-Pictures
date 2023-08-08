from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data),200
    
    return {"message": "Internal server error"},500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    try:
        return jsonify(data[id-1]),200
    except:
        return {"message": "Internal Client Error"},404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
   # print(new_picture["id"])
    if not new_picture:
        return {"Message": "Invalid data by client"},404
    for idx in data:
        # print(idx)
        if idx["id"] is new_picture["id"]:
            return {"Message": f"picture with id {new_picture['id']} already present"},302;
    
    try:
        data.append(new_picture)   
        return jsonify(new_picture),201
    except NameError:
        return {"message": "data not defined"}, 500
         

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.json
    print(new_picture['id'])
    if new_picture['id'] == 'id':
        for idx in range(len(data)):
            if(data['idx'].id == 'id'):
                data['idx'] = new_picture
        
                return jsonify(data["id"]),200
        
    return {"message": "picture not found"},404
        

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):

    for idx in range(len(data)):
        print(data[idx]['id'])
        # print('id')
        if(data[idx]['id'] == id):
            # print(data[idx])
            data.remove(data[idx])
            return {"Message": "HTTP_204_NO_CONTENT"},204
    return {"message": "picture not found"},404
