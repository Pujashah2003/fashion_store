from django.urls import path
from . import views

app_name = "admin_dashboard"

urlpatterns = [
    #Dashboard
    path("", views.dashboard, name="dashboard"),

    # Products
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/<int:pk>/edit/", views.edit_product, name="edit_product"),
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),

    # Categories
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/edit/<int:pk>/", views.edit_category, name="edit_category"),
    path("categories/delete/<int:pk>/", views.delete_category, name="delete_category"),

    #  Orders    
    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path(
        "orders/<int:pk>/status/",
        views.update_order_status,
        name="update_order_status",
    ),
    # Customers 

    path(
    "customers/",
    views.customer_list,
    name="customer_list",
   ),

    path(
    "customers/<int:pk>/",
    views.customer_detail,
    name="customer_detail",
    ),
    # ---------------- Payments ----------------

path(
    "payments/",
    views.payment_list,
    name="payment_list",
    ),

path(
    "payments/<int:pk>/",
    views.payment_detail,
    name="payment_detail",
    ),
]