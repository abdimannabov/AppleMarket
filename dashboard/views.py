from django.shortcuts import render, get_object_or_404, redirect
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

@login_required
def delete(request, pk):
    item = get_object_or_404(Product, pk=pk)
    item.delete()

    return redirect('dashboard:index')