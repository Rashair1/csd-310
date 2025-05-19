import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values
from datetime import datetime

# Load environment variables from .env
secrets = dotenv_values(".env")

# Configure database connection
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print(f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Report 1: Equipment Sales Summary
    cursor.execute("""
        SELECT 
            e.equipment_id,
            e.equipment_name,
            COUNT(t.transaction_id) AS total_transactions,
            SUM(t.transaction_price) AS total_revenue
        FROM transactions t
        JOIN equipment e ON t.equipment_id = e.equipment_id
        GROUP BY e.equipment_id, e.equipment_name
        ORDER BY total_revenue DESC;
    """)
    print("\nReport 1: Equipment Sales Summary")
    print("Equipment ID | Equipment Name | Total Transactions | Total Revenue")
    for row in cursor.fetchall():
        print(row)

    # Report 2: Regional Booking Trends
    cursor.execute("""
        SELECT 
            location,
            YEAR(departure_date) AS year,
            COUNT(*) AS total_bookings
        FROM trips
        GROUP BY location, YEAR(departure_date)
        ORDER BY location, year;
    """)
    print("\nReport 2: Regional Booking Trends")
    print("Location | Year | Total Bookings")
    for row in cursor.fetchall():
        print(row)

    # Report 3: Aging Inventory Report
    cursor.execute("""
        SELECT 
            equipment_id,
            equipment_name,
            date_purchased,
            ROUND(DATEDIFF(CURDATE(), date_purchased) / 365, 1) AS age_in_years
        FROM equipment
        WHERE date_purchased < CURDATE() - INTERVAL 5 YEAR;
    """)
    print("\nReport 3: Aging Inventory Report")
    print("Equipment ID | Equipment Name | Date Purchased | Age (Years)")
    for row in cursor.fetchall():
        print(row)
        df = pd.read_sql_query(query, connection)

    cursor.close()
    db.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Access denied: Check your username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)