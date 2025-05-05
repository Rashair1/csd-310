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



cursor.execute("CREATE TABLE customer (customer_id INT AUTO_INCREMENT PRIMARY KEY, customer_name VARCHAR(255), email VARCHAR(255))")


cursor.execute("CREATE TABLE employee (employee_id INT AUTO_INCREMENT PRIMARY KEY, employee_name VARCHAR(55))")



cursor.execute("CREATE TABLE trip (trip_id INT AUTO_INCREMENT PRIMARY KEY, trip_name VARCHAR(255), trip_location VARCHAR(255), trip_price INT, FOREIGN KEY (employee_id) REFERENCES employee(employee_id), FOREIGN KEY (customer_id) REFERENCES customer(customer_id))")




#def show_trips (cursor, title) :
# method to execute an inner join on all tables,
#iterate over the dataset and output the results to the terminal window.

# inner join query
#    cursor.execute ("select trip_name as Name, employee_name as Director, trip_location as Genre, studio_name as 'Studio Name' from film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id")

# get the results from the cursor object
#    trips = cursor.fetchall ()

#    print ("\n -- {} -- ".format (title) )

# iterate over the film data set and display the results
#    for trip in trips:
#        print ("Trip Name: {}\n Director: {}\n Genre Name ID: {}\n Studio Name: {}\n".format (film[0], film[1], film[2], film[3] ) )

#show_trips(cursor, "DISPLAYING TRIPS")



#db.close()


