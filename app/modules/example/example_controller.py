from flask import jsonify, request, Blueprint
from .example_service import UserService

# Instancia de la clase UserService del archivo example_service.py
user_service = UserService()

# blueprint creado para llamarlo en el archivo principal de la aplicacion
user_service_bp = Blueprint('user_service', __name__)

@user_service_bp.route('/', methods = ['GET'])
def get_users():
    return user_service.get_users()

@user_service_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return user_service.get_user(user_id)

@user_service_bp.route('/', methods=['POST'])
def add_user():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    if not name or not age:
        return jsonify({"error": "Nombre y edad son requeridos"}), 400
    return user_service.add_user(name, age)