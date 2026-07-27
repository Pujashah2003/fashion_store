from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect("cart:cart")

    cart_items = cart.items.all()
    total_amount = sum(item.subtotal for item in cart_items)
    
    # Calculate shipping fee (Free for orders over Rs. 3000, else Rs. 150)
    shipping_fee = 0 if total_amount >= 3000 else 150
    grand_total = total_amount + shipping_fee

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address_line1 = request.POST.get("address_line1")
        address_line2 = request.POST.get("address_line2", "")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        payment_method = request.POST.get("payment_method", "COD")

        if not all([full_name, email, phone, address_line1, city, state, postal_code]):
            messages.error(request, "Please fill in all required shipping fields.")
            return render(request, "orders/checkout.html", {
                "cart_items": cart_items,
                "total_amount": total_amount,
                "shipping_fee": shipping_fee,
                "grand_total": grand_total,
            })

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            total_amount=total_amount,
            shipping_fee=shipping_fee,
            grand_total=grand_total,
            payment_method=payment_method,
            payment_status="Pending",
            status="Pending",
        )

        # Create Order Items and update stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                subtotal=item.subtotal,
            )
            # Reduce product stock
            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
                item.product.save()

        # Clear cart
        cart.items.all().delete()

        messages.success(request, f"Order #{order.order_number} placed successfully!")
        return redirect("orders:order_success", order_number=order.order_number)

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total_amount": total_amount,
        "shipping_fee": shipping_fee,
        "grand_total": grand_total,
    })


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, "orders/order_success.html", {
        "order": order
    })


@login_required
def order_list(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_list.html", {
        "orders": user_orders
    })


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/order_detail.html", {
        "order": order
    })
