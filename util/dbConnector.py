import mysql.connector

cnx = mysql.connector.connect(user='', password='password',
                              host='127.0.0.1',
                              database='',
                              use_pure=False)
cnx.close()