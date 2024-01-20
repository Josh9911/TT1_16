from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# Replace 'user', 'password', 'host', 'database' with your MySQL connection details
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'techtrek24'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Customer displays all itineraries

@app.route('/get_itinerary', methods = ['POST'])
def index():
    try:   
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM itinerary WHERE user_id = %s", data['id'])
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})


# Customer create a new itinerary 
@app.route("/new_itinerary", methods = ["POST"]) 
def create_itinerary():
    try:
        data = request.get_json()
        #using datetime to generate unique id
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
                cursor.execute (
                    "INSERT INTO itinerary_destination(id, destination_id, itinearary_id VALUES (%s, %s , %s)",
                    (f"{unique_id}_{i}", data['destinations'][i-1], data['itinerary_id'])
                
            )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Itinerary added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Customer updates the itinerary

@app.route('/edit_itinerary', methods=['POST'])
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
@app.route('/edit_itinerary_destination', methods = ['POST'])
def edit_itinerary_destination():
    try:
        
        data =  request.get_json()
        cursor = mysql.connection.cursor()
        unique_id = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]

        #delete all records wrt to the itinerary
        cursor.execute ("""
                DELETE FROM itinerary_destination WHERE itinearary_id = %s
                        """, (data['itinerary_id']))
        
        #update record in itinerary
        cursor.execute("""
            UPDATE itinerary
            SET country_id = %s, budget = %s, title = %s
            WHERE id = %s AND user_id = %s
        """, (data['country_id'], data['budget'], data['title'], data["id"], data['user_id']))
        
        #re-insert record into itinerary_destination
        for i in len(data['destinations']):
            cursor.execute (
                "INSERT INTO itinerary_destination(id, destination_id, itinearary_id VALUES (%s, %s , %s)",
                (f"{unique_id}_{i}", data['destinations'][i], data['itinerary_id'])
            )
        
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Itinerary updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})


# To delete itinerary
@app.route('/delete_itinerary', methods = ['POST'])
def delete_itinerary_destination():
    try:
        #update itinerary_destination
        data =  request.get_json()
        cursor = mysql.connection.cursor()


        #delete all records wrt to the itinerary table
        cursor.execute ("""
                DELETE FROM itinerary WHERE id = %s
                        """, (data['itinerary_id']))
        #delete all record wrt to the itinerary_destination table 
        cursor.execute ("""
                DELETE FROM itinerary_destination WHERE itinearary_id = %s
                        """, (data['itinerary_id']))
        
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Itinerary deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)