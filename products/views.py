from django.shortcuts import render
from django.http import JsonResponse

def upvote_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.upvote()
    data = {'votes_total': product.votes_total}
    return JsonResponse(data)


# Create your views here.
