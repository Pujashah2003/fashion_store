from .models import Cart, CartItem

def cart_context(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_item_count = sum(item.quantity for item in cart.items.all())
    return {
        'cart_item_count': cart_item_count,
    }
