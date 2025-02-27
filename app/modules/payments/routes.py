from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource
from modules.payments.paypal_controller import PaymentsController
from modules.payments.paypal_service import create_payment
from modules.payments.paypal_docs import (
    create_payment_model,
    create_payment_response_model,
    process_payment_model,
    payment_response_model
)

payments_bp = Blueprint("payments", __name__)
api = Namespace("payments", description="APIs para gestionar pagos con PayPal")

# Registrar modelos en la documentación
api.models[create_payment_model.name] = create_payment_model
api.models[create_payment_response_model.name] = create_payment_response_model
api.models[process_payment_model.name] = process_payment_model
api.models[payment_response_model.name] = payment_response_model

@api.route("/create-payment")
class CreatePayment(Resource):
    @api.expect(create_payment_model)
    @api.response(200, "Éxito", create_payment_response_model)
    def post(self):
        """Crea un pago en PayPal y devuelve la URL de aprobación."""
        data = request.json
        payment= create_payment(data)
        return payment

@api.route("/process-payment")
class ProcessPayment(Resource):
    @api.expect(process_payment_model)
    @api.response(201, "Pago registrado correctamente", payment_response_model)
    def post(self):
        """Procesar un pago y guardarlo en MongoDB."""
        return PaymentsController.process_payment()

