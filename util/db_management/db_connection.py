from pymongo import MongoClient
import os


def connect_to_db(table_name):
    """
        Utility, connects to the database
        :return: MongoDB cursor object
    """
    # heroku config:set API_KEY=your-mongo-uri

    mongo_uri = os.getenv('MONGO_URI')
    mongo = MongoClient(mongo_uri)

    if table_name == "links": 
        return mongo.LinkRollDB.Links
    if table_name == "users":
        return mongo.LinkRollDB.Users
