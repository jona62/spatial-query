import mysql.connector
from mysql.connector import errorcode
import json

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

    def insert_location(self, data_location):
        self.ensure_connection()
        cursor = self.connection.cursor()
        add_location = ("INSERT INTO locations "
            "(name, latitude, longitude, geom, addressLine1, addressLine2, addressLine3, postcode, telephone, restaurantUrl, openstatus, hoursMonday, hoursTuesday, hoursWednesday, hoursThursday, hoursFriday, hoursSaturday, hoursSunday)"
            "VALUES (%(name)s, %(latitude)s, %(longitude)s, ST_GeomFromText(%(geom)s, 4326), "
            "%(addressLine1)s, %(addressLine2)s, %(addressLine3)s, %(postcode)s, %(telephone)s, %(restaurantUrl)s, %(openstatus)s, %(hoursMonday)s, %(hoursTuesday)s, %(hoursWednesday)s, %(hoursThursday)s, %(hoursFriday)s, %(hoursSaturday)s, %(hoursSunday)s)"
        )

        cursor.execute(add_location, data_location)
        self.connection.commit()
        cursor.close()

    def ensure_connection(self):
        if not self.connection.is_connected():
            self.connection.reconnect()

if __name__ == "__main__":
    conn = mysql.connector.connect(
        host="localhost",
        user="Admin",
        password="Admin",
        database="mcdonalds_locations"
    )
    db = RestaurantDatabase(conn)
    db.create_table(
        table_name="locations",
        table_description="""
        CREATE TABLE IF NOT EXISTS locations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            latitude DOUBLE,
            longitude DOUBLE,
            geom POINT NOT NULL SRID 4326,
            addressLine1 VARCHAR(255),
            addressLine2 VARCHAR(255),
            addressLine3 VARCHAR(255),
            postcode VARCHAR(255),
            telephone VARCHAR(255),
            restaurantUrl VARCHAR(255),
            openstatus VARCHAR(255),
            hoursMonday VARCHAR(255),
            hoursTuesday VARCHAR(255),
            hoursWednesday VARCHAR(255),
            hoursThursday VARCHAR(255),
            hoursFriday VARCHAR(255),
            hoursSaturday VARCHAR(255),
            hoursSunday VARCHAR(255)
        )
        """
    )

    with open('McDonalds.json') as json_file:
        list_of_mcdonalds = json.load(json_file)

    # Insert locations into the database
    print("Inserting locations into the database...")
    for mcdonalds in list_of_mcdonalds:
        geometry = mcdonalds["geometry.coordinates"]
        name = mcdonalds["properties.identifierValue"]
        latitude = geometry[1]
        longitude = geometry[0]
        addressLine1 = mcdonalds["properties.addressLine1"]
        addressLine2 = mcdonalds["properties.addressLine2"]
        addressLine3 = mcdonalds["properties.addressLine3"]
        postcode = mcdonalds["properties.postcode"]
        telephone = mcdonalds["properties.telephone"]
        restaurantUrl = mcdonalds["properties.restaurantUrl"]
        openstatus = mcdonalds["properties.openstatus"]
        hoursMonday = mcdonalds["properties.restauranthours.hoursMonday"]
        hoursTuesday = mcdonalds["properties.restauranthours.hoursTuesday"]
        hoursWednesday = mcdonalds["properties.restauranthours.hoursWednesday"]
        hoursThursday = mcdonalds["properties.restauranthours.hoursThursday"]
        hoursFriday = mcdonalds["properties.restauranthours.hoursFriday"]
        hoursSaturday = mcdonalds["properties.restauranthours.hoursSaturday"]
        hoursSunday = mcdonalds["properties.restauranthours.hoursSunday"]
        
        data_location = {
            'name': name,
            'latitude': latitude,
            'longitude': longitude,
            'geom': f'POINT({latitude} {longitude})',
            'addressLine1': addressLine1,
            'addressLine2': addressLine2,
            'addressLine3': addressLine3,
            'postcode': postcode,
            'telephone': telephone,
            'restaurantUrl': restaurantUrl,
            'openstatus': openstatus,
            'hoursMonday': hoursMonday,
            'hoursTuesday': hoursTuesday,
            'hoursWednesday': hoursWednesday,
            'hoursThursday': hoursThursday,
            'hoursFriday': hoursFriday,
            'hoursSaturday': hoursSaturday,
            'hoursSunday': hoursSunday
        }
        db.insert_location(data_location)
    
    print("Inserted {} locations".format(len(list_of_mcdonalds)))
    conn.close()
