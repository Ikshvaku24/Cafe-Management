"""
Cafe Management

get-items - get all the items in the Cafe Menu
get-item - get given item from menu
add-items - add item in the Menu
update-item - update the item in the menu
delete-item - delete the given item
"""
from flask import *
import json
from resources.item import blp as ItemBluePrint
from resources.user import blp as UserBluePrint
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

app = Flask(__name__) # app should same as filename for flask run

app.config["PROPAGATE EXCEPTIONS"] = True
app.config["API_TITLE"] = "Items REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config["JWT_SECRET_KEY"] = "47012555650598238363665201410193855259"

api= Api(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST
    
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return(
        {
            "Description": "User has been logged out",
            "error": "token_revoked"
        },
        401
    )

api.register_blueprint(ItemBluePrint)
api.register_blueprint(UserBluePrint)
