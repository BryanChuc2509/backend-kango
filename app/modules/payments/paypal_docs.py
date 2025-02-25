from flask_restx import Model, fields

# Modelo para la solicitud de creación de pago
create_payment_model = Model("CreatePayment", {
    "amount": fields.String(required=True, description="Monto del pago en USD")
})

# Modelo para la respuesta de creacion de pago
create_payment_response_model = Model("CreatePaymentResponse", {
    "id": fields.String(description="ID del pago en PayPal"),
    "status": fields.String(description="Estado del pago"),
    "approval_url": fields.String(description="URL para que el usuario apruebe el pago")
})

# Modelo para la solicitud de procesamiento de pago
process_payment_model = Model("ProcessPayment", {
    "id_transaccion": fields.String(description="ID de la transacción generada por PayPal"),
    "id_reserva": fields.String(required=True, description="ID de la reserva asociada al pago"),
    "id": fields.String(required=True, description="ID del pasajero que realiza el pago"),
    "monto": fields.String(required=True, description="Monto del pago"),
    "estado": fields.String(required=True, description="Estado del pago (Approved, Failed, etc.)")
})

payment_response_model = Model("PaymentResponse", {
    "id_transaccion": fields.String(description="ID de la transacción generada por PayPal"),
    "id_reserva": fields.String(description="ID de la reserva asociada"),
    "id": fields.String(description="ID del pasajero"),
    "monto": fields.String(description="Monto del pago"),
    "estado": fields.String(description="Estado del pago"),
    "message": fields.String(description="Mensaje de confirmación del pago")
})
