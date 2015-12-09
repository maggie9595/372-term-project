# Complex Query 3:
# As a user I want to finish my ride and pay AND
# As a driver, I want to charge more for a ride if I drive a bigger or more luxurious car
# 67-372 F15 Team J9

import sys
import time
from datetime import datetime
import psycopg2

# ============== Global variables =================

PRINT_DEBUG = True

# TODO Change the rates to be realistic
RIDE_TYPE_PRICING = {
    "x": {"base_fare": 1, "per_minute": 1, "per_mile": 1},
    "xl": {"base_fare": 1, "per_minute": 1, "per_mile": 1},
    "select": {"base_fare": 1, "per_minute": 1, "per_mile": 1},
    "black": {"base_fare": 1, "per_minute": 1, "per_mile": 1}
}


# ========= Complex query functions below ============

def complete_ride(ride_id, mileage=None, duration=None):
    """
    Completes a ride by saving the ride's duration, mileage, and transaction information.

    :param ride_id: The id of the ride to complete. Should already be in the database.
    :param mileage: The length of the ride, in miles.
    :param duration: The duration of the ride, in minutes.
    """

    # Get the mileage and duration from the database if not specified.
    if mileage == None or duration == None:
        rows = _do_query("""
          SELECT mileage, duration
          FROM Rides
          WHERE id = %s;
        """, ride_id)
        mileage, duration = rows[0]

    # Get the driver's car type
    rows = _do_query("""
        SELECT manufacturer, model, ride_type
        FROM Rides
        INNER JOIN Drivers ON Rides.driver_id = Drivers.id
        INNER JOIN CarOwnerships ON CarOwnerships.driver_id = Drivers.id
        INNER JOIN Cars ON Cars.id = CarOwnerships.car_id
        WHERE Rides.id = %s;
    """, ride_id)
    manufacturer, model, ride_type = rows[0]
    ride_type = ride_type.lower().strip()

    # Calculate the price
    total_price = RIDE_TYPE_PRICING[ride_type]["base_fare"]
    total_price += RIDE_TYPE_PRICING[ride_type]["per_minute"] * duration
    total_price += RIDE_TYPE_PRICING[ride_type]["per_mile"] * mileage
    total_price = "{0:.2f}".format(total_price) # Round to 2 decimals

    # Find the payment method the customer will pay with (defaults to the first one).
    rows = _do_query("""
        SELECT UserPaymentMethods.payment_method_id
        FROM UserPaymentMethods
        INNER JOIN Users ON Users.id = UserPaymentMethods.user_id
        INNER JOIN Riders ON Riders.user_id = Users.id
        INNER JOIN Rides ON Rides.rider_id = Riders.id
        WHERE Rides.id = %s
        LIMIT 1;
    """, ride_id)
    rider_payment_method = rows[0][0]

    # Save the transaction at this time.
    end_datetime = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    _do_query_no_results("""
      UPDATE Rides
      SET mileage=%s,
          duration=%s,
          end_datetime=%s,
          payment_method_id=%s,
          price=%s,
          datetime_paid=%s
      WHERE Rides.id=%s
    """, mileage, duration, end_datetime, rider_payment_method, total_price, end_datetime, ride_id)


def run_example_queries():
    # TODO Create more example queries
    complete_ride(2, 2, 3)


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