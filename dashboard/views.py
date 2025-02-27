from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.forms import EditProduct
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

@login_required
def edit(request, pk):
    item = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = EditProduct(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()

            return redirect('dashboard:index')
    else:
        form = EditProduct(instance=item)

    return render(request, 'core/components/form.html', {
        'form':form,
        'title':"Edit Item"
    })