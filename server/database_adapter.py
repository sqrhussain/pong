import sqlite3
from sqlite3 import Error

database = "/database/database.db"

def create_connection(database_file):
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except Error as e:
        print(e)

    return None


def getplayerid(player_name):

    # Please don't sqlinject tyvm

    conn = create_connection(database)
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Players WHERE name=\"" + player_name + "\";")
        rows = cursor.fetchall()
        return rows #to retrieve use 'for row in rows:'


def getplayerhighscore(player_name):

    # Please don't sqlinject tyvm

    conn = create_connection(database)
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT highscore FROM Players WHERE name=\"" + player_name + "\";")
        rows = cursor.fetchall()
        return rows #to retrieve use 'for row in rows:'
