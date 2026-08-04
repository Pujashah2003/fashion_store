from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "transaction_id",
        "order",
        "amount",
        "payment_method",
        "payment_status",
    )

    search_fields = (
        "transaction_id",
        "order__order_number",
    )