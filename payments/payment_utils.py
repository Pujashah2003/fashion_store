import hmac
import hashlib
import base64


MERCHANT_ID = "EPAYTEST"

SECRET_KEY = "8gBm/:&EnhH.1/q"

SUCCESS_URL = "http://127.0.0.1:8000/payments/success/"
FAILURE_URL = "http://127.0.0.1:8000/payments/failure/"

PAYMENT_URL = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"


def generate_signature(message):
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()

    return base64.b64encode(signature).decode("utf-8")