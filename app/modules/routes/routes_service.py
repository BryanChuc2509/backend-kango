from app.database import dbConnect
from bson.json_util import dumps, ObjectId
from flask import jsonify
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

class RouteService: 
    def __init__(self):
        self.db = dbConnect()
        if self.db is not None:
            self.routes_collection = self.db["rutas"]
        else:
            self.routes_collection = None

    def get_routes(self):  #se obtienen las rutas de la BD
        if self.db is None:  
            return {"error": "No se pudo conectar a la base de datos"}, 500

        routes = list(self.routes_collection.find({}))
        
        if not routes:
            return {"message": "No hay rutas"}, 404
        
        # Convert ObjectId to string 
        for route in routes:
            route["_id"] = str(route["_id"])
        
        return routes, 200

    def get_route(self, route_id): #se obtiene una sola ruta de la BD

        if self.db is None: 
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            route = self.routes_collection.find_one({"_id": ObjectId(route_id)})
            if not route:
                return {"message": "ruta no encontrado"}, 404

            route["_id"] = str(route["_id"])

            return route, 200
        except Exception as e:
            logging.error(f"Error al buscar ruta {route_id}: {str(e)}")
            return {"error": "Error interno del servidor"}, 500
    
    def add_route(self, route_data): #se añaden las rutas en la BD
        if self.routes_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500 

        try: #se verifican los datos requeridos obligatoriamente
            required_fields = ["coords_salida", "coords_destino", "fecha_inicio", "fecha_llegada", "duracion_estimada", "distancia", "asientos_ocupados"]
            missing_fields = [field for field in required_fields if field not in route_data or not str(route_data[field]).strip()]
        
            if missing_fields:
                return {"error": f"Faltan los siguientes campos obligatorios: {', '.join(missing_fields)}"}, 400

                #Verifica si ya existe una ruta con la misma fecha de creación
            route = self.routes_collection.find_one({
                "fecha_inicio": route_data["fecha_inicio"]
            })
            if route:
                return {"error": "La ruta ya existe"}, 400

            result = self.routes_collection.insert_one(route_data)
            return {"message": "ruta agregada", "id": str(result.inserted_id)}, 201

        except Exception as e:
            return {"error": f"Error al agregar la ruta: {str(e)}"}, 500


    def update_route(self, route_id, route_data): #se actualizan las rutas en la BD
        if self.routes_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.routes_collection.update_one(
                {"_id": ObjectId(route_id)},
                {"$set": route_data}
            )
            if result.matched_count == 0:
                return {"message": "ruta no encontrada"}, 404
            return {"message": "ruta actualizada"}, 200
        except Exception as e:
            return {"error": f"Error al actualizar rutas: {str(e)}"}, 500

    def delete_route(self, route_id): #se eliminan las rutas en la BD
        """Elimina una ruta por ID."""
        if self.routes_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.routes_collection.delete_one({"_id": ObjectId(route_id)})
            if result.deleted_count == 0:
                return {"message": "ruta no encontrada"}, 404
            return {"message": "ruta eliminada"}, 200
        except Exception as e:
            return {"error": f"Error al eliminar ruta: {str(e)}"}, 500
