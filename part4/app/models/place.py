from app.models.baseclass import BaseModel
from app import db
from sqlalchemy.orm import relationship, validates


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = relationship('Review', back_populates='place', lazy=True)
    amenities = relationship(
        'Amenity',
        secondary='place_amenities',
        back_populates='places',
        lazy=True
    )

    @staticmethod
    @validates('title')
    def validate_title(key, title):
        if not isinstance(title, str) or len(title) > 100:
            raise ValueError("Title must be a string and max 100 characters")
        return title

    @staticmethod
    @validates('price')
    def validate_price(key, price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a positive number")
        return price

    @staticmethod
    @validates('latitude')
    def validate_latitude(key, latitude):
        if not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        return latitude

    @staticmethod
    @validates('longitude')
    def validate_longitude(key, longitude):
        if not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        return longitude
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "amenities": [amenity.name for amenity in self.amenities]
        }


class PlaceAmenity(db.Model):
    __tablename__ = 'place_amenities'

    amenity_id = db.Column(db.String, db.ForeignKey('amenities.id'), primary_key=True)
    place_id = db.Column(db.String, db.ForeignKey('places.id'), primary_key=True)
