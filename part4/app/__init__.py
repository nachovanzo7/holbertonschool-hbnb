from flask import Flask, render_template
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Instancias globales de extensiones
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Configurar la API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/', prefix="/api/v1")

    # Importar y registrar namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as login_ns

    api.add_namespace(users_ns, path='/users')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(login_ns, path='/auth')

    # Rutas de frontend
    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/places/')
    def places_page():
        return render_template('place.html')

    @app.route('/home')
    def home_page():
        return render_template('index.html')

    # Crear tablas
    with app.app_context():
        from app.models.amenity import Amenity
        from app.models.place import Place, PlaceAmenity
        from app.models.review import Review
        from app.models.user import User

        db.create_all()

    return app
