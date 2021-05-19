from util.db_management.db_connection import connect_to_db
import random
import string

db = connect_to_db("links")

def generate_code(length):
    url_chars = string.ascii_letters + string.digits

    random_link = ''.join([random.choice(url_chars) for _ in range(length)])
    exists = db.find_one({'link_code': random_link})
    while exists:
        random_link = ''.join([random.choice(url_chars) for _ in range(length)])
        exists = db.find_one({'link_code': random_link})
    return random_link
