from distutils.file_util import move_file
import mysql.connector
from mysql.connector import Error
import sqlCommands

try:
    cnx = mysql.connector.connect(user='root', password='',
                                host='127.0.0.1',
                                database='media_recommendation',
                                use_pure=False)
    if cnx.is_connected():
        db_Info = cnx.get_server_info()
        print("\n\nConnected to MySQL Server version ", db_Info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute(sqlCommands.select_all)
        movie = cursor.fetchone()
        print(movie)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print("MySQL connection is closed")