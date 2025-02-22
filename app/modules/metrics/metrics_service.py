from database import dbConnect
from bson.json_util import dumps, ObjectId
from flask import jsonify
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

class MetricService: 
    def __init__(self):
        self.db = dbConnect()
        if self.db is not None:
            self.metrics_collection = self.db["metricas"]
        else:
            self.metrics_collection = None

    def get_metrics(self):  #se obtienen las métricas de la BD
        if self.db is None:  
            return {"error": "No se pudo conectar a la base de datos"}, 500

        metrics = list(self.metrics_collection.find({}))
        
        if not metrics:
            return {"message": "No hay métricas"}, 404
        
        # Convert ObjectId to string 
        for metric in metrics:
            metric["_id"] = str(metric["_id"])
        
        return metrics, 200

    def get_metric(self, metric_id): #se obtiene una sola métrica de la BD

        if self.db is None: 
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            metric = self.metrics_collection.find_one({"_id": ObjectId(metric_id)})
            if not metric:
                return {"message": "Métrica no encontrado"}, 404

            metric["_id"] = str(metric["_id"])

            return metric, 200
        except Exception as e:
            logging.error(f"Error al buscar métrica {metric_id}: {str(e)}")
            return {"error": "Error interno del servidor"}, 500
    
    def add_metric(self, metric_data): #se añaden las métricas en la BD
        if self.metrics_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500 

        try: #se verifican los datos requeridos obligatoriamente
            required_fields = ["viajes_diarios", "viajes_semanales", "ingresos_mensuales", "distancia_viaje", "duracion_viaje", "created_at"]
            missing_fields = [field for field in required_fields if field not in metric_data or not str(metric_data[field]).strip()]
        
            if missing_fields:
                return {"error": f"Faltan los siguientes campos obligatorios: {', '.join(missing_fields)}"}, 400

                #Verifica si ya existe una métrica con la misma fecha de creación
            metric = self.metrics_collection.find_one({
                "created_at": metric_data["created_at"]
            })
            if metric:
                return {"error": "Las métricas ya existen"}, 400

            result = self.metrics_collection.insert_one(metric_data)
            return {"message": "Métrica agregada", "id": str(result.inserted_id)}, 201

        except Exception as e:
            return {"error": f"Error al agregar las métricas: {str(e)}"}, 500


    def update_metric(self, metric_id, metric_data): #se actualizan las métricas en la BD
        if self.metrics_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.metrics_collection.update_one(
                {"_id": ObjectId(metric_id)},
                {"$set": metric_data}
            )
            if result.matched_count == 0:
                return {"message": "Métrica no encontrada"}, 404
            return {"message": "Métrica actualizada"}, 200
        except Exception as e:
            return {"error": f"Error al actualizar métricas: {str(e)}"}, 500

    def delete_metric(self, metric_id): #se eliminan las métricas en la BD
        """Elimina una métrica por ID."""
        if self.metrics_collection is None:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        try:
            result = self.metrics_collection.delete_one({"_id": ObjectId(metric_id)})
            if result.deleted_count == 0:
                return {"message": "Métrica no encontrada"}, 404
            return {"message": "Métrica eliminada"}, 200
        except Exception as e:
            return {"error": f"Error al eliminar métrica: {str(e)}"}, 500
