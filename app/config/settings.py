import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_super_segura")
