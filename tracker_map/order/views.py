from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import os


def index(request):
    orders = Order.objects.all()
    order_list = []
    for order in orders:
        for item in order.product.all():
            order_list.append([order,item])

    context = {
        'order_list' : order_list
    }
    return render(request,'index.html', context)

def map (request):
    if request.method == 'GET':
        buyer_id = request.GET.get('buyer')
        vendor_id = request.GET.get('vendor')
        product_id = request.GET.get('product')
        current_buyer = Address.objects.get(user_id=buyer_id)
        current_vendor = Address.objects.get(user_id=vendor_id)
        current_product = User.objects.get(pk=product_id)
        context = {
            'buyer' : current_buyer,
            'vendor' : current_vendor,
            'product' : current_product,
            'api_key' : os.environ.get('TOMTOM_KEY')
        }
        return render(request, 'map.html', context)
    else:
        return render(request, 'map.html')

def runner_map(request):
    orders = Order.objects.all()
    order_list = []
    for order in orders:
        for item in order.product.all():
            buyer_address = Address.objects.get(user_id = order.buyer_id)
            vendor_address = Address.objects.get(user_id = item.vendor_id)
            order_list.append([order,item,buyer_address,vendor_address])
    context = {
        'order_list' : order_list,
        'api_key' : os.environ.get('TOMTOM_KEY')

    }
    return render(request, 'runner_map.html', context)