from datetime import datetime
import mysql.connector
from mysql.connector import Error


def connection():
    try:
        connection = mysql.connector.connect(host='127.0.0.1', database='h3discord', user='root', password='root')
        if connection.is_connected():
            print("You're connected to database")
            return connection

        return None
    except Error as e:
        print("Error while connecting to MySQL", e)


def add_cmd(connection, cmd, user_id):
    try:
        cursor = connection.cursor()

        query = "INSERT INTO homepage_history (cmd, user_id, executed_at) VALUES (%s, %s, %s)"
        record = (cmd, user_id, datetime.now())

        cursor.execute(query, record)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
