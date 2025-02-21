from flask import jsonify, request
from flask_restx import Namespace, Resource, fields

from .routes_service import RouteService

route_service = RouteService()
api = Namespace("routes", description="Operaciones con las métricas")

# Modelo de datos para la documentación de Swagger
"coords_salida", "coords_destino", "fecha_inicio", "fecha_llegada", "duracion_estimada", "distancia", "asientos_ocupados"
route_model = api.model("Route", {
    "coords_salida": fields.Integer(required=True, description="Coordenadas del lugar de salida"),
    "coords_destino": fields.Integer(required=True, description="Coordenadas del lugar de llegada"),
    "fecha_inicio": fields.Date(required=True, description="Fecha de cuando sale el vehiculo"),
    "fecha_llegada": fields.Date(required=True, description="Fecha de cuando se estima llegue el vehiculo"),
    "duracion_estimada": fields.DateTime(required=True, description="Duración esimada del viaje"),
    "distancia" : fields.Integer(required=True, description="Distancia total del viaje"),
    "asientos_ocupados" : fields.String(required=True, description="Lista de asientos ocupados"),
})


@api.route("/")
class routeList(Resource):
    @api.doc("listar_routeas")
    def get(self):
        """Obtener todos los routeas"""
        return route_service.get_routes()

    @api.doc("agregar_routea")
    @api.expect(route_model)  # Valida el body de la petición
    def post(self):
        """Agregar una nueva routea"""
        route_data = request.get_json()
        return route_service.add_route(route_data)

@api.route("/<string:route_id>")
@api.param("route_id", "El ID del routea")
class route(Resource):
    @api.doc("obtener_routea")
    def get(self, route_id):
        """Obtener una routea por ID"""
        return route_service.get_route(route_id)

    @api.doc("actualizar_routea")
    @api.expect(route_model)
    def put(self, route_id):
        """Actualizar una routea por ID"""
        route_data = request.get_json()
        return route_service.update_route(route_id, route_data)

    @api.doc("eliminar_routea")
    def delete(self, route_id):
        """Eliminar una routea por ID"""
        return route_service.delete_route(route_id)