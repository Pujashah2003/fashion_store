from django.db import models
from orders.models import Order


class Payment(models.Model):

    PAYMENT_METHODS = (
        ("eSewa", "eSewa"),
        ("COD", "Cash On Delivery"),
    )

    PAYMENT_STATUS = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="eSewa"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.transaction_id