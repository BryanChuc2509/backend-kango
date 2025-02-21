from flask import Blueprint
from modules.auth.auth_routes import auth_bp

api_bp = Blueprint('api', __name__)

# Registrar los modulos para app.py
api_bp.register_blueprint(auth_bp, url_prefix='/auth')
