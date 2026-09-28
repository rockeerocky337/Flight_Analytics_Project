import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Roma@081293",
    database="flight_analytics"
)

print("MySQL connection successful!")

connection.close()