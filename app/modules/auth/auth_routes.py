from flask import request
from flask_restx import Namespace, Resource
from modules.auth.auth_swagger_docs import register_model, login_model, login_response_model


api = Namespace("auth", description="APIs de autenticación")

#  los modelos en Swagger-RESTx
api.models[register_model.name] = register_model
api.models[login_model.name] = login_model
api.models[login_response_model.name] = login_response_model
#rutas de registro

@api.route("/register")
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """Registro de un nuevo pasajero con 2FA"""
        from modules.auth.auth_controller import AuthController  #  Importación dentro de la función por errores gg
        data = api.payload
        return AuthController.register(data)
#rutas del login

@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, "Éxito", login_response_model)
    def post(self):
        """Inicio de sesión con validación 2FA para pasajeros y administradores"""
        from modules.auth.auth_controller import AuthController  #  Importación dentro de la función por errores gg
        data = api.payload
        return AuthController.login(data)
#rutas de google login

@api.route("/google-login")
class GoogleLogin(Resource):
    def post(self):
        """Inicio de sesión con Google OAuth"""
        from modules.auth.auth_controller import AuthController  #  Importación dentro de la función por errores gg
        data = request.get_json()
        return AuthController.google_login(data)
