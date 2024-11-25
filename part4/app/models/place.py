from app.models.baseclass import BaseModel
from app import db
from sqlalchemy.orm import validates


class Place(BaseModel):

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.relationship('users', backref='owner', lazy=True)
    reviews = db.relationship('review', backref='place', lazy=True)
    amenities =  db.relationship('amenities', secondary='place_amenities', backref='places')

    def __init__(self, title: str, description: str, price: float, latitude: float, longitude: float, owner_id, amenities):
        super().__init__()
        if self.validate_title(title):
            self.title = title
        if self.validate_description(description):
            self.description = description
        if self.validate_price(price):
            self.price = price
        if self.validate_latitude(latitude):
            self.latitude = latitude
        if self.validate_longitude(longitude):
            self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = amenities
    

    @staticmethod
    @validates('title')
    def validate_title(title):
        if type(title) is not str:
            raise TypeError("Title not valid")
        if len(title) > 100:
            raise ValueError("Title cannot contain more than 100 characters")
        return True

    @staticmethod
    @validates('description')
    def validate_description(description):
        if type(description) is not str:
            raise TypeError("Description not valid")
        return True

    @staticmethod
    @validates('price')
    def validate_price(price):
        if type(price) is not float and type(price) is not int:
            raise ValueError("Error: Price not valid")
        if price < 0:
            raise ValueError("Price must be greater than 0")
        return True

    @staticmethod
    @validates('latitude')
    def validate_latitude(latitude):
        if type(latitude) is not float and type(latitude) is not int:
            raise TypeError("Latitude not valid")
        if latitude > 90.0 or latitude < -90.0:
            raise ValueError("Latitude not valid")
        return True

    @staticmethod
    @validates('longitude')
    def validate_longitude(longitude):
        if type(longitude) is not float and type(longitude) is not int:
            raise TypeError("Longitude not valid")
        if longitude > 180.0 or longitude < -180.0:
            raise ValueError("Longitude not valid")
        return True

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def serializar_places(self):
            return {
                "id": self.id,
                "title": self.title,
                "latitude": self.latitude,
                "longitude": self.longitude
            }
    
class PlaceAmenity(db.Model):
    amenity_id = db.Column(db.String, db.ForeignKey("amenity.id"), primary_key=True)
    place_id = db.Column(db.String, db.ForeignKey("place.id"), primary_key=True)