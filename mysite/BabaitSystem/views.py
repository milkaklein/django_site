
from django.http import HttpResponse, HttpResponseRedirect
from selenium.common.exceptions import NoSuchElementException

from .models import Products,Suppliers,ProductBySupplier
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from .add_to_db import *
import urllib
import time
import string

from django.contrib.auth.decorators import login_required





def search(request):
    if (request.GET.get('mybtn')):
        makat = request.GET.get('makat')
        if(makat):
            results = find_all(makat)
            context = {'results': results}
            return render(request, 'BabaitSystem/result_info.html', context)



    return render(request, 'BabaitSystem/search.html')

def login(request):


    return render(request, 'registration/login.html')
#
# def find(request, product_id):
#     product = get_object_or_404(Products, pk=product_id)
#     return render(request, 'BabaitSystem/result_info.html', {
#         'product': product,
#         'error_message': "You didn't select a choice.",})



def find(request, product_id):

    ProductBySupplier_list = ProductBySupplier.objects.order_by('price')
    context = {
        'ProductBySupplier_list': ProductBySupplier_list,
    }
    return render(request, 'BabaitSystem/result_info.html', context)


def result_info(request):
    ProductBySupplier_list = ProductBySupplier.objects.order_by('price')
    context = {
        'ProductBySupplier_list': ProductBySupplier_list,
    }
    return render(request, 'BabaitSystem/result_info.html', context)


