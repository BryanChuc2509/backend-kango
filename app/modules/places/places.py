from flask import Flask, request, jsonify
from flask_restx import Namespace, Resource, fields
from app.modules.places.places_service import PlacesService

# Inicializar API de lugares
places_service = PlacesService()
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
    @api.doc("listar_lugares")
    def get(self):
        """Obtener todos los lugares"""
        return places_service.get_places()

    @api.doc("agregar_lugar")
    @api.expect(places_model)
    def post(self):
        """Agregar un nuevo lugar"""
        place_data = request.get_json()
        return places_service.add_place(place_data)

@api.route("/<string:place_id>")
@api.param("place_id", "El ID del lugar")
class Place(Resource):
    @api.doc("eliminar_lugar")
    def delete(self, place_id):
        """Eliminar un lugar por ID"""
        return places_service.delete_place(place_id)

@api.route("/update/<string:place_id>")
@api.param("place_id", "El ID del lugar")
class UpdatePlace(Resource):
    @api.doc("actualizar_lugar")
    @api.expect(places_model)
    def put(self, place_id):
        """Actualizar un lugar por ID"""
        place_data = request.get_json()
        return places_service.update_place(place_id, place_data)