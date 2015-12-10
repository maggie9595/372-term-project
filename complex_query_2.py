# Complex Query 2:
# As a user I want to request the driver that is nearest to my location
# And I would like this ride history to be stored for future reference
# 67-372 F15 Team J9

import sys
import time
from datetime import datetime
import psycopg2
import math

# ============== Global variables =================

PRINT_DEBUG = True

# ========= Complex query functions below ============

def calculateDistance(rider_lat, rider_long, driver_lat, driver_long):
    distance = math.sqrt( ((driver_lat - rider_lat)**2) + ((driver_long - rider_long)**2))
    return distance


def request_ride(rider_id, start_datetime):
    """
    Rider requests a ride, system matches them with closest driver, stores ride information in the Rides table

    :param ride_id: The id of the rider that has requested a ride. Should already be in the database.
    """

    # Get the rider's current latitude and longitude
    riderQuery = """
        SELECT current_longitude, current_latitude
        FROM Riders
        WHERE id = %s
    """
    rows = _do_query(riderQuery, rider_id)
    rider_longitude, rider_latitude = rows[0]

    # Find the closest driver
    closestDriver = 1
    closestDistance = 0.0;
    driversQuery = """
        SELECT id, is_available, current_longitude, current_latitude
        FROM Drivers
        WHERE is_available = true
    """
    rows = _do_query(driversQuery)
    for row in rows:
        driverid, is_available, driver_longitude, driver_latitude = row
        if driverid == 1:
            closestDistance = calculateDistance(rider_latitude, rider_longitude, driver_latitude, driver_longitude)
        distance = calculateDistance(rider_latitude, rider_longitude, driver_latitude, driver_longitude)
        if (distance < closestDistance):
            closestDistance = distance
            closestDriver = driverid

    print("The closest driver to the rider is", closestDriver)
    # Insert into rides: rider_id, driver_id, start_longitude, start_latitude, start_datetime
    insertQuery = """
        INSERT INTO Rides (rider_id, driver_id, start_longitude, start_latitude, start_datetime)
        VALUES(%s, %s, %s, %s, %s)
    """

    _do_query_no_results(insertQuery, rider_id, closestDriver, rider_longitude, rider_latitude, start_datetime) 


def run_example_queries():
    # TODO Create more example queries
    request_ride(2, datetime.today())


# ============== Helper functions ================

def _do_query(tmpl, *params):
    """
    Helper method to perform a query.

    :param tmpl: The SQL template.
    :param params: The parameters to fill the template with.
    :return: The rows returned by the query.
    """
    cmd = cur.mogrify(tmpl, params)
    if(PRINT_DEBUG):
        print(cmd.decode('utf-8'))
    cur.execute(cmd)
    return cur.fetchall()

def _do_query_no_results(tmpl, *params):
    """
    Like _do_query except it doesn't return rows. Useful for updates or inserts.
    """
    cmd = cur.mogrify(tmpl, params)
    if(PRINT_DEBUG):
        print(cmd.decode('utf-8'))
    cur.execute(cmd)


# ========= Main method that runs the program ===========

if __name__ == '__main__':
    try:
        # Default database and user
        db, user = 'j9_uber', 'postgres'

        # Expected Usage: python create_query_3.py postgres
        if len(sys.argv) >= 2:
            user = sys.argv[1] # Get the specified user if it exists
        else:
            print("Using default user 'postgres' since it was not specified.")

        # Connect to the db with an optional password
        if len(sys.argv) >= 3:
            password = sys.argv[2]
            conn = psycopg2.connect(database=db, user=user, password=password, host="127.0.0.1", port="5432")
        else:
            conn = psycopg2.connect(database=db, user=user, host="127.0.0.1", port="5432")

        conn.autocommit = True
        cur = conn.cursor() # Global cursor variable available everywhere.
        run_example_queries()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e))



    