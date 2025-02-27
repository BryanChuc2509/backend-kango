from database import dbConnect
import uuid

class Pago:
    def __init__(self, id, id_reserva, id_transaccion, monto, estado):
        self.id = str(uuid.uuid4())  # ID unico del pago
        self.id = id  # ID del pasajero que realiza el pago
        self.id_reserva = id_reserva  # ID de la reserva asociada
        self.id_transaccion = id_transaccion  # ID de la transaccion de PayPal
        self.monto = monto  # Monto del pago
        self.estado = estado  # Estado del pago

    def to_dict(self):
        """Convierte el objeto en un diccionario para guardar en MongoDB"""
        return {
            "id": self.id,
            "id": self.id,
            "id_reserva": self.id_reserva,
            "id_transaccion": self.id_transaccion,
            "monto": self.monto,
            "estado": self.estado
        }

    @staticmethod
    def save(pago):
        """Guarda el pago en la base de datos MongoDB"""
        db = dbConnect()  # Conectar con la BD
        return db.pagos.insert_one(pago.to_dict())
