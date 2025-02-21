from flask import Flask
from flask_restx import Api
from .modules.drivers.drivers_controller import api as driver_api
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


api = Api(app, version="1.0", title="API de Gestión de Conductores", description="Documentación con Flask-RESTx")

# Registrar el namespace de auth

# Registrar el namespace de conductores
api.add_namespace(driver_api, path="/api/drivers")

# Registrar el namespace de metrics

# Registrar el namespace de payments

# Registrar el namespace de places

# Registrar el namespace de reservations

# Registrar el namespace de routes

# Registrar el namespace de vehicles


if __name__ == '__main__':
    app.run(debug=True)