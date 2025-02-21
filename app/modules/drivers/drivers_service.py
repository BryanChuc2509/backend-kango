from database import dbConnect
from bson.json_util import dumps, ObjectId
from flask import jsonify
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

class DriverService: 
    def __init__(self):
        self.db = dbConnect()
        if self.db is not None:
            self.drivers_collection = self.db["conductores"]
        else:
            self.drivers_collection = None

    def get_drivers(self):
        if self.db is None:  
            return {"error": "No se pudo conectar a la base de datos"}, 500

        drivers = list(self.drivers_collection.find({}))
        
        if not drivers:
            return {"message": "No hay conductores"}, 404
        
        # Convert ObjectId to string 
        for driver in drivers:
            driver["_id"] = str(driver["_id"])
        
        return drivers, 200

    def get_driver(self, driver_id):

        if self.db is None: 
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            driver = self.drivers_collection.find_one({"_id": ObjectId(driver_id)})
            if not driver:
                return {"message": "Conductor no encontrado"}, 404

            driver["_id"] = str(driver["_id"])

            return driver, 200
        except Exception as e:
            logging.error(f"Error al buscar conductor {driver_id}: {str(e)}")
            return {"error": "Error interno del servidor"}, 500
    
    def add_driver(self, driver_data):
        if self.drivers_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500 

        try:
            required_fields = ["nombre", "apellido", "licencia_valida", "numero_telefonico"]
            missing_fields = [field for field in required_fields if field not in driver_data or not str(driver_data[field]).strip()]
        
            if missing_fields:
                return {"error": f"Faltan los siguientes campos obligatorios: {', '.join(missing_fields)}"}, 400

            driver = self.drivers_collection.find_one({
                "apellido": driver_data["apellido"]
            })
            if driver:
                return {"error": "El conductor ya existe"}, 400

            result = self.drivers_collection.insert_one(driver_data)

            return {"message": "Conductor agregado", "id": str(result.inserted_id)}, 201

        except Exception as e:
            return {"error": f"Error al agregar conductor: {str(e)}"}, 500


    def update_driver(self, driver_id, driver_data):
        if self.drivers_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.drivers_collection.update_one(
                {"_id": ObjectId(driver_id)},
                {"$set": driver_data}
            )
            if result.matched_count == 0:
                return {"message": "Conductor no encontrado"}, 404
            return {"message": "Conductor actualizado"}, 200
        except Exception as e:
            return {"error": f"Error al actualizar conductor: {str(e)}"}, 500

    def delete_driver(self, driver_id):
        """Elimina un conductor por ID."""
        if self.drivers_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.drivers_collection.delete_one({"_id": ObjectId(driver_id)})
            if result.deleted_count == 0:
                return {"message": "Conductor no encontrado"}, 404
            return {"message": "Conductor eliminado"}, 200
        except Exception as e:
            return {"error": f"Error al eliminar conductor: {str(e)}"}, 500
