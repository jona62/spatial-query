import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from mysql.connector import errorcode
import os

db = None  # Initialize as global variable
app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
  return "Hello, world!"

@app.route('/mickeyd', methods=['POST'])
def get_mcdonalds_within_range():
    try:
        data = request.get_json()
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        range_km = int(data['range'])

        locations = db.get_mcdonalds_within_range(latitude=latitude, longitude=longitude, range_km=range_km)
        json_results = [
            {
                "name": loc[0],
                "latitude": loc[1],
                "longitude": loc[2],
                "addressLine1": loc[3],
                "addressLine2": loc[4],
                "addressLine3": loc[5],
                "postcode": loc[6],
                "telephone": loc[7],
                "restaurantUrl": loc[8],
                "openstatus": loc[9],
                "hoursMonday": loc[10],
                "hoursTuesday": loc[11],
                "hoursWednesday": loc[12],
                "hoursThursday": loc[13],
                "hoursFriday": loc[14],
                "hoursSaturday": loc[15],
                "hoursSunday": loc[16]
            } for loc in locations
        ]
        return jsonify(json_results)
    except (KeyError, ValueError) as e:
        return jsonify({"error": "Invalid input data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    return response

class RestaurantDatabase:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self, table_name, table_description):
        self.ensure_connection()
        cursor = self.connection.cursor()
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        cursor.close()


    def ensure_connection(self):
        if not self.connection.is_connected():
            self.connection.reconnect()

    def get_mcdonalds_within_range(self, latitude: float, longitude: float, range_km: int) -> list:
        print("Getting mcdonalds within range {} at coordinates [{}, {}]".format(range_km, latitude, longitude))
        self.ensure_connection()
        cursor = self.connection.cursor()
        query = """
        SELECT DISTINCT name, latitude, longitude, addressLine1, addressLine2, addressLine3, postcode, telephone, restaurantUrl, openstatus,
        hoursMonday, hoursTuesday, hoursWednesday, hoursThursday, hoursFriday, hoursSaturday, hoursSunday
        FROM locations 
        WHERE ST_Distance_Sphere(geom, ST_GeomFromText(%s, 4326)) <= %s
        """
        point = f'POINT({longitude} {latitude})'
        cursor.execute(query, (point, range_km * 1000))  # range_km to meters
        results = cursor.fetchall()
        cursor.close()
        return results

if __name__ == "__main__":
    connection = mysql.connector.connect(
        host="localhost",
        user="Admin",
        password="Admin",
        database="mcdonalds_locations"
    )
    db = RestaurantDatabase(connection)

    port = int(os.environ.get("PORT", 5001))  # Default to 5001 if PORT is not set
    app.run(port=port, debug=True)

    connection.close()
