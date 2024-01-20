from datetime import datetime
from functools import wraps

import jwt
from flask import Flask, request, redirect, jsonify, session
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL, MySQLdb
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from datetime import datetime, timedelta

from login_settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, JWT_SECRETKEY

import json

# ================================ CONNECTION SPECIFICATION ================================== #
############ Call Flask, Connect Flask to Database ############
# Initializing flask app
app = Flask(__name__)

CORS(app)

# TODO: Place config in config.py file or .env file so it is private
# Connect to Database (App Config)
app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_HOST"] = MYSQL_HOST
app.config["MYSQL_DB"] = MYSQL_DB
app.config["SECRET_KEY"] = JWT_SECRETKEY

mysql = MySQL(app)


########### JWT Authentication ############
# TODO: Implement JWT Authentication function

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(request.args)
        token = request.headers['token'] # Token sent in the header/ could also put it in args
        print(token)
        if not token:
            return jsonify({'message': 'token is missing'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            public_id = data['id']
            print('data: {}'.format(data))
            myCursor = mysql.connection.cursor()

            query = "SELECT id FROM user WHERE id = %s"
            values = (public_id)

            # Executing Query and storing return value of query into myCursor
            myCursor.execute(query, values)

            currUserID = myCursor.fetchall()
        except:
            return jsonify({'message': 'Token is invalid'}), 4  01

        return f(*args, **kwargs)

    return decorated

# def generate_jwt_token(content):
#     expiration_time = datetime.now() + timedelta(hours=36)
#
#     content.update({"exp": expiration_time})
#
#     encoded_content = jwt.encode(content, JWT_SECRETKEY, algorithm="HS256")
#
#     return encoded_content


@app.route('/login', methods=['POST'])
def login_user():
    login_data = request.json
    try:
        loginUsername = login_data['username']
        loginPassword = login_data['password']

        # Initialise Cursor for MySQL Database, allows us to execute mySQL commands in a database session
        myCursor = mysql.connection.cursor()
        print("Cursor connected!")

        query = "SELECT id FROM user WHERE username = %s AND password = %s"
        values = (loginUsername, loginPassword)

        # Executing Query and storing return value of query into myCursor
        myCursor.execute(query, values)

        # Storing all values returned from execute into variable userID
        userID = myCursor.fetchall()
        print("UserID fetched: ", userID, "UserID type: ", type(userID))  # Testing

        # json.dumps converts tuple into a json string
        loginJsonResult = json.dumps(userID[0][0])

        print("Login JSON string: ", loginJsonResult, "Login JSON type: ", type(loginJsonResult))

        # .close() close the query connection to mySQL database
        myCursor.close()

        loginContent = {"id": loginJsonResult}
        print("login function done:", loginContent)

        if not userID:
            print("No User found")
            return "No User Found", 401
        else:
            expiration_time = datetime.now() + timedelta(hours=36)
            loginContent.update({"exp": expiration_time})
            print("login function update:", loginContent)

            token = jwt.encode(loginContent, app.config["SECRET_KEY"], algorithm="HS256")
            print("token:", token)
            print(jsonify({"id": loginJsonResult, 'token': token}))
            return jsonify({"id": loginJsonResult, 'token': token}), 200

        # Frontend side could be response.accessToken.token instead to get token

    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(debug=True)
