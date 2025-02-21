from flask import Flask, request, jsonify
from flask_restx import Namespace, Resource, fields

# Simulación de una base de datos
class PlacesAPI:
    def __init__(self):
        self.places = []
        self.counter = 1
    
    def get_places(self):
        return jsonify(self.places)
    
    def add_place(self, place_data):
        place_data["id"] = self.counter
        self.places.append(place_data)
        self.counter += 1
        return jsonify({"message": "Lugar agregado", "place": place_data})
    
    def delete_place(self, place_id):
        for place in self.places:
            if place["id"] == place_id:
                self.places.remove(place)
                return jsonify({"message": "Lugar eliminado"})
        return jsonify({"error": "Lugar no encontrado"}), 404

# Inicializar API de lugares
places_api = PlacesAPI()
api = Namespace("places", description="Operaciones con lugares")

# Definir modelo para validación
places_model = api.model("Place", {
    "nombre": fields.String(required=True, description="Nombre del lugar"),
    "cordenadas": fields.String(required=True, description="Coordenadas del lugar"),
    "direccion": fields.String(required=True, description="Dirección del lugar"),
    "estado": fields.String(required=True, description="Estado del lugar"),
})

@api.route("/")
class PlaceList(Resource):
    @api.doc("editar_lugar")
    def get(self):
        """Editar los lugares"""
        return places_api.get_places()

    @api.doc("agregar_lugar")
    @api.expect(places_model)
    def post(self):
        """Agregar un nuevo lugar"""
        place_data = request.get_json()
        return places_api.add_place(place_data)

@api.route("/<int:place_coords>")
@api.param("place_coords", "Las coordenadas del lugar")
class Place(Resource):
    @api.doc("eliminar_lugar")
    def delete(self, place_id):
        """Eliminar un lugar por coordenadas"""
        return places_api.delete_place(place_coords)

@api.route("/<int:place_id>")
@api.param("place_id", "El ID del lugar")
class Place(Resource):
    @api.doc("obtener_lugar")
    def get(self, place_id):
        """Obtener un lugar por ID"""
        return places_api.get_place(place_id)
