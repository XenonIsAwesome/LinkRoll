from util.db_management.db_connection import connect_to_db
from hashlib import sha256
import re

class User:
    def __init__(self, username=None):
        self.users_db = connect_to_db("users")
        self.username = ""
        self.passwd_hash = ""

        if username:
            user_doc = self.users_db.find_one({'username'})
            if user_doc:
                self.login(user_doc["username"], user_doc["passwd"])

    def login(self, username:str, passwd:str) -> bool:
        passwd_hash = sha256(passwd.encode("UTF-8")).hexdigest()

        user_doc = self.users_db.find_one({'username': username, 'passwd_hash': passwd_hash})
        
        if user_doc:
            self.username = username
            self.passwd_hash = passwd_hash

            return True
        return False
    
    def register(self, username:str, passwd:str) -> None:
        username_check = re.match(r"[a-zA-z0-9]{4,32}", username)
        passwd_check = re.match(r"[a-zA-z0-9]{8,32}", passwd)
        exists_check = self.users_db.find_one({'username': self.username})

        if not username_check or not passwd_check or exists_check:
            return False

        passwd_hash = sha256(passwd.encode("UTF-8")).hexdigest()
        
        self.users_db.insert_one({
            'username': username,
            'passwd_hash': passwd_hash
        })

        self.username = username
        self.passwd_hash = passwd_hash

        return True
