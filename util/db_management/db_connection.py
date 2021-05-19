# rename this file to db_connection.py

from pymongo import MongoClient


def connect_to_db(table_name):
    """
        Utility, connects to the database
        :return: MongoDB cursor object
    """
    mongo = MongoClient("mongodb+srv://PhoneBotDBAccess:PBDB2021@cluster0.jiisa.mongodb.net/LinkRollDB?retryWrites"
                        "=true&w=majority")

    if table_name == "links": 
        return mongo.LinkRollDB.Links
    if table_name == "users":
        return mongo.LinkRollDB.Users
