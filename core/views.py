from django.shortcuts import render
from django.views.generic import ListView
from core.models import *


# Create your views here.
def index(request):
    items = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'core/index.html',{
        'categories':categories,
        'items':items
    })

def contact(request):
    return render(request, 'core/components/contact.html')