from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import json
from flask_cors import CORS
 
# Author: Jon Lim
app = Flask(__name__)
CORS(app)
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
def editDest():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE destination 
                    SET cost = %s, name = %s, notes = %s 
                    WHERE id = %s''', (request.json['cost'], request.json['name'], request.json['notes'], request.json['id'],))
        mysql.connection.commit()
        cursor.close()
        return "200"
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/deleteDest', methods=['DELETE'])
def deleteDest():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM destination WHERE id = %s''', (request.json['id'],))
        mysql.connection.commit()
        cursor.close()
        return "200"
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)