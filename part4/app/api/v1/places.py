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
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        place_data = api.payload
        current_user = get_jwt_identity()
        new_place = facade.create_place(place_data)
        if current_user['id'] != place_data['owner_id']:
            return {'error': 'not authorized', 'current': current_user}, 401
        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": new_place.owner_id,
            "amenities": new_place.amenities
        }

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        lista = []
        lista2 = facade.get_all_places()
        for i in lista2:
            serializado = i.serializar_places()
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
