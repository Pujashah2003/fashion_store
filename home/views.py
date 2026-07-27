from django.shortcuts import render
from products.models import Product
from categories.models import Category

def home(request):
    featured_products = Product.objects.filter(is_available=True)[:8]
    categories = Category.objects.all()

    return render(request, 'home/home.html', {
        'products': featured_products,
        'categories': categories,
    })