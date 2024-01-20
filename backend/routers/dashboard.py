from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'oReo*rUffles+100599'
app.config['MYSQL_DB'] = 'techtrek24'

mysql = MySQL(app)

# @app.route("/dashboard")
@app.route("/dashboard", methods = ['POST'])
def dashboard():
    user_id = request.get_data('user_id')
    cursor = mysql.connect.cursor()
    cursor.execute( "SELECT * from itinerary" )
    itineraries = cursor.fetchall()

    user_itineraries = []

    # get user's itineraries
    for row in itineraries:
        if row[2] == user_id:
            user_itineraries.append(row)
    if not user_itineraries:
        return {"Error": "No itineraries under user id"}

    # define functions to get country and destination names from database
    def get_country(country_id):
        cursor.execute("SELECT name from country WHERE id = (%s)", (str(country_id)))
        country = cursor.fetchall()

        return country[0][0]
    
    def get_destinations(itinerary_id):
        cursor.execute("SELECT destination_id from itinerary_destination WHERE itinerary_id = (%s)", (str(itinerary_id)))
        destination_ids = cursor.fetchall()

        destinations = []

        for destination_id in destination_ids:
            cursor.execute("SELECT name from destination WHERE id = (%s)", (str(destination_id[0])))
            name = cursor.fetchall()
            destinations.append(name[0][0])
        
        destinations = ', '.join(destinations)

        return destinations

    # create responses
    # response = {'itinerary_id': 0, 'itinerary_title': '', 'budget':0, 'country': '', 'destinations': ''}
    response_list = []
    
    for itinerary in user_itineraries:
        response = {}
        response['itinerary_id'] = itinerary[0]
        response['itinerary_title'] = itinerary[4]
        response['budget'] = itinerary[3]
        response['country'] = get_country(itinerary[1])
        response['destinations'] = get_destinations(itinerary[0])
        response_list.append(response)

    return jsonify(response_list)

if __name__ == '__main__':
    app.run(debug=True)