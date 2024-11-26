from app.models.baseclass import BaseModel
from app import db
from sqlalchemy.orm import relationship, validates


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    place = relationship('Place', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    @staticmethod
    @validates('text')
    def validate_text(key, text):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string")
        return text

    @staticmethod
    @validates('rating')
    def validate_rating(key, rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
