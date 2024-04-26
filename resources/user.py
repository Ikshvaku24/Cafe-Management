from flask import *
from db.user import UserDatabase
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schemas import SuccessMessageSchema, UserSchema,UserQuerySchema
import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blocklist import BLOCKLIST
blp = Blueprint("Users", __name__, description="Operation on Users")

@blp.route("/login")
class UserLogin(MethodView):
    def __init__(self) :
        self.db = UserDatabase()
       
    @blp.arguments(UserSchema)
    def post(self,request_data):
        username = request_data["username"]
        password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()
        #check if user exist in database
        user_id = self.db.verify_user(username, password)
        if user_id:
            return {"access_token": create_access_token(identity=user_id)}
        abort(400,message = "Username  or password incorrect")
       
@blp.route("/logout")
class UserLogout(MethodView):
    
    @jwt_required()   
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}
             
        

@blp.route("/user")
class User(MethodView):
    def __init__(self) :
        self.db = UserDatabase()
    
    @blp.response(200, UserSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def get(self,args):
        id = args.get("id")
        result = self.db.get_user(id)
        if result is None:
            abort(404, message="User doesn't exist")
        return result
    
    @blp.arguments(UserSchema)
    @blp.response(200, SuccessMessageSchema)
    def post(self,request_data):
        username = request_data["username"]
        password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()
        if self.db.add_user(username, password):
            return {"message": "User added succefully"}, 201
        return abort(403, message="User already exist")

    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def delete(self,args):
        id = args.get("id")
        if self.db.delete_user(id):
            return {"message":"User deleted successfully"}
        abort(404, message="User ID not found")
