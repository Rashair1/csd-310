#Rashai Robertson
#CSD_310
#4/27/2025
#Module 7.2

""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}
try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database

    # output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                       config["database"]))

    input("\n\n  Press any key to continue...")

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

cursor = db.cursor()
# Execute a query to fetch all rows from table named 'studio'
cursor.execute("SELECT studio_id, studio_name FROM studio")

# Fetch all results from the executed query
studios = cursor.fetchall()
print ("-- DISPLAYING Studio RECORDS --")
# Print the results
for studio in studios:

    print("Studio ID: {}\n Studio Name:{}\n" .format(studio[0], studio[1], studio[0]))

# Execute a query to fetch all rows from table named 'genre'
cursor.execute("SELECT genre_id, genre_name FROM genre")

# Fetch all results from the executed query
genres = cursor.fetchall()
print ("-- DISPLAYING Genre RECORDS --")
# Print the results
for genre in genres:

    print("Genre ID: {}\n Genre Name:{}\n" .format(genre[0], genre[1], genre[0]))

# Execute a query to fetch all rows from table named 'film'
cursor.execute("SELECT film_name, film_runtime FROM film")

# Fetch all results from the executed query
films = cursor.fetchall()
print ("-- DISPLAYING Short Film RECORDS --")
# Print the results
for film in films:

    print("Film Name: {}\n Runtime:{}\n" .format(film[0], film[1]))

cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_releaseDate DESC")

# Fetch all results from the executed query
films = cursor.fetchall()
print ("-- DISPLAYING Director in Order RECORDS --")
# Print the results
for film in films:

    print("Film Name: {}\n Director:{}\n" .format(film[0], film[1]))

db.close()

