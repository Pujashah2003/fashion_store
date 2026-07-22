from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from products.models import Product
from .models import Cart, CartItem



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        cart_items = cart.items.all()
    else:
        cart_items = []

    total = sum(item.subtotal for item in cart_items)

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total": total,
    })