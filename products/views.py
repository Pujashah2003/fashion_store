from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from categories.models import Category
from .models import Product


def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Category filter
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Search filter
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


def product_detail_by_slug(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })