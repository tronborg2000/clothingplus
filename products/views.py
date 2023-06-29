from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Product
from .forms import ProductForm

def product_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    sort_by = request.GET.get('sort_by')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(location__icontains=query) |
            Q(features__icontains=query)
        )

    if category:
        products = products.filter(category=category)

    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'popularity':
        products = products.order_by('-votes_total')

    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_create.html', {'form': form})


def upvote_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.upvote()
    data = {'votes_total': product.votes_total}
    return JsonResponse(data)

