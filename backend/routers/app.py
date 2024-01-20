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
        print(request.headers)
        token = request.headers['token'] # Token sent in the header/ could also put it in args
        print(token)
        if not token:
            return jsonify({'message': 'token is missing'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            public_id = data['id']
            print('JWT data: {}'.format(data))
            myCursor = mysql.connection.cursor()

            query = "SELECT id FROM user WHERE id = %s"
            values = (public_id)

            # Executing Query and storing return value of query into myCursor
            myCursor.execute(query, values)

            currUserID = myCursor.fetchall()
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated

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


@app.route("/dashboard", methods=['POST'])
# @token_required
def dashboard():
    try:

        user_id = request.json['user_id']
        print(user_id)
        cursor = mysql.connect.cursor()
        cursor.execute(''' SELECT * from itinerary ''')
        itineraries = cursor.fetchall()

        user_itineraries = []

        # get user's itineraries
        for row in itineraries:
            if row[2] == user_id:
                user_itineraries.append(row)

        # response = {'itinerary_title': '', 'budget':0, 'country': '', 'destinations': ''}
        response_list = []

        def get_country(country_id):
            cursor.execute("SELECT name from country WHERE id = (%s)", (str(country_id)))
            country = cursor.fetchall()

            return country[0][0]

        def get_destinations(itinerary_id):
            cursor.execute("SELECT destination_id from itinerary_destination WHERE itinerary_id = (%s)",
                           (str(itinerary_id)))
            destination_ids = cursor.fetchall()

            destinations = []

            for destination_id in destination_ids:
                cursor.execute("SELECT name from destination WHERE id = (%s)", (str(destination_id[0])))
                name = cursor.fetchall()
                destinations.append(name[0][0])

            destinations = ', '.join(destinations)

            return destinations

        # create responses
        for itinerary in user_itineraries:
            response = {}
            response['itinerary_id'] = itinerary[0]
            response['itinerary_title'] = itinerary[4]
            response['budget'] = itinerary[3]
            response['country'] = get_country(itinerary[1])
            response['destinations'] = get_destinations(itinerary[0])
            response_list.append(response)

        return jsonify(response_list)

    except Exception as e:
        return jsonify({'error': str(e)})

# Customer displays all itineraries

@app.route('/get_itinerary', methods=['POST'])
# @token_required
def index():
    try:
        print(request)
        data = request.get_json()
        print(data)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM itinerary WHERE user_id = %s", data['id'])
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})


# Customer create a new itinerary
@app.route("/new_itinerary", methods=["POST"])
# @cross_origin()
# @token_required
def create_itinerary():
    try:
        data = request.get_json()
        # using datetime to generate unique id
        unique_id = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]

        cursor = mysql.connection.cursor()

        # Statement to update itinerary table
        cursor.execute(
            "INSERT INTO itinerary (id, country_id, user_id, budget, title) VALUES (%s, %s, %s, %s, %s)",
            (unique_id, data['country_id'], data['user_id'], data['budget'], data['title'])
        )

        # Statement to update itinerary-destination table
        if len(data['destinations']) == 0:
            pass
        else:
            for i in len(data['destinations']):
                cursor.execute(
                    "INSERT INTO itinerary_destination(id, destination_id, itinearary_id VALUES (%s, %s , %s)",
                    (f"{unique_id}_{i}", data['destinations'][i - 1], data['itinerary_id'])

                )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Itinerary added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


# Customer updates the itinerary

@app.route('/edit_itinerary', methods=['POST'])
# @token_required
def edit_itinerary():
    try:
        # Update itinerary data
        data = request.get_json()
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE itinerary
            SET country_id = %s, budget = %s, title = %s
            WHERE id = %s AND user_id = %s
        """, (data['country_id'], data['budget'], data['title'], data["id"], data['user_id']))

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Itinerary updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})


# Customer edits destination which requires updates to both the itinerary and itinerary_destination tables.
@app.route('/edit_itinerary_destination', methods=['POST'])
# @token_required
def edit_itinerary_destination():
    try:

        data = request.get_json()
        cursor = mysql.connection.cursor()
        unique_id = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]

        # delete all records wrt to the itinerary
        cursor.execute("""
                DELETE FROM itinerary_destination WHERE itinearary_id = %s
                        """, (data['itinerary_id']))

        # update record in itinerary
        cursor.execute("""
            UPDATE itinerary
            SET country_id = %s, budget = %s, title = %s
            WHERE id = %s AND user_id = %s
        """, (data['country_id'], data['budget'], data['title'], data["id"], data['user_id']))

        # re-insert record into itinerary_destination
        for i in len(data['destinations']):
            cursor.execute(
                "INSERT INTO itinerary_destination(id, destination_id, itinearary_id VALUES (%s, %s , %s)",
                (f"{unique_id}_{i}", data['destinations'][i], data['itinerary_id'])
            )

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Itinerary updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})


# To delete itinerary
@app.route('/delete_itinerary', methods=['POST'])
# @token_required
def delete_itinerary_destination():
    try:
        # update itinerary_destination
        data = request.get_json()
        cursor = mysql.connection.cursor()

        # delete all records wrt to the itinerary table
        cursor.execute("""
                DELETE FROM itinerary WHERE id = %s
                        """, (data['itinerary_id']))
        # delete all record wrt to the itinerary_destination table
        cursor.execute("""
                DELETE FROM itinerary_destination WHERE itinearary_id = %s
                        """, (data['itinerary_id']))

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Itinerary deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/', methods=['GET'])
@token_required
def base():
    return "Hello World"

@app.route('/getDestNames', methods=['GET'])
# @token_required
def getDestNames():
    try:
        itinerary_id = request.args['id']
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT destination.name 
                    FROM destination
                    RIGHT JOIN itinerary_destination 
                    ON itinerary_destination.destination_id = destination.id 
                    WHERE itinerary_destination.itinerary_id = %s''', itinerary_id)
        data = cursor.fetchall()
        cursor.close()

        print("data: ", data)

        json_data = []
        for result in data:
            json_data.append(result)
        json_result = json.dumps(json_data)
        return json_result
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/getDest', methods=['GET'])
# @token_required
def getDest():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
                    SELECT country.name, destination.cost, destination.name, destination.notes, destination.id 
                    FROM destination
                    LEFT JOIN country ON destination.country_id = country.id
                    ORDER BY country.id ''')
        data = cursor.fetchall()
        cursor.close()
        country_dest = {}
        for country_data in data:
            if country_data[0] not in country_dest.keys():
                country_dest[country_data[0]] = []
            dest_details = {"cost": country_data[1], "name": country_data[2], "notes": country_data[3], "id": country_data[4]}
            country_dest[country_data[0]].append(dest_details)
        return country_dest
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/postDest', methods=['POST'])
# @token_required
def postDest():
    try:
        cursor = mysql.connection.cursor()

        #calculate new id for destination
        cursor.execute('''SELECT MAX(id) FROM destination ''')
        prev_id = cursor.fetchall()
        new_id = prev_id[0][0] + 1

        #check if country exists
        cursor.execute('''SELECT COUNT(id) FROM country WHERE name = %s''',(request.json['country'],))
        num_countries = cursor.fetchall()[0][0]

        print(num_countries)
        if num_countries == 0:
            #create new country if if not exist
            cursor.execute('''SELECT MAX(id) FROM country''')
            new_country_id = cursor.fetchall()[0][0] + 1
            print(new_country_id)
            cursor.execute('''INSERT INTO country (id, name) VALUES (%s, %s)''', (new_country_id, request.json['country']))
            cursor.execute('''INSERT INTO destination (id, country_id, cost, name, notes) 
                    VALUES (%s, %s, %s, %s, %s)''', (new_id, new_country_id, request.json['cost'], request.json['location'], request.json['notes']))
        else:
            cursor.execute('''SELECT id FROM country WHERE name = %s''',(request.json['country'],))
            country_id = cursor.fetchall()[0][0]
            cursor.execute('''INSERT INTO destination (id, country_id, cost, name, notes) 
                    VALUES (%s, %s, %s, %s, %s)''', (new_id, country_id, request.json['cost'], request.json['location'], request.json['notes']))
        mysql.connection.commit()
        cursor.close()
        return "200"
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/editDest', methods=['POST'])
# @token_required
def editDest():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE destination 
                    SET cost = %s, name = %s, notes = %s 
                    WHERE id = %s''', (request.json['cost'], request.json['location'], request.json['notes'], request.json['id'],))
        mysql.connection.commit()
        cursor.close()
        return "200"
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/deleteDest', methods=['DELETE'])
# @token_required
def deleteDest():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM destination WHERE id = %s''', (request.json['id'],))
        mysql.connection.commit()
        cursor.close()
        return "200"

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
