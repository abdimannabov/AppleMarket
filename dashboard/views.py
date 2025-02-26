from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.models import Product
# Create your views here.

@login_required
def index(request):
    items = Product.objects.all()

    return render(request, 'dashboard/index.html', {
        'items':items,
        'title':"Dashboard"
    })