import re
from app.models.basemodel import BaseModel
from flask_bcrypt import bcrypt, Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, password, is_admin=False):
        super().__init__()
        if self.validate_first_name(first_name) and self.validate_last_name(last_name):
            self.first_name = first_name
            self.last_name = last_name
        if self.validate_email(email):
            self.email = email
        self.is_admin = is_admin
        self.password = self.hash_password(password)

    @staticmethod
    def validate_first_name(first_name):
        if type(first_name) is not str:
            raise TypeError("Name not valid")
        if len(first_name) > 50:
            raise ValueError("Name cannot contain more than 50 characters")
        return True

    @staticmethod
    def validate_last_name(last_name):
        if type(last_name) is not str:
            raise TypeError("Name not valid")
        if len(last_name) > 50:
            raise ValueError("Name cannot contain more than 50 characters")
        return True

    @staticmethod
    def validate_email(email):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, email):
            return True
        else:
            raise TypeError("Email not valid")

    def serializar_usuario(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)