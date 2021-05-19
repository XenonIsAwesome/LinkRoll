# rename this file to db_connection.py

from pymongo import MongoClient


def connect_to_db(table_name):
    """
        Utility, connects to the database
        :return: MongoDB cursor object
    """
    mongo = MongoClient("add-your-mongo-uri")

    if table_name == "links": 
        return mongo.LinkRollDB.Links
    if table_name == "users":
        return mongo.LinkRollDB.Users
