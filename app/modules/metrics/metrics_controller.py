from flask import jsonify, request
from flask_restx import Namespace, Resource, fields

from .metrics_service import MetricService

metric_service = MetricService()
api = Namespace("metrics", description="Operaciones con las métricas")

# Modelo de datos para la documentación de Swagger

metric_model = api.model("Metric", {
    "viajes_diarios": fields.Integer(required=True, description="Viajes diarios realizados"),
    "viajes_semanales": fields.Integer(required=True, description="Viajes semanales realizados"),
    "ingresos_mensuales": fields.Integer(required=True, description="Ingresos recibidos al mes"),
    "distancia_viaje": fields.Integer(required=True, description="Distancia realizada por viaje"),
    "duracion_viaje": fields.Integer(required=True, description="Duración realizada por viaje"),
    "created_at" : fields.DateTime(required=True, description="Fecha de creación del registro"),
})


@api.route("/")
class metricList(Resource):
    @api.doc("listar_metricas")
    def get(self):
        """Obtener todos los metricas"""
        return metric_service.get_metrics()

    @api.doc("agregar_metrica")
    @api.expect(metric_model)  # Valida el body de la petición
    def post(self):
        """Agregar una nueva metrica"""
        metric_data = request.get_json()
        return metric_service.add_metric(metric_data)

@api.route("/<string:metric_id>")
@api.param("metric_id", "El ID del metrica")
class metric(Resource):
    @api.doc("obtener_metrica")
    def get(self, metric_id):
        """Obtener una metrica por ID"""
        return metric_service.get_metric(metric_id)

    @api.doc("actualizar_metrica")
    @api.expect(metric_model)
    def put(self, metric_id):
        """Actualizar una metrica por ID"""
        metric_data = request.get_json()
        return metric_service.update_metric(metric_id, metric_data)

    @api.doc("eliminar_metrica")
    def delete(self, metric_id):
        """Eliminar una metrica por ID"""
        return metric_service.delete_metric(metric_id)