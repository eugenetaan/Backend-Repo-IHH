from flask import Flask
from flask_cors import CORS
from db import *
from secret_keys import *
import jwt
from Authentication.Authentication_API import auth_api
from Users.Users_API import users_api
from Items.items_API import items_api
from Profiles.Profiles_APi import profiles_api

app = Flask(__name__)
app.config['SECRET_KEY'] = auth_secret_key
app.register_blueprint(profiles_api, url_prefix="/profiles")
app.register_blueprint(auth_api, url_prefix="/auth")
app.register_blueprint(items_api, url_prefix="/items")
app.register_blueprint(users_api, url_prefix="/users")


# Endpoints
@app.route("/", methods=["GET"])
def hello():
	return "Welcome!"

# Start the server (development)
if __name__ == "__main__":
    app.run("localhost", port=8080, debug= True)
	 #Testing on own computer
	#app.run("0.0.0.0", port=8080) #Deploying