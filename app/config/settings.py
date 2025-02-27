import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_super_segura")

    PAYPAL_CLIENT_ID = "AdzbAOTlXBFbbcw-NPdudBvV5u6EYKOj20gG56nOWSutvLfaQJhaBZITh6q3IAx5jrEw53lKRDRwmJYM"
    PAYPAL_CLIENT_SECRET = "EGZCbS4axrRpPaJFqjJ0afpDTCzH0OI8AlVlyYLCHPRY2z8dUIBHLllOOfpkl9Wj9lCUqo7o6Uu37wyV"
    PAYPAL_MODE = "sandbox"  # Cambia a 'live' en producción


