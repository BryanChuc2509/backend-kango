from flask import request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
from database import db
import jwt
import datetime
import pyotp
from config.settings import Config
from modules.auth.auth_models import Pasajero, Admin

GOOGLE_CLIENT_ID = "973428652330-pf4rncidpkqktjhnfr12vmf63h9l3rrg.apps.googleusercontent.com"  

class AuthController:
#Registrar un nuevo pasajero con autenticación 2FA
    @staticmethod
    def register(data):
        """Registra un nuevo pasajero con autenticación 2FA"""
        if not all(k in data for k in ["nombre", "apellido", "correo_electronico", "numero_telefonico", "password"]):
            return {"error": "Todos los campos son obligatorios"}, 400

        email = data["correo_electronico"]

        if Pasajero.find_by_email(email):
            return {"error": "El correo ya está registrado"}, 400

        pasajero = Pasajero(
            nombre=data["nombre"],
            apellido=data["apellido"],
            correo_electronico=email,
            numero_telefonico=data["numero_telefonico"],
            password=data["password"]
        )

        Pasajero.save(pasajero)

        return {
            "message": "Pasajero registrado correctamente",
            "otp_secret": pasajero.otp_secret  
        }, 201
#Login con autenticación 2FA
    @staticmethod
    def login(data):
        """Inicio de sesión con 2FA para pasajeros y admins"""
        email = data.get("correo_electronico")
        password = data.get("password")
        otp_code = data.get("otp_code")

        # Buscar usuario en pasajeros o admins
        user = Pasajero.find_by_email(email) or Admin.find_by_email(email)

        if not user:
            return {"error": "Usuario no encontrado"}, 400

        if not Pasajero.verify_password(user["password"], password):
            return {"error": "Contraseña incorrecta"}, 400

        # Validar OTP
        totp = pyotp.TOTP(user["otp_secret"])
        if not totp.verify(otp_code):
            return {"error": "Código 2FA incorrecto"}, 400

        # Genera JWT para la sesión
        token = jwt.encode(
            {
                "correo_electronico": email,
                "rol": user["rol"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
            },
            Config.SECRET_KEY,
            algorithm="HS256",
        )

        return {
            "message": "Inicio de sesión exitoso",
            "token": token,
            "rol": user["rol"],
        }, 200
# Login con google
    @staticmethod
    def google_login(data):
        """Autenticación con Google"""
        token = data.get("token")
        if not token:
            return {"error": "Token de Google es requerido"}, 400

        try:
            # Verifica el token con Google
            google_data = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            
            email = google_data["email"]
            nombre = google_data.get("given_name", "Usuario")
            apellido = google_data.get("family_name", "")

            # Verificar si el usuario ya existe
            user = Pasajero.find_by_email(email)
            if not user:
                # Crear usuario si no existe
                new_user = Pasajero(
                    nombre=nombre,
                    apellido=apellido,
                    correo_electronico=email,
                    numero_telefonico="",
                    password="google_oauth"  
                )
                Pasajero.save(new_user)
                user = new_user.to_dict()

            # Generar token JWT para la sesión
            token = jwt.encode(
                {
                    "correo_electronico": email,
                    "rol": user["rol"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
                },
                Config.SECRET_KEY,
                algorithm="HS256",
            )

            return {
                "message": "Inicio de sesión exitoso con Google",
                "token": token,
                "rol": user["rol"],
            }, 200

        except Exception as e:
            return {"error": f"Error en la autenticación con Google: {str(e)}"}, 400