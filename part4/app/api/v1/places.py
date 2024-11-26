from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields, marshal
from app.services import facade
from app.models.user import User
from app.models.place import Place

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities IDs")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        place_data = api.payload
        current_user_id = get_jwt_identity()  # This is the user's ID as a string
        place_data['owner_id'] = current_user_id  # Set owner_id from the JWT identity

        # Validate required fields
        required_fields = ['title', 'description', 'price', 'latitude', 'longitude']
        for field in required_fields:
            if field not in place_data or not place_data[field]:
                return {'error': f'Missing field: {field}'}, 400

        # Create the new place
        try:
            new_place = facade.create_place(place_data)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner_id,
                "amenities": [amenity.name for amenity in new_place.amenities]
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        lista = []
        lista2 = facade.get_all_places()
        for i in lista2:
            serializado = i.serialize()
            lista.append(serializado)
        return lista


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')

    def get(self, place_id):
        place = facade.get_place(place_id)
        return marshal(place, place_model)


    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        data = api.payload
        current_user = get_jwt_identity()
        if data['owner_id'] != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        if not data["title"] or not data["description"] or not data["longitude"] or not data["latitude"] or not data["price"]:
            return {"error": "Missing data"}, 400
        place = facade.update(place_id, data)
        return {"message": "Place updated successfully", "data": data}, 200
    
@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()
        data = api.payload
        place = facade.get_place(place_id)
        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id: #comprueba que no sea la misma persona que lo creo
            return {'error': 'Unauthorized action'}, 403
        
        if not is_admin:
            if not data["title"] or not data["description"] or not data["longitude"] or not data["latitude"] or not data["price"]:
                return {"error": "Missing data"}, 400
            
            if data['longitude'] != place.longitude or data['latitude'] != place.latitude:
                return {"error": "Cannot modify Latitude or Longitude "}, 400
            
        place = facade.update(place_id, data)
        return {"message": "Place updated successfully", "data": data}, 200
        