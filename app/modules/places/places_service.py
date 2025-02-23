from app.database import dbConnect
from bson.json_util import dumps, ObjectId
from flask import jsonify
import logging
from typing import Dict, Tuple, Any

logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class PlacesService:
    def __init__(self):
        self.db = dbConnect()
        if self.db is not None:
            self.places_collection = self.db["destinos"]
        else:
            self.places_collection = None
            logger.error("No se pudo establecer conexión con la base de datos")

    def validate_place_data(self, place_data: Dict) -> Tuple[bool, str]:
        """Validar los datos del lugar"""
        required_fields = ["nombre", "cordenadas", "direccion", "estado"]
        missing_fields = [
            field for field in required_fields 
            if field not in place_data or not str(place_data[field]).strip()
        ]

        if missing_fields:
            return False, f"Faltan los siguientes campos obligatorios: {', '.join(missing_fields)}"
        return True, ""

    def get_places(self) -> Tuple[Dict, int]:
        """Obtener todos los lugares"""
        if self.db is None:
            logger.error("Error de conexión a la base de datos en get_places")
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            places = list(self.places_collection.find({}))

            if not places:
                return {"message": "No hay lugares registrados"}, 404

            # Convertir ObjectId a string
            for place in places:
                place["_id"] = str(place["_id"])

            return {"places": places}, 200

        except Exception as e:
            logger.error(f"Error al obtener lugares: {str(e)}")
            return {"error": "Error al obtener los lugares"}, 500

    from app.database import dbConnect
from bson.json_util import dumps, ObjectId
from flask import jsonify
import logging
from typing import Dict, Tuple, Any

logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class PlacesService:
    def __init__(self):
        self.db = dbConnect()
        if self.db is not None:
            self.places_collection = self.db["destinos"]
        else:
            self.places_collection = None
            logger.error("No se pudo establecer conexión con la base de datos")

    def validate_place_data(self, place_data: Dict) -> Tuple[bool, str]:
        """Validar los datos del lugar"""
        required_fields = ["nombre", "cordenadas", "direccion", "estado"]
        missing_fields = [
            field for field in required_fields 
            if field not in place_data or not str(place_data[field]).strip()
        ]

        if missing_fields:
            return False, f"Faltan los siguientes campos obligatorios: {', '.join(missing_fields)}"
        return True, ""

    def get_places(self) -> Tuple[Dict, int]:
        """Obtener todos los lugares"""
        if self.db is None:
            logger.error("Error de conexión a la base de datos en get_places")
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            places = list(self.places_collection.find({}))

            if not places:
                return {"message": "No hay lugares registrados"}, 404

            # Convertir ObjectId a string
            for place in places:
                place["_id"] = str(place["_id"])

            return {"places": places}, 200

        except Exception as e:
            logger.error(f"Error al obtener lugares: {str(e)}")
            return {"error": "Error al obtener los lugares"}, 500

    def get_place(self, place_id: str) -> Tuple[Dict, int]:
        """Obtener un lugar por ID"""
        if self.db is None:
            logger.error("Error de conexión a la base de datos en get_place")
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            if not ObjectId.is_valid(place_id):
                return {"error": "ID de lugar inválido"}, 400

            place = self.places_collection.find_one({"_id": ObjectId(place_id)})
            if not place:
                return {"message": "Lugar no encontrado"}, 404

            # Convertir ObjectId a str
            place["_id"] = str(place["_id"])
            return {"place": place}, 200

        except Exception as e:
            logger.error(f"Error al obtener lugar {place_id}: {str(e)}")
            return {"error": "Error interno del servidor"}, 500

    def add_place(self, place_data: Dict) -> Tuple[Dict, int]:
        """Agregar un nuevo lugar"""
        if self.places_collection is None:
            logger.error("Error de conexión a la base de datos en add_place")
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            # Validar datos
            is_valid, error_message = self.validate_place_data(place_data)
            if not is_valid:
                return {"error": error_message}, 400

            # Verificar si el lugar ya existe
            existing_place = self.places_collection.find_one({
                "nombre": place_data["nombre"]
            })
            if existing_place:
                return {"error": "Ya existe un lugar con ese nombre"}, 400

            # Insertar nuevo lugar
            result = self.places_collection.insert_one(place_data)
            
            # Convertir ObjectId a str
            place_data["_id"] = str(result.inserted_id)
            
            return {
                "message": "Lugar agregado exitosamente",
                "id": str(result.inserted_id),
                "place": place_data
            }, 201

        except Exception as e:
            logger.error(f"Error al agregar lugar: {str(e)}")
            return {"error": f"Error al agregar lugar: {str(e)}"}, 500

    def update_place(self, place_id: str, place_data: Dict) -> Tuple[Dict, int]:
        """Actualizar un lugar existente"""
        if self.places_collection is None:
            logger.error("Error de conexión a la base de datos en update_place")
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            # Validar el ID
            if not ObjectId.is_valid(place_id):
                return {"error": "ID de lugar inválido"}, 400

            # Validar datos
            is_valid, error_message = self.validate_place_data(place_data)
            if not is_valid:
                return {"error": error_message}, 400

            # Verificar si existe el lugar
            existing_place = self.places_collection.find_one({"_id": ObjectId(place_id)})
            if not existing_place:
                return {"error": "Lugar no encontrado"}, 404

            # Verificar si el nuevo nombre ya existe (si se está cambiando el nombre)
            if (place_data["nombre"] != existing_place["nombre"] and
                self.places_collection.find_one({"nombre": place_data["nombre"]})):
                return {"error": "Ya existe un lugar con ese nombre"}, 400

            # Actualizar el lugar
            result = self.places_collection.update_one(
                {"_id": ObjectId(place_id)},
                {"$set": place_data}
            )

            if result.modified_count > 0:
                updated_place = self.places_collection.find_one({"_id": ObjectId(place_id)})
                # Convertir ObjectId a str
                updated_place["_id"] = str(updated_place["_id"])
                return {
                    "message": "Lugar actualizado exitosamente",
                    "place": updated_place
                }, 200
            else:
                return {"message": "No se realizaron cambios"}, 200

        except Exception as e:
            logger.error(f"Error al actualizar lugar: {str(e)}")
            return {"error": f"Error al actualizar lugar: {str(e)}"}, 500

    def delete_place(self, place_id: str) -> Tuple[Dict, int]:
        """Eliminar un lugar"""
        if self.places_collection is None:
            logger.error("Error de conexión a la base de datos en delete_place")
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            # Validar el ID
            if not ObjectId.is_valid(place_id):
                return {"error": "ID de lugar inválido"}, 400

            # Verificar si existe el lugar
            place = self.places_collection.find_one({"_id": ObjectId(place_id)})
            if not place:
                return {"error": "Lugar no encontrado"}, 404

            # Eliminar el lugar
            result = self.places_collection.delete_one({"_id": ObjectId(place_id)})
            
            if result.deleted_count > 0:
                # Convertir ObjectId a str
                place["_id"] = str(place["_id"])
                return {
                    "message": "Lugar eliminado exitosamente",
                    "deleted_place": place
                }, 200
            else:
                return {"error": "No se pudo eliminar el lugar"}, 500

        except Exception as e:
            logger.error(f"Error al eliminar lugar: {str(e)}")
            return {"error": f"Error al eliminar lugar: {str(e)}"}, 500