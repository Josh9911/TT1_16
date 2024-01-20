from flask import Flask, request, redirect, jsonify, session
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL, MySQLdb
from flask_jwt_extended import jwt_required

import json

# Initializing flask app
app = Flask(__name__)

CORS(app)

# Connect to Database TODO: Place config in config.py file or .env file so it is private
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "1998durby"
app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_DB'] = "techtrek24"

mysql = MySQL(app)


# TODO: Implement JWT Authentication function

@app.route('/')
def testing_connection():
    try:
        # Initialise Cursor for MySQL Database
        myCursor = mysql.connection.cursor()
        query = "SELECT * FROM user"

        # Executing Query for connection testing\
        myCursor.execute(query)

        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/login', methods=['POST'])
def login_user():
    login_data = request.json
    try:
        loginUsername = login_data['Username']
        loginPassword = login_data['Password']

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

        # json.dumps converts a subset of Python objects into a json string
        loginJsonResult = json.dumps(userID)

        print("Login JSON string: ", loginJsonResult, "Login JSON type: ", type(loginJsonResult))

        # .close() close the query connection to mySQL database
        myCursor.close()

        if not userID:
            print("no user found")
            return "No User Found", 401
        else:
            return "Successfully Logged in", 200

    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(debug=True)
