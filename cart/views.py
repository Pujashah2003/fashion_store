from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not product.is_available or product.stock <= 0:
        messages.error(request, f"Sorry, '{product.name}' is currently out of stock.")
        return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        new_qty = cart_item.quantity + quantity
        if new_qty > product.stock:
            messages.warning(request, f"Cannot add more. Only {product.stock} items available in stock.")
            cart_item.quantity = product.stock
        else:
            cart_item.quantity = new_qty
            messages.success(request, f"Updated quantity of '{product.name}' in your cart.")
        cart_item.save()
    else:
        if quantity > product.stock:
            quantity = product.stock
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"Added '{product.name}' to your cart.")

    return redirect("cart:cart")


@login_required
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action') or request.GET.get('action')

    if action == 'increment':
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Increased quantity of {cart_item.product.name}.")
        else:
            messages.warning(request, f"Maximum available stock for {cart_item.product.name} reached.")
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f"Decreased quantity of {cart_item.product.name}.")
        else:
            cart_item.delete()
            messages.info(request, f"Removed {cart_item.product.name} from cart.")

    return redirect("cart:cart")


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f"Removed '{product_name}' from your cart.")
    return redirect("cart:cart")


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.select_related('product').all() if cart else []
    
    total = sum(item.subtotal for item in cart_items)
    shipping_fee = 0 if total >= 3000 or total == 0 else 150
    grand_total = total + shipping_fee

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total": total,
        "shipping_fee": shipping_fee,
        "grand_total": grand_total,
    })