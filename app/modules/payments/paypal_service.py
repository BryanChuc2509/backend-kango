import paypalrestsdk
from config.settings import Config

# Configurar PayPal SDK
paypalrestsdk.configure({
    "mode": Config.PAYPAL_MODE,
    "client_id": Config.PAYPAL_CLIENT_ID,
    "client_secret": Config.PAYPAL_CLIENT_SECRET
})

def create_payment(amount, currency="USD"):
    """
    Crea una orden de pago en PayPal.
    """
    try:
        print("Valor de amount recibido:", amount)  

        # Extraer valor si viene en un diccionario
        if isinstance(amount, dict) and "amount" in amount:
            amount = amount["amount"]

        formatted_amount = f"{float(amount):.2f}"

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": formatted_amount, "currency": currency},
                "description": "Pago por servicio de KanGo"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:5173/success",
                "cancel_url": "http://localhost:5173/cancel"
            }
        })

        if payment.create():
            return {
                "id_transaccion": payment.id,  # 
                "paymentID": payment.id,
                "approval_url": payment["links"][1]["href"]
            }
        else:
            return {"error": payment.error}
    
    except Exception as e:
        return {"error": str(e)}
