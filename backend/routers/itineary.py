from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Replace 'user', 'password', 'host', 'database' with your MySQL connection details
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'popcorn2'
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


# Customer create a new itineary 
@app.post("/new_itineary", methods = ["POST"]) 
def create_itineary():
    try:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO itinerary (id, country_id, user_id, budget, title) VALUES (%s, %s, %s, %s, %s)",
            (data['id'], data['country_id'], data['user_id'], data['budget'], data['title'])
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Itinerary added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Customer updates the itineary
