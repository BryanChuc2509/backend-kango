from flask import request
from modules.payments.paypal_models import Pago


class PaymentsController:

    @staticmethod
    def process_payment():
        """Procesa un pago después de que PayPal lo aprueba."""
        data = request.get_json()  # Obtener los datos de la solicitud JSON
        print(" Datos recibidos en el backend:", data)  
        id= data.get("id")  # ID del pasajero que hizo el pago
        id_reserva = data.get("id_reserva")  # ID de la reserva
        id_transaccion = data.get("id_transaccion")  # ID del PayPasl
        monto = data.get("monto")  # Monto pagado
        estado = data.get("estado")  # Estado del pago )

        if not id or not id_reserva or not id_transaccion or not monto or not estado:
            return {"error": "Faltan datos para procesar el pago"}, 400

        # Crear el objeto Pago y guardarlo en monguito
        pago = Pago(id, id_reserva, id_transaccion, monto, estado)
        Pago.save(pago)

        return {"mensaje": "Pago registrado correctamente"}, 201
