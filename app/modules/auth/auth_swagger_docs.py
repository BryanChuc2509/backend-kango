from flask_restx import fields, Model

# Modelo para el registro de pasajeros 
register_model = Model("Registro", {
    "nombre": fields.String(required=True, description="Nombre del pasajero"),
    "apellido": fields.String(required=True, description="Apellido del pasajero"),
    "correo_electronico": fields.String(required=True, description="Correo electrónico"),
    "numero_telefonico": fields.String(required=True, description="Número de teléfono"),
    "password": fields.String(required=True, description="Contraseña"),
})

# Modelo para el inicio de sesión (Sirve para pasajeros y admins)
login_model = Model("Login", {
    "correo_electronico": fields.String(required=True, description="Correo electrónico (Pasajero o Admin)"),
    "password": fields.String(required=True, description="Contraseña"),
    "otp_code": fields.String(required=True, description="Código de autenticación 2FA"),
})

# Modelo de respuesta del login
login_response_model = Model("LoginResponse", {
    "message": fields.String(description="Mensaje de éxito"),
    "token": fields.String(description="Token de autenticación"),
    "rol": fields.String(description="Rol del usuario (admin/pasajero)"),
})
