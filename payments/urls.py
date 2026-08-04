from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [

    path(
        "esewa/<int:order_id>/",
        views.esewa_payment,
        name="esewa_payment"
    ),


    path(
        "success/",
        views.payment_success,
        name="payment_success"
    ),


    path(
        "failure/",
        views.payment_failure,
        name="payment_failure"
    ),

]