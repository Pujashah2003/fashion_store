from django.shortcuts import render
from products.models import Product

def home(request):
    products = Product.objects.filter(is_available=True)

    return render(request, 'home/home.html', {
        'products': products
    })