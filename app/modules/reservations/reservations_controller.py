from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from .reservations_service import ReservationService

reservation_service = ReservationService()
api = Namespace("reservations", description="Operaciones con reservaciones")

# Modelo de datos para la documentación de Swagger
reservation_model = api.model("Reservation", {
    "fecha_reservacion": fields.DateTime(required=True, description="Fecha de la reservación"),
    "id_pasajero": fields.String(required=True, description="ID del pasajero"),
    "id_ruta": fields.String(required=True, description="ID de la ruta"),
    "estado_pago": fields.String(required=True, description="Estado del pago (pagado/pendiente)"),
    "asientos": fields.Integer(required=True, description="Número de asientos reservados"),
    "usado": fields.Boolean(required=True, description="Indica si la reservación fue utilizada"),
    "id_pago": fields.String(required=True, description="ID del pago asociado"),
    "id_vehiculo": fields.String(required=True, description="ID del vehículo asignado"),
    "monto_total": fields.Float(required=True, description="Monto total a pagar por la reservación")
})

@api.route("/")
class ReservationList(Resource):
    @api.doc("listar_reservaciones")
    def get(self):
        """Obtener todas las reservaciones"""
        return reservation_service.get_reservations()

    @api.doc("agregar_reservacion")
    @api.expect(reservation_model)
    def post(self):
        """Agregar una nueva reservación"""
        reservation_data = request.get_json()
        return reservation_service.add_reservation(reservation_data)

@api.route("/<string:reservation_id>")
@api.param("reservation_id", "El ID de la reservación")
class Reservation(Resource):
    @api.doc("obtener_reservacion")
    def get(self, reservation_id):
        """Obtener una reservación por ID"""
        return reservation_service.get_reservation(reservation_id)

    @api.doc("actualizar_reservacion")
    @api.expect(reservation_model)
    def put(self, reservation_id):
        """Actualizar una reservación por ID"""
        reservation_data = request.get_json()
        return reservation_service.update_reservation(reservation_id, reservation_data)

    @api.doc("eliminar_reservacion")
    def delete(self, reservation_id):
        """Eliminar una reservación por ID"""
        return reservation_service.delete_reservation(reservation_id) 