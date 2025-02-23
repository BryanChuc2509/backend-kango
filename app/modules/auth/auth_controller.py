from flask import request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
from database import db
import jwt
import datetime
import pyotp
from config.settings import Config
from modules.auth.auth_models import Pasajero, Admin

# Importar librerías para generar QR
import qrcode
import io
import base64

GOOGLE_CLIENT_ID = "973428652330-pf4rncidpkqktjhnfr12vmf63h9l3rrg.apps.googleusercontent.com"  

class AuthController:

    @staticmethod
    def register(data):
        """Registra un nuevo pasajero con autenticación 2FA y genera el QR para Google Authenticator"""
        # Verificar que todos los campos estén presentes y no vacios
        required_fields = ["nombre", "apellido", "correo_electronico", "numero_telefonico", "password"]
        for field in required_fields:
            if field not in data or not data[field].strip():
                return {"error": f"El campo '{field}' es obligatorio y no puede estar vacío."}, 400

        email = data["correo_electronico"].strip()

        if Pasajero.find_by_email(email):
            return {"error": "El correo ya está registrado"}, 400

        pasajero = Pasajero(
            nombre=data["nombre"].strip(),
            apellido=data["apellido"].strip(),
            correo_electronico=email,
            numero_telefonico=data["numero_telefonico"].strip(),
            password=data["password"].strip()
        )

        Pasajero.save(pasajero)

        # Generar el url del Authenticator
        totp = pyotp.TOTP(pasajero.otp_secret)
        provisioning_uri = totp.provisioning_uri(name=email, issuer_name="KanGo")

        # Generar el QR  a partir del url
        qr_img = qrcode.make(provisioning_uri)
        buffered = io.BytesIO()
        qr_img.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {
            "message": "Pasajero registrado correctamente",
            "otp_secret": pasajero.otp_secret,
            "qr": qr_base64  # Este string se usa para mostrar la imagen en el front />
        }, 201

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

        totp = pyotp.TOTP(user["otp_secret"])
        if not totp.verify(otp_code):
            return {"error": "Código 2FA incorrecto"}, 400

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

            user = Pasajero.find_by_email(email)
            if not user:
                new_user = Pasajero(
                    nombre=nombre.strip(),
                    apellido=apellido.strip(),
                    correo_electronico=email.strip(),
                    numero_telefonico="",
                    password="google_oauth"  
                )
                Pasajero.save(new_user)
                user = new_user.to_dict()

            jwt_token = jwt.encode(
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
                "token": jwt_token,
                "rol": user["rol"],
            }, 200

        except Exception as e:
            return {"error": f"Error en la autenticación con Google: {str(e)}"}, 400
