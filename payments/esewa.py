import hmac
import hashlib
import base64


MERCHANT_ID = "EPAYTEST"

SECRET_KEY = "8gBm/:&EnhH.1/q"


PAYMENT_URL = (
    "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
)


SUCCESS_URL = (
    "http://127.0.0.1:8000/"
    "payments/success/"
)


FAILURE_URL = (
    "http://127.0.0.1:8000/"
    "payments/failure/"
)



def generate_signature(message):

    digest = hmac.new(
        SECRET_KEY.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()


    return base64.b64encode(
        digest
    ).decode("utf-8")