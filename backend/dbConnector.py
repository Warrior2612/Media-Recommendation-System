import mysql.connector
from mysql.connector import Error
import backend.sqlCommands

def conn(cnx = mysql.connector, conn_switch=True):
    if(conn_switch):
        try:
            cnx = mysql.connector.connect(user='root', password='',
                                    host='127.0.0.1',
                                    database='media_recommendation',
                                    use_pure=False)
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return cnx
    else:
        if cnx.is_connected():
            cnx.close()

def insert():
    cnx = conn()
    try:
        if cnx.is_connected():
            cursor = cnx.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute(backend.sqlCommands.select_all)
            movie = cursor.fetchone()
            print(movie)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        conn(cnx, False)

if __name__ == '__main__':
    insert()