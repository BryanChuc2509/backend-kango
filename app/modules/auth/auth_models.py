from database import db  
import uuid
import bcrypt
import pyotp
#Modelo para Pasajeros
class Pasajero:
    def __init__(self, nombre, apellido, correo_electronico, numero_telefonico, password):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.apellido = apellido
        self.correo_electronico = correo_electronico
        self.numero_telefonico = numero_telefonico
        self.password = self.hash_password(password)
        self.otp_secret = pyotp.random_base32()
        self.rol = "pasajero"

    def hash_password(self, password):
        """Encripta la contraseña con bcrypt"""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def to_dict(self):
        """Convierte el objeto en un diccionario para guardar en MongoDB"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo_electronico": self.correo_electronico,
            "numero_telefonico": self.numero_telefonico,
            "password": self.password,
            "otp_secret": self.otp_secret,
            "rol": self.rol,  
        }

    @staticmethod
    def find_by_email(email):
        """Busca un pasajero por su correo"""
        return db["pasajeros"].find_one({"correo_electronico": email})  

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verifica si la contraseña es correcta"""
        return bcrypt.checkpw(provided_password.encode("utf-8"), stored_password)

    @staticmethod
    def save(pasajero):
        """Guarda un pasajero en la base de datos"""
        return db["pasajeros"].insert_one(pasajero.to_dict())  


# Modelo para Administradores
class Admin:
    def __init__(self, nombre, correo_electronico, password):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.password = self.hash_password(password)
        self.otp_secret = pyotp.random_base32()
        self.rol = "admin"

    def hash_password(self, password):
        """Encripta la contraseña con bcrypt"""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def to_dict(self):
        """Convierte el objeto en un diccionario para MongoDB"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo_electronico": self.correo_electronico,
            "password": self.password,
            "otp_secret": self.otp_secret,
            "rol": self.rol,
        }

    @staticmethod
    def find_by_email(email):
        """Busca un admin en la base de datos"""
        return db["admins"].find_one({"correo_electronico": email}) 

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verifica la contraseña del admin"""
        return bcrypt.checkpw(provided_password.encode("utf-8"), stored_password)

    @staticmethod
    def save(admin):
        """Guarda un administrador en la base de datos"""
        return db["admins"].insert_one(admin.to_dict())  
