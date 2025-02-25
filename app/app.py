from flask import Flask, jsonify
from flask_restx import Api
from flask_cors import CORS
from modules.auth.auth_routes import api as auth_api
from modules.drivers.drivers_controller import api as driver_api
from modules.routes.routes_controller import api as routes_api
from modules.metrics.metrics_controller import api as metrics_api
from modules.reservations.reservations_routes import reservas_bp
from modules.payments.routes import api as payments_api
from database import dbConnect
from bson import ObjectId
from modules.places.places import api as places_api
from modules.vehicles.vehicles_controller import api as vehicles_api
from modules.reservations.reservations_controller import api as reservations_api
from modules.payments.routes import api as payments_api

app = Flask(__name__)
CORS(app, supports_credentials=True, origins="*")


api = Api(app, version="1.0", title="API de KanGo", description="Documentación con Flask-RESTx")

# Esto se va a añadir al servicio de pasajeros, para obtener datos de la bd. Aquí empieza
db = dbConnect()

# Función para convertir los documentos que contienen ObjectId a cadenas
def convert_objectid_to_str(document):
    for key, value in document.items():
        if isinstance(value, ObjectId):
            document[key] = str(value)  # Convierte ObjectId a string
    return document


import base64

# Función para convertir el ObjectId y bytes a formatos serializables en JSON
def convert_to_serializable(document):
    for key, value in document.items():
        if isinstance(value, ObjectId):
            document[key] = str(value)  # Convertir ObjectId a string
        elif isinstance(value, bytes):
            document[key] = base64.b64encode(value).decode('utf-8')  # Convertir bytes a base64
    return document

@app.route("/structure")
def structure():
    try:
        # Fetch all documents from the 'pasajeros' collection
        pasajeros_collection = db["pasajeros"]
        pasajeros = list(pasajeros_collection.find({}))  # List of all documents
        
        if not pasajeros:
            # Return a proper JSON response if no pasajeros are found
            return jsonify({"message": "No hay pasajeros"})
        
        # Convert ObjectId and bytes to serializable formats
        pasajeros = [convert_to_serializable(pasajero) for pasajero in pasajeros]
        
        # Return the list of pasajeros as a JSON response
        return jsonify(pasajeros)
    
    except Exception as e:
        # Return error as JSON response
        return jsonify({"error": f"Error fetching collection info: {str(e)}"}), 500

# Aquí termina 

# Registrar el namespace de auth
api.add_namespace(auth_api, path="/auth")

# Registrar el namespace de conductores
api.add_namespace(driver_api, path="/api/drivers")

# Registrar el namespace de metrics
api.add_namespace(metrics_api, path="/api/metrics")

# Registrar el namespace de payments
api.add_namespace(payments_api, path="/payments")
# devuelve el precio de cada reserva
app.register_blueprint(reservas_bp)
# Registrar el namespace de places
api.add_namespace(places_api, path="/api/places")

# Registrar el namespace de reservations
api.add_namespace(reservations_api, path="/api/reservations")

# Registrar el namespace de routes
api.add_namespace(routes_api, path="/api/routes")


# Registrar el namespace de vehicles
api.add_namespace(vehicles_api, path="/api/vehicles")


if __name__ == '__main__':
    app.run(debug=True)