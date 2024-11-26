from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.UserRepository import UserRepository
from app import db


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)


    # Functions for user
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all(self):
        return self.user_repo.get_all()

    def update(self, user_id, data):
        return self.user_repo.update(user_id, data)


    # Functions for Amenities
    def create_amenity(self, amenity_data):
        amenity_name = amenity_data.get('name', '').strip()
        if not amenity_name:
            raise ValueError("Amenity name cannot be empty")

        # Check if the amenity already exists
        existing_amenity = self.amenity_repo.get_by_attribute('name', amenity_name)
        if existing_amenity:
            raise ValueError(f"Amenity '{amenity_name}' already exists")

        # Create and add the new amenity
        amenity = Amenity(name=amenity_name)
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)


    # Functions for place
    # app/services/facade.py

    def create_place(self, place_data):
        with db.session.begin():
            amenities_names = place_data.pop('amenities', [])
            place = Place(**place_data)
            if amenities_names:
                amenities = []
                for amenity_name in amenities_names:
                    # Normalize the amenity name
                    normalized_name = amenity_name.strip()
                    amenity = self.amenity_repo.get_by_attribute('name', normalized_name)
                    if not amenity:
                        # Optionally create the amenity if it doesn't exist
                        amenity = Amenity(name=normalized_name)
                        db.session.add(amenity)
                    amenities.append(amenity)
                place.amenities = amenities
            db.session.add(place)
        return place




    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)


    # Functions for review
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
    