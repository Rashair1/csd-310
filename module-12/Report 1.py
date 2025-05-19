#Silver Group
#Rashai R.
#Crystal
#Tyspn B.

#CSD_310
#5/17/2025
#Module 12

""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
from prettytable import PrettyTable
from datetime import datetime
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
    print()

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)
cursor = db.cursor()

#updating equipment stock from sold quantity.
sql = "UPDATE equipment SET stock = stock - (SELECT SUM(s.quantity) FROM sales s WHERE s.equipment_id = equipment.equipment_id) WHERE EXISTS (SELECT 1 FROM sales s WHERE s.equipment_id = equipment.equipment_id)"

query3 = "SELECT COUNT(sale_id) AS 'Number of Equipment Sales' FROM sales"
cursor.execute(query3)
rows = cursor.fetchall()
table3 = PrettyTable()
table3.field_names = [i[0] for i in cursor.description]  # Set column headers from query result
# Add rows to the table
for row in rows:
    table3.add_row(row)
    # Print the table
print("Equipment Sales Report:"f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(table3)

query = """
    SELECT equipment_name, SUM(quantity) AS total_quantity, 
        SUM(quantity * sale_total) AS total_sales
    FROM sales
    GROUP BY equipment_name
    ORDER BY total_sales DESC;
    """
cursor.execute(query)
results = cursor.fetchall()

# Generate a formatted report
table = PrettyTable(["Product Name", "Total Quantity Sold", "Total Sales ($)"])
for row in results:
    table.add_row(row)

print(table)


query2 = "SELECT equipment_name AS 'Product Name', stock AS 'Remaining Stock' FROM equipment ORDER BY stock DESC"
cursor.execute(query2)
rows = cursor.fetchall()
table2 = PrettyTable()
table2.field_names = [i[0] for i in cursor.description]  # Set column headers from query result
# Add rows to the table
for row in rows:
    table2.add_row(row)
    # Print the table
print(table2)
print()
print()


query4 = "SELECT location AS 'Location', COUNT(*) AS 'Total Trips' FROM trips GROUP BY location ORDER BY 'Total Trips' DESC"
cursor.execute(query4)
rows = cursor.fetchall()
table4 = PrettyTable()
table4.field_names = [i[0] for i in cursor.description]  # Set column headers from query result
# Add rows to the table
for row in rows:
    table4.add_row(row)
    # Print the table
print("----------------------------------------------------------------------------------------------------------------")
print()
print("Regional Booking Trends:")
print(table4)
print()
print()

query5 = "SELECT equipment_name AS 'Product Name', date_stocked AS 'Date Stocked', ROUND(DATEDIFF(CURDATE(), date_stocked) / 365, 1) AS 'Age (Years.Months)' FROM equipment WHERE date_stocked < CURDATE() - INTERVAL 5 YEAR"
cursor.execute(query5)
rows = cursor.fetchall()
table5 = PrettyTable()
table5.field_names = [i[0] for i in cursor.description]  # Set column headers from query result
# Add rows to the table
for row in rows:
    table5.add_row(row)
    # Print the table
print("----------------------------------------------------------------------------------------------------------------")
print()
print("Equipment Stocked 5+ Years Ago:")
print(table5)
#print("Regional Booking Trends")
#print(table4)




db.close()
