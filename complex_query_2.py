# 9. As a rider, I want to get the driver that is nearest to my location

#-----------------------------------------------------------------
# Working with psycopg2
#-----------------------------------------------------------------

import psycopg2
import sys

SHOW_CMD = True
def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

def print_rows(rows):
    for row in rows:
        print(row)

def get_nearest_driver():
    targetRider = "2"
    # get the targetRider's current latitude and longitude and store them in variables
    # Need to set these after getting the data
    riderLatitude = 0
    riderLongitude = 0
	riderQuery = '''
        SELECT id, current_latitude, current_longitude
        FROM Riders
        WHERE id = %s
	'''
	cmd = cur.mogrify(riderQuery, (targetRider,))
    print("RiderQuery SQL Statement: ")
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print("Results: \n")
    print_rows(rows)
    for row in rows:
        id, current_latitude


    # get array of drivers
    closestDriver = "6"
    closestDistance = 0
    driverQuery = '''
        SELECT *
        FROM Drivers
        WHERE is_availabe = True
    '''
    print()


    print("SQL Statement: ")
    print(tmpl)
    cur.execute(tmpl)
    rows = cur.fetchall()
    print("Results: \n")
    print_rows(rows)
    print()
    for row in rows:
        uid, first, last, email = row
        print("%s. %s, %s (%s)" % (uid, first, last, email))



# iterate over the drivers and find the closest one with the distance formula
# insert into rides table
  rider_id        SERIAL REFERENCES Riders (id),
  driver_id       SERIAL REFERENCES Drivers (id),
  start_latitude  FLOAT     NOT NULL,
  start_longitude FLOAT     NOT NULL,
  destination     TEXT      NOT NULL,
  start_datetime  TIMESTAMP NOT NULL,



    