from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .forms import ProductForm
from .forms import CategoryForm

from products.models import Product
from categories.models import Category
from orders.models import Order

from django.db.models import Q


# ==========================
# Dashboard
# ==========================
def dashboard(request):
    latest_orders = Order.objects.order_by("-id")[:5]
    latest_products = Product.objects.order_by("-id")[:5]

    context = {
        "product_count": Product.objects.count(),
        "category_count": Category.objects.count(),
        "order_count": Order.objects.count(),
        "user_count": User.objects.count(),

        "latest_orders": latest_orders,
        "latest_products": latest_products,
    }

    return render(request, "admin_dashboard/dashboard.html", context)


# ==========================
# Product List
# ==========================
def product_list(request):
    products = Product.objects.all().order_by("-id")

    context = {
        "products": products
    }

    return render(
        request,
        "admin_dashboard/products/product_list.html",
        context
    )


# ==========================
# Add Product
# ==========================
def add_product(request):

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect("admin_dashboard:product_list")

    else:
        form = ProductForm()

    return render(
        request,
        "admin_dashboard/products/product_form.html",
        {
            "form": form,
            "title": "Add Product"
        }
    )


# ==========================
# Edit Product
# ==========================
def edit_product(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            return redirect("admin_dashboard:product_list")

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "admin_dashboard/products/product_form.html",
        {
            "form": form,
            "title": "Edit Product"
        }
    )


# ==========================
# Delete Product
# ==========================
def delete_product(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("admin_dashboard:product_list")

    return render(
        request,
        "admin_dashboard/products/delete_product.html",
        {
            "product": product
        }
    )
# ==========================
# Category List
# ==========================
def category_list(request):

    categories = Category.objects.all().order_by("-id")

    return render(
        request,
        "admin_dashboard/categories/category_list.html",
        {
            "categories": categories
        }
    )


# ==========================
# Add Category
# ==========================
def add_category(request):

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("admin_dashboard:category_list")

    else:
        form = CategoryForm()

    return render(
        request,
        "admin_dashboard/categories/category_form.html",
        {
            "form": form,
            "title": "Add Category"
        }
    )


# ==========================
# Edit Category
# ==========================
def edit_category(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():
            form.save()
            return redirect("admin_dashboard:category_list")

    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "admin_dashboard/categories/category_form.html",
        {
            "form": form,
            "title": "Edit Category"
        }
    )


# ==========================
# Delete Category
# ==========================
def delete_category(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect("admin_dashboard:category_list")

    return render(
        request,
        "admin_dashboard/categories/delete_category.html",
        {
            "category": category
        }
    )
# ==========================
# Order List
# ==========================
def order_list(request):
    search = request.GET.get("search")

    orders = Order.objects.all().order_by("-created_at")

    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(full_name__icontains=search) |
            Q(email__icontains=search) |
            Q(user__username__icontains=search)
        )

    return render(
        request,
        "admin_dashboard/orders/order_list.html",
        {
            "orders": orders,
            "search": search,
        }
    )


# ==========================
# Order Detail
# ==========================
def order_detail(request, pk):

    order = get_object_or_404(Order, pk=pk)

    return render(
        request,
        "admin_dashboard/orders/order_detail.html",
        {
            "order": order
        }
    )


# ==========================
# Update Order Status
# ==========================
def update_order_status(request, pk):

    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":

        order.status = request.POST.get("status")
        order.save()

    return redirect("admin_dashboard:order_detail", pk=order.pk)

# ==========================
# Customer List
# ==========================

def customer_list(request):

    search = request.GET.get("search")

    customers = User.objects.all().order_by("-id")

    if search:
        customers = customers.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    return render(
        request,
        "admin_dashboard/customers/customer_list.html",
        {
            "customers": customers,
            "search": search,
        }
    )


# ==========================
# Customer Detail
# ==========================

def customer_detail(request, pk):

    customer = get_object_or_404(User, pk=pk)

    orders = Order.objects.filter(user=customer).order_by("-created_at")

    return render(
        request,
        "admin_dashboard/customers/customer_detail.html",
        {
            "customer": customer,
            "orders": orders,
        }
    )
# ==========================
# Payment List
# ==========================

def payment_list(request):

    search = request.GET.get("search")

    payments = Order.objects.all().order_by("-created_at")

    if search:
        payments = payments.filter(
            Q(order_number__icontains=search) |
            Q(full_name__icontains=search)
        )

    return render(
        request,
        "admin_dashboard/payments/payment_list.html",
        {
            "payments": payments,
            "search": search,
        }
    )
# ==========================
# Payment Detail
# ==========================

def payment_detail(request, pk):

    payment = get_object_or_404(Order, pk=pk)

    return render(
        request,
        "admin_dashboard/payments/payment_detail.html",
        {
            "payment": payment
        }
    )