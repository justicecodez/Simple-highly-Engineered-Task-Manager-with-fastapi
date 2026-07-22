from passlib.context import CryptContext

class password_helper:

    def __init__(self):
        self.helper=CryptContext(schemes=["argon2"], deprecated='auto')

    def hash_helper(self, password)->str:
        return self.helper.hash(password)
    
    def verify_hash_helper(self, password, db_password)->bool:
        return self.helper.verify(password, db_password)
    