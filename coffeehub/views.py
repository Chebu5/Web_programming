from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from coffeehub.models import Product
# Create your views here.
class ShowProductView(View):
    def get(request,*args,**kwargs):
        products = Product.objects.all()
        results = ""
        for s in products:
            results += s.name + "<br>"
        return HttpResponse(results)