from app.models.baseclass import BaseModel
from app import db, bcrypt
from sqlalchemy.orm import relationship, validates
import re


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relaciones
    places = relationship('Place', backref='owner', lazy=True)
    reviews = relationship('Review', backref='reviewer', lazy=True)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.hash_password(password)
        self.is_admin = is_admin

    @staticmethod
    @validates('email')
    def validate_email(key, email):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if not re.match(regex, email):
            raise ValueError("Invalid email format")
        return email

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }

    def hash_password(self, password):
        """Hashes the password for storage."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password, password)
