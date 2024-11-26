from app.models.baseclass import BaseModel
from app import db
from sqlalchemy.orm import relationship, validates


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False, unique=True)
    places = relationship(
        'Place',
        secondary='place_amenities',
        back_populates='amenities',
        lazy=True
    )

    @validates('name')
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or len(value) > 100:
            raise ValueError("Amenity name must be a non-empty string up to 100 characters")
        return value.strip()
