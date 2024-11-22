from flask import json, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.user import User

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'mensaje': 'Creado con exito'}, 201

    def get(self):
        lista = []
        lista2 = facade.get_all()
        for i in lista2:
            serializado = i.serializar_usuario()
            lista.append(serializado)
        return lista

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully created')
    @api.response(400, 'Missing data')
    @jwt_required()
    def put(self, user_id):
        if not request.is_json:
            return {"error": "Unsupported Media Type. Content-Type should be 'application/json'"}, 415

        data = api.payload
        if not data.get("first_name") or not data.get("last_name") or not data.get("email"):
            return {"error": "Missing data"}, 400

        user = facade.update(user_id, data)
        data['id'] = user_id

        return jsonify(data)
    