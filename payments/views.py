import uuid


from django.shortcuts import (
    render,
    get_object_or_404
)


from orders.models import Order


from .esewa import (
    MERCHANT_ID,
    PAYMENT_URL,
    SUCCESS_URL,
    FAILURE_URL,
    generate_signature,
)


def esewa_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    amount = f"{order.grand_total:.2f}"

    transaction_uuid = (
        f"{order.order_number}-"
        f"{uuid.uuid4().hex[:8]}"
    )


    message = (
        f"total_amount={amount},"
        f"transaction_uuid={transaction_uuid},"
        f"product_code={MERCHANT_ID}"
    )


    signature = generate_signature(message)


    print("======== eSEWA DEBUG ========")
    print("Amount:", amount)
    print("Transaction UUID:", transaction_uuid)
    print("Message:", message)
    print("Signature:", signature)
    print("=============================")


    context = {
        "payment_url": PAYMENT_URL,
        "amount": amount,
        "total_amount": amount,
        "tax_amount": "0",
        "transaction_uuid": transaction_uuid,
        "product_code": MERCHANT_ID,
        "signature": signature,
        "success_url": SUCCESS_URL,
        "failure_url": FAILURE_URL,
        "order": order,
    }


    return render(
        request,
        "payments/esewa_payment.html",
        context
    )



def payment_success(request):

    return render(
        request,
        "payments/success.html"
    )



def payment_failure(request):

    return render(
        request,
        "payments/failure.html"
    )