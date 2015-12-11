# Complex Query 3:
# As a driver I want to complete a ride and charge the right price for it
# 67-372 F15 Team J9

import sys
import time
from datetime import datetime
import psycopg2

# ============== Global variables =================

PRINT_DEBUG = True

RIDE_TYPE_PRICING = {
    "x": {"base_fare": 3, "per_minute": 0.4, "per_mile": 2.15},
    "xl": {"base_fare": 4.5, "per_minute": 0.6, "per_mile": 3.25},
    "select": {"base_fare": 5, "per_minute": 0.5, "per_mile": 3},
    "black": {"base_fare": 7, "per_minute": 0.65, "per_mile": 3.75}
}


# ========= Complex query functions below ============

def complete_ride(ride_id, mileage, end_latitude, end_longitude):
    """
    Completes a ride by saving the ride's mileage and transaction information.

    :param ride_id: The id of the ride to complete. Should already be in the database.
    :param mileage: The length of the ride, in miles (optional if already in the database).
    """

    # Get the start and end date times
    rows = _do_query("""
        SELECT start_datetime, end_datetime
        FROM Rides
        WHERE id=%s
    """, ride_id)
    start_datetime, end_datetime = rows[0]

    # Use current time if end_time doesn't exist
    if(end_datetime == None):
        end_datetime = datetime.fromtimestamp(time.time())

    # Calculate the duration of the ride
    sdt_seconds = time.mktime(start_datetime.timetuple())
    edt_seconds = time.mktime(end_datetime.timetuple())
    duration = (edt_seconds - sdt_seconds) / 60 # In minutes

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
    _do_query_no_results("""
      UPDATE Rides
      SET end_latitude=%s,
          end_longitude=%s,
          mileage=%s,
          end_datetime=%s,
          payment_method_id=%s,
          price=%s,
          datetime_paid=%s
      WHERE Rides.id=%s
    """, end_latitude, end_longitude, mileage, end_datetime,
         rider_payment_method, total_price, end_datetime, ride_id)

    print("Ride #%s has been completed and paid for, the price is: $%s." % (ride_id, total_price))


def run_example_queries():
    complete_ride(3, 8, 40.438959,-79.930746)
    complete_ride(4, 4, 40.443241,-79.923416)
    complete_ride(5, 3, 40.453195,-79.931458)


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