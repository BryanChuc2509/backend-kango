from database import dbConnect
from bson.json_util import dumps, ObjectId
from flask import jsonify
import re

# vehiculo = [
#     modelo, 
#     placa, 
#     numAsientos,
#     estado,
#     viajes_completados,
#     calidad,
#     costoK,
#     kilometraje_media
# ]

class VehiclesService: 
    def __init__(self):
        self.db = dbConnect()
        if self.db is not None:
            self.vehicles_collection = self.db["vehiculos"]
        else:
            self.drivers_collection = None

    def get_vehicles(self):
        try :
            if self.db is None:  
                raise Exception ("Ocurrió un problema al momento de realizar la solicitud")

            vehicles = list(self.vehicles_collection.find({}))
            
            if not vehicles:
                return {"message": "No hay vehiculos"}, 404
            
            # Convert ObjectId to string 
            for vehicle in vehicles:
                vehicle["_id"] = str(vehicle["_id"])
            
            return vehicles, 200
        except Exception as e:
            return {"message" : str(e)}, 500

    def get_vehicle(self, vehicle_id):
        try:
            if self.db is None: 
                raise Exception ("Ocurrió un problema al momento de realizar la solicitud")  
            try:
                vehicle_id = ObjectId(vehicle_id)
            except Exception as e:
                return {"message": "ID de vehículo inválido"}, 400

            vehicle = self.vehicles_collection.find_one({"_id": ObjectId(vehicle_id)})
            if not vehicle:
                return {"message": "vehiculo no encontrado"}, 404
            
            vehicle["_id"] = str(vehicle["_id"])
            
            return vehicle, 200
        except Exception as e:
            return {"message": str(e)}, 500
    
    def add_vehicle(self, vehicle_data):
        try:
            if self.vehicles_collection is None:
                raise Exception("Ocurrió un problema al momento de realizar la solicitud")
            
            # Check if any required fields are missing or empty
            required_fields = ["modelo", "marca", "placa", "numAsientos", "calidad"]
            
            missing_fields = [field for field in required_fields if field not in vehicle_data or not str(vehicle_data[field]).strip()]
        
            if missing_fields:
                return {"message": f"Faltan los siguientes campos obligatorios: {', '.join(missing_fields)}"}, 400
            
            modelo = vehicle_data.get('modelo')
            placa = vehicle_data.get('placa')
            marca = vehicle_data.get('marca')
            numAsientos = vehicle_data.get('numAsientos')
            calidad = vehicle_data.get('calidad')

            # Validate the number of seats
            try:
                min_seats = 0;
                max_seats = 40
                format_num_seats = int(numAsientos)
                if format_num_seats <= min_seats:
                    return {"message": "El número de asientos debe ser un número entero positivo"}, 400
                if numAsientos > max_seats:
                    return {"message": f"El número de asientos no puede ser mayor a {max_seats}"}, 400
                
            except ValueError:
                return {"message" : "El número de asientos debe ser un número"}, 400
            
            # Validate the vehicle's plate format
            if not re.match(r"^[A-Z0-9]{3}-[A-Z0-9]{3}-[A-Z0-9]{1}$", placa):
                return {"message": "El formato de la placa es inválido, prueba con un formato: AAA-BBB-X"}, 400
            
            # Validate if the vehicle license plate already exists in the database
            vehicle = self.vehicles_collection.find_one({"placa": placa })
            if vehicle:
                return {"message" : "La placa ya está registrada, pruebe con otra"}, 409

            # Validate if the quality is right
            enum_calidad = ["Estándar", "Premiun"]
            if calidad not in enum_calidad:
                return {"message": f"La calidad debe ser: {' o '.join(enum_calidad)}"}, 400
            
            # Insert the new vehicle into the collection
            result = self.vehicles_collection.insert_one({
                    "modelo": modelo,
                    "placa": placa,
                    "numAsientos": format_num_seats, 
                    "estado": "Disponible",
                    "viajes_completados": 0,
                    "calidad": calidad,
                    "costoKm": 0,
                    "kilometraje_media": "",
                    "marca": marca
            })
            
            if result.inserted_id:
                return {"message": "Vehículo agregado", "id": str(result.inserted_id)}, 201, {'Access-Control-Allow-Origin':'*'}
            
            raise Exception("Ocurrió un error al agregar el vehículo")

        except Exception as e:
            return {"message": str(e)}, 500


    def update_vehicle(self, vehicle_id, vehicle_data):
        try:
            if self.vehicles_collection is None:
                raise Exception("Ocurrió un problema al momento de realizar la solicitud")
            
            # Validate ObjectId
            if not ObjectId.is_valid(vehicle_id):
                return {"message": "El ID del vehículo no es válido"}, 400
            
            # Check de the vehicle in the database 
            vehicle = self.vehicles_collection.find_one({"_id": ObjectId(vehicle_id)})
            if not vehicle:
                return {"message": "El vehículo no fue encontrado"}, 404
            
            # Fields allowed
            allowed_fields = [
                "modelo", 
                "placa", 
                "numAsientos",
                "estado",
                "calidad",
                "marca", 
            ]
            
            update_data = {key: vehicle_data[key] for key in allowed_fields if key in vehicle_data and vehicle_data[key]}
            if not update_data:
                return {"message": "No se proporcionaron datos válidos para actualizar"}, 400
            
            # Validate fields 
            
            if "placa" in update_data.keys():
                if not re.match(r"^[A-Z0-9]{3}-[A-Z0-9]{3}-[A-Z0-9]{1}$", update_data["placa"]):
                    return {"message": "El formato de la placa es inválido, prueba con un formato: AAA-BBB-X"}, 400
                
                # Check if the plate exists
                existing_vehicle = self.vehicles_collection.find_one({
                    "placa": update_data["placa"], 
                    "_id": {"$ne": ObjectId(vehicle_id)}
                })
                if existing_vehicle:
                    return {"message": "La placa ya está registrada en otro vehículo"}, 409
            
            # Validate the seats number 
            if "numAsientos" in update_data.keys():
                try:
                    format_num_seats = int(update_data["numAsientos"])
                    min_seats = 1
                    max_seats = 40
                    if format_num_seats < min_seats:
                        return {"message": "El número de asientos debe ser un número entero positivo"}, 400
                    if format_num_seats > max_seats:
                        return {"message": f"El número de asientos no puede ser mayor a {max_seats}"}, 400
                    update_data["numAsientos"] = format_num_seats
                except ValueError:
                    return {"message": "El número de asientos debe ser un número"}, 400
            
            # Validate if the quaility is right
            if "calidad" in update_data.keys():
                enum_calidad = ["Estándar", "Premiun"]
                if update_data["calidad"] not in enum_calidad:
                    return {"message": f"La calidad debe ser: {' o '.join(enum_calidad)}"}, 400
                
            # Validate if the status is right
            if "estado" in update_data.keys():
                enum_calidad = ["Disponible", "Ocupado", "Deshabilitado"]
                if update_data["estado"] not in enum_calidad:
                    return {"message": f"La calidad debe ser: {' o '.join(enum_calidad)}"}, 400
                
            result = self.vehicles_collection.update_one(
                {"_id": ObjectId(vehicle_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return {"message": "Vehículo actualizado exitosamente"}, 200
            
            return {"message": "No se realizaron cambios en el vehículo"}, 200
        
        except Exception as e:
            return {"message": str(e)}, 500



    def delete_vehicle(self, vehicle_id):
        if self.vehicles_collection is None:
            return {"message": "Ocurrió un problema al momento de realizar la solicitud"}, 500

        try:
            if not ObjectId.is_valid(vehicle_id):
                return {"message": "El ID del vehículo no es válido"}, 400
            
            result = self.drivers_collection.delete_one({
                "_id": ObjectId(vehicle_id)
            })
            
            if result.deleted_count == 0:
                return {"message": "Vehículo no encontrado"}, 404
            return {"message": "Vehículo eliminado"}, 200
        except Exception as e:
            return {"message": f"Error al eliminar el vehículo: {str(e)}"}, 500
