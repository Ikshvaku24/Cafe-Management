from flask import *
import uuid
from db.item import ItemDatbase
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schemas import ItemGetSchema, ItemOptionalQuerySchema, ItemQuerySchema, ItemSchema, SuccessMessageSchema
from flask_jwt_extended import jwt_required

blp = Blueprint("items", __name__, description="Operation on Items")


@blp.route("/item")
class Item(MethodView):
    def __init__(self) :
        self.db = ItemDatbase()
    
    @jwt_required()
    @blp.response(200, ItemGetSchema(many=True))
    @blp.arguments(ItemOptionalQuerySchema, location="query")
    def get(self,args):
        print(args)
        id = args.get("id")
        if id is None:
            return self.db.get_Items()  # get-items
        else: 
            result = self.db.get_Item(id)
            if result is None:
                abort(404, message="record doesn't exist")
            return result
    
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, SuccessMessageSchema)
    def post(self,request_data):
        id = uuid.uuid4().hex
        body = request_data
        self.db.add_Item(id,body)
        return {"message": "Item added succefully"}, 201

    @jwt_required()
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def put(self,request_data,args):
        id = args.get("id")
        if self.db.put_Item(id,request_data):
            return {"message": "Item updated successfully"}, 200  # returns http 200 code which is default
        abort(404, message="Item not found")

    @jwt_required()
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def delete(self,args):
        id = args.get("id")
        if self.db.delete_Item(id):
            return {"message":"Item deleted successfully"}
        abort(404, message="Item not found")
