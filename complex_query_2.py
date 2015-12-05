# 9. As a rider, I want to get the driver that is nearest to my location

#-----------------------------------------------------------------
# Working with psycopg2
#-----------------------------------------------------------------

import psycopg2
import sys

def heading(str):
    print('-'*60)
    print("** %s:" % (str,))
    print('-'*60, '\n')    

SHOW_CMD = True
def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))



def print_rows(rows):
    for row in rows:
        print(row)

def get_nearest_driver():
	tmpl = '''


	'''
	print("SQL Statement: ")
	print(tmpl)
	cur.execute(tmpl)
    rows = cur.fetchall()
    print("Results: \n")
    print_rows(rows)
    print()





    