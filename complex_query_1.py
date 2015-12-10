# Complex Query 3:
# As a rider, I want Uber to validate and verify my credit card
# So that I can use it to pay for future rides
# 67-372 F15 Team J9

import sys
import psycopg2

# ============== Global variables =================

PRINT_DEBUG = True

# ========= Complex query functions below ============

def validate_card(card_id):
    """
    Validates a credit card number entered by a rider and update the database with the result.

    :param card_id: The id of the credit card to validate. Should already be in the database.
    """

    # Get the number of the given credit card
    rows = _do_query("""
        SELECT card_number
        FROM CreditCards
        WHERE id = %s;
    """, card_id)
    card_number = rows[0][0]

    # Validate the credit card number
    # Luhn algorithm for mod-10 checksum credit card validation
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1

    print(card_number)
    for count in range(0, num_digits):
        digit = int(card_number[count])

        if not ((count & 1) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        sum = sum + digit

    is_valid = ((sum % 10) == 0)

    print(is_valid)

    # Save the validation result to the database.
    # _do_query_no_results("""
    #   UPDATE Rides
    #   SET mileage=%s,
    #       duration=%s,
    #       end_datetime=%s,
    #       payment_method_id=%s,
    #       price=%s,
    #       datetime_paid=%s
    #   WHERE Rides.id=%s
    # """, mileage, duration, end_datetime, rider_payment_method, total_price, end_datetime, ride_id)


def run_example_queries():
    validate_card(1)


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