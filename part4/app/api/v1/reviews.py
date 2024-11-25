from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields, marshal
from app.services import facade
from app.models.review import Review

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        review_data = api.payload
        current_user = get_jwt_identity()
        place = facade.get_place(review_data['place_id'])
        reviews = facade.get_all_reviews()
        user = facade.get_user(review_data['user_id'])

        for review in reviews: #Ya hizo la review el usuario
            if review.place_id == review_data['place_id'] and review.user_id == review_data['user_id']:
                return {'error': "You have already reviewed this place."}, 400

        if review_data['user_id'] == place.owner_id: #el user no puede comentar su propio place
            return {"Error": "You cannot review your own place."}, 400

        if user is None: #User no existe
            return {"error": "User not found"}, 400

        if place is None: #place no esxiste
            return {"error": "place not found"}, 400
               
    
        new_review = facade.create_review(review_data)

        return {
            "id": new_review.id,
            "text": new_review.text,
            "rating": new_review.rating,
            "user_id": new_review.user_id,
            "place_id": new_review.place_id
        }, 200

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        lista = []
        lista2 = facade.get_all_reviews()
        for i in lista2:
            serializar = i.serializar_reviews()
            lista.append(serializar)
        return lista

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        new_review = facade.get_review(review_id)
        return marshal(new_review, review_model), 200


    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        review_data = api.payload
        review = facade.get_review(review_id)
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        if not is_admin:
            if review_data['user_id'] != current_user['id']:
                return {"error": "Unauthorized action"}, 403
        
        
        facade.update_review(review_id, review_data)
        return {'message': 'Review updated successfully'}, 200
    
    

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        review_data = facade.get_review(review_id)
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        if not is_admin:
            if review_data.user_id != current_user['id']:
                return {"error": "Unauthorized action"}, 403
        
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        
        reviews_list = facade.get_reviews_by_place(place_id)
        return marshal(reviews_list, review_model), 200