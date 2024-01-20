from flask import Flask, request
from flask_mysqldb import MySQL
import json
 
# Author: Jon Lim
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'techtrek24'
 
mysql = MySQL(app)

@app.route('/', methods=['GET'])
def base():
    return "Hello World"

@app.route('/getDestNames', methods=['GET'])
def getDestNames():
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

@app.route('/getDest', methods=['GET'])
def getDest():
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

if __name__ == '__main__':
    app.run(debug=True)