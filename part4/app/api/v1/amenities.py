from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.amenity import Amenity

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        try:
            amenitie_data = api.payload
            current_user = get_jwt()
            if current_user.get("is_admin", False):
                return {'error': 'Admin privileges required'}, 403
            
            new_amenitie = facade.create_amenity(amenitie_data)
            return {
                'id': new_amenitie.id,
                'name': new_amenitie.name
                }, 201
        except ValueError as e:
            # Handle empty name error
            return {'error': str(e)}, 400


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        lista = []
        lista2 = facade.get_all_amenities()
        for i in lista2:
            serializar = i.serializar_amenities()
            lista.append(serializar)
        return lista


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        return {
            'id': amenity.id,
            'name': amenity.name
        }


    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    
    @jwt_required()
    def put(self, amenity_id):
        amenitie_data = api.payload
        current_user = get_jwt_identity()
        if current_user["is_admin"] == False:
            return {'error': 'Admin privileges required'}, 403
        
        facade.update_amenity(amenity_id, amenitie_data)
        return {"message": "Amenity updated successfully"}, 200