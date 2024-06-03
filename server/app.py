import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

connection = None  # Initialize as global variable
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

        locations = get_mcdonalds_within_range(connection=connection, latitude=latitude, longitude=longitude, range_km=range_km)
        json_results = [
            {
                "name": name,
                "latitude": latitude,
                "longitude": longitude,
                "addressLine1": addressLine1,
                "addressLine2": addressLine2,
                "addressLine3": addressLine3,
                "postcode": postcode,
                "telephone": telephone,
                "restaurantUrl": restaurantUrl,
                "openstatus": openstatus,
                "hoursMonday": hoursMonday,
                "hoursTuesday": hoursTuesday,
                "hoursWednesday": hoursWednesday,
                "hoursThursday": hoursThursday,
                "hoursFriday": hoursFriday,
                "hoursSaturday": hoursSaturday,
                "hoursSunday": hoursSunday
            } for name, latitude, longitude, addressLine1, addressLine2, addressLine3, postcode, telephone, restaurantUrl, openstatus, hoursMonday, hoursTuesday, hoursWednesday, hoursThursday, hoursFriday, hoursSaturday, hoursSunday in locations
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

def ensure_connection(connection):
    if not connection.is_connected():
        connection.reconnect()

def get_mcdonalds_within_range(connection: mysql.connector, latitude: float, longitude: float, range_km: int) -> list:
    print("Getting mcdonalds within range {} at coordinates [{}, {}]".format(range_km, latitude, longitude))
    ensure_connection(connection)
    cursor = connection.cursor()
    query = """
        SELECT DISTINCT name, latitude, longitude, addressLine1, addressLine2, addressLine3, postcode, telephone, restaurantUrl, openstatus,
        hoursMonday, hoursTuesday, hoursWednesday, hoursThursday, hoursFriday, hoursSaturday, hoursSunday
        FROM locations 
        WHERE ST_Distance_Sphere(geom, ST_GeomFromText(%s, 4326)) <= %s
    """
    point = f'POINT({latitude} {longitude})'
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

    port = int(os.environ.get("PORT", 5001))  # Default to 5001 if PORT is not set
    app.run(port=port, debug=True)

    connection.close()
