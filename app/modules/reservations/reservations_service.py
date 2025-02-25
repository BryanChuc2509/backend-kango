from database import dbConnect
from bson.json_util import dumps, ObjectId
from flask import jsonify
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

class ReservationService:
    def __init__(self):
        self.db = dbConnect()
        if self.db is not None:
            self.reservations_collection = self.db["reservas"]
        else:
            self.reservations_collection = None

    def get_reservations(self):
        if self.db is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        reservations = list(self.reservations_collection.find({}))
        
        if not reservations:
            return {"message": "No hay reservaciones"}, 404
        
        for reservation in reservations:
            reservation["_id"] = str(reservation["_id"])
        
        return reservations, 200

    def get_reservation(self, reservation_id):
        if self.db is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            reservation = self.reservations_collection.find_one({"_id": ObjectId(reservation_id)})
            if not reservation:
                return {"message": "Reservación no encontrada"}, 404

            reservation["_id"] = str(reservation["_id"])
            return reservation, 200
        except Exception as e:
            logging.error(f"Error al buscar reservación {reservation_id}: {str(e)}")
            return {"error": "Error interno del servidor"}, 500

    def add_reservation(self, reservation_data):
        if self.reservations_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            required_fields = ["fecha_reservacion", "id_pasajero", "id_ruta", "estado_pago", 
                             "asientos", "usado", "id_pago", "id_vehiculo", "monto_total"]
            missing_fields = [field for field in required_fields if field not in reservation_data]

            if missing_fields:
                return {"error": f"Faltan los siguientes campos obligatorios: {', '.join(missing_fields)}"}, 400

            result = self.reservations_collection.insert_one(reservation_data)
            return {"message": "Reservación agregada", "id": str(result.inserted_id)}, 201

        except Exception as e:
            return {"error": f"Error al agregar reservación: {str(e)}"}, 500

    def update_reservation(self, reservation_id, reservation_data):
        if self.reservations_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.reservations_collection.update_one(
                {"_id": ObjectId(reservation_id)},
                {"$set": reservation_data}
            )
            if result.matched_count == 0:
                return {"message": "Reservación no encontrada"}, 404
            return {"message": "Reservación actualizada"}, 200
        except Exception as e:
            return {"error": f"Error al actualizar reservación: {str(e)}"}, 500

    def delete_reservation(self, reservation_id):
        if self.reservations_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.reservations_collection.delete_one({"_id": ObjectId(reservation_id)})
            if result.deleted_count == 0:
                return {"message": "Reservación no encontrada"}, 404
            return {"message": "Reservación eliminada"}, 200
        except Exception as e:
            return {"error": f"Error al eliminar reservación: {str(e)}"}, 500 