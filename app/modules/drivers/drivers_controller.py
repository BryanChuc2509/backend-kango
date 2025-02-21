from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from .drivers_service import DriverService

driver_service = DriverService()
api = Namespace("drivers", description="Operaciones con conductores")

# Modelo de datos para la documentación de Swagger
driver_model = api.model("Driver", {
    "nombre": fields.String(required=True, description="Nombre del conductor"),
    "apellido": fields.String(required=True, description="Número de licencia"),
    "correo_electronico": fields.String(required=True, description="Correo electronico"),
    "numero_telefonico": fields.String(required=True, description="Número telefónico"),
    "licencia_valida": fields.String(required=True, description="licencia valida"),
})


@api.route("/")
class DriverList(Resource):
    @api.doc("listar_conductores")
    def get(self):
        """Obtener todos los conductores"""
        return driver_service.get_drivers()

    @api.doc("agregar_conductor")
    @api.expect(driver_model)  # Valida el body de la petición
    def post(self):
        """Agregar un nuevo conductor"""
        driver_data = request.get_json()
        return driver_service.add_driver(driver_data)

@api.route("/<string:driver_id>")
@api.param("driver_id", "El ID del conductor")
class Driver(Resource):
    @api.doc("obtener_conductor")
    def get(self, driver_id):
        """Obtener un conductor por ID"""
        return driver_service.get_driver(driver_id)

    @api.doc("actualizar_conductor")
    @api.expect(driver_model)
    def put(self, driver_id):
        """Actualizar un conductor por ID"""
        driver_data = request.get_json()
        return driver_service.update_driver(driver_id, driver_data)

    @api.doc("eliminar_conductor")
    def delete(self, driver_id):
        """Eliminar un conductor por ID"""
        return driver_service.delete_driver(driver_id)
