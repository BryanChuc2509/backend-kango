# app/modules/places/places_service.py
from app.database import dbConnect
from bson.json_util import dumps, ObjectId
from flask import jsonify
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

class PlacesService:
    def __init__(self):
        self.db = dbConnect()
        if self.db is not None:
            self.places_collection = self.db["destinos"]
        else:
            self.places_collection = None

    def get_places(self):
        if self.db is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        places = list(self.places_collection.find({}))

        if not places:
            return {"message": "No hay lugares"}, 404

        # Convert ObjectId to string
        for place in places:
            place["_id"] = str(place["_id"])

        return places, 200

    def add_place(self, place_data):
        if self.places_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            required_fields = ["nombre", "cordenadas", "direccion", "estado"]
            missing_fields = [field for field in required_fields if field not in place_data or not str(place_data[field]).strip()]

            if missing_fields:
                return {"error": f"Faltan los siguientes campos obligatorios: {', '.join(missing_fields)}"}, 400

            place = self.places_collection.find_one({
                "nombre": place_data["nombre"]
            })
            if place:
                return {"error": "El lugar ya existe"}, 400

            result = self.places_collection.insert_one(place_data)

            return {"message": "Lugar agregado", "id": str(result.inserted_id)}, 201

        except Exception as e:
            return {"error": f"Error al agregar lugar: {str(e)}"}, 500

    def delete_place(self, place_id):
        if self.places_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.places_collection.delete_one({"_id": ObjectId(place_id)})
            if result.deleted_count == 0:
                return {"message": "Lugar no encontrado"}, 404
            return {"message": "Lugar eliminado"}, 200
        except Exception as e:
            return {"error": f"Error al eliminar lugar: {str(e)}"}, 500

    def update_place(self, place_name, place_data):
        if self.places_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.places_collection.update_one(
                {"nombre": place_name},
                {"$set": place_data}
            )
            if result.matched_count == 0:
                return {"message": "Lugar no encontrado"}, 404
            return {"message": "Lugar actualizado"}, 200
        except Exception as e:
            return {"error": f"Error al actualizar lugar: {str(e)}"}, 500