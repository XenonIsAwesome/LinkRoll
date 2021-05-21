from os import link
from util.db_management.db_connection import connect_to_db
import random
import string
import re

db = connect_to_db("links")

def generate_code(length):
    url_chars = string.ascii_letters + string.digits

    random_link = ''.join([random.choice(url_chars) for _ in range(length)])
    exists = db.find_one({'link_code': random_link})
    while exists:
        random_link = ''.join([random.choice(url_chars) for _ in range(length)])
        exists = db.find_one({'link_code': random_link})
    return random_link


def insert_code(is_custom, link_code, discord_link, user_link=None, custom_user=None):
    if not user_link:
        user_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    exp = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

    if not re.match(exp, discord_link):
        return {'success': False, 'err': 'Discord embed link has to be a link.'}
    if not re.match(exp, user_link):
        return {'success': False, 'err': 'User link has to be a link.'}
    
    if not is_custom:
        doc = db.find_one({
            'discord_link': discord_link,
            'user_link': user_link
        })

        if doc:
            return {
                'success': True, 
                'err': None, 
                'link_code': doc['link_code']
            }
        
    elif link_code in ['login', 'logout', 'register', 'custom']:
        return {'success': False, 'err': "You canno't use this custom URL."}
    
    db.insert_one({
        'link_code': link_code,
        'discord_link': discord_link,
        'user_link': user_link,
        'custom_user': custom_user
    })

    return {'success': True, 'err': None, 'link_code': link_code}


def check_user_agent(ua: str) -> bool:
    for social in ['discord', 'twitter', 'whatsapp']:
        if social in ua.lower():
            return True
    return False
