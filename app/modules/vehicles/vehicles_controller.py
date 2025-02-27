
from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from .vehicles_service import VehiclesService

vehicles_service = VehiclesService()
api = Namespace("Vehicles", description="Operaciones con vehículos")

# Modelo de datos para la documentación de Swagger
vehiculo_model = api.model("Vehiculo", {
    "modelo": fields.String(required=False, description="Modelo del vehículo"),
    "placa": fields.String(required=False, description="Placa del vehículo"),
    "numAsientos": fields.Integer(required=False, description="Número de asientos del vehículo"),
    "estado": fields.String(required=False, description="Estado del vehículo"),
    # "viajes_completados": fields.String(required=True, description="Número de viajes completados"),
    "calidad": fields.String(required=False, description="Calidad del vehículo"),
    # "costoKm": fields.String(required=True, description="Costo por kilómetro del vehículo"),
    # "kilometraje_media": fields.String(required=True, description="Kilometraje promedio del vehículo"),
    "marca": fields.String(required=False, description="Marca del vehículo")
})



@api.route("/")
class VehicleList(Resource):
    @api.doc("listar_vehiculos")
    def get(self):
        return vehicles_service.get_vehicles()

    @api.doc("agregar_vehiculo")
    @api.expect(vehiculo_model)  # Valida el body de la petición
    def post(self):
        """Agregar un nuevo conductor"""
        vehicle_data = request.get_json()
        return vehicles_service.add_vehicle(vehicle_data)

@api.route("/<string:vehicle_id>")
@api.param("vehicle_id", "El ID del conductor")
class Vehicle(Resource):
    @api.doc("obtener_conductor")
    def get(self, vehicle_id):
        return vehicles_service.get_vehicle(vehicle_id)


    @api.doc("actualizar_conductor")
    @api.expect(vehiculo_model)
    def put(self, vehicle_id):
        driver_data = request.get_json()
        return vehicles_service.update_vehicle(vehicle_id, driver_data)

    @api.doc("eliminar_vehiculo")
    def delete(self, vehicle_id):
        return vehicles_service.delete_vehicle(vehicle_id) 
