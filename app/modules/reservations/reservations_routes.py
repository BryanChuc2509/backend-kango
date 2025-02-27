from flask import Blueprint, jsonify
from database import dbConnect  
from bson import ObjectId  

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route("/api/precio/<string:id_reserva>", methods=["GET"])
def obtener_precio(id_reserva):
    """Obtiene el precio de una reserva desde MongoDB con el id_reserva"""
    db = dbConnect()  

    try:
        #  id_reserva tiene 24 caracteres, intentamos convertirlo a ObjectId
        object_id = ObjectId(id_reserva) if len(id_reserva) == 24 else id_reserva
        reserva = db.reservas.find_one({"id_reserva": object_id})  
    except:
        return jsonify({"error": "Formato de ID inválido"}), 400  

    if not reserva:
        return jsonify({"error": "Reserva no encontrada"}), 404  

    return jsonify({
        "id_reserva": str(reserva["id_reserva"]),
        "precio": reserva.get("precio", 0)  
    }), 200
