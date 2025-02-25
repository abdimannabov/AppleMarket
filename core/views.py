from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from core.forms import SignUpForm, AddNewProduct
from core.models import *

# Create your views here.
def index(request):
    items = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'core/index.html',{
        'categories':categories,
        'items':items
    })

def detail(request, pk):
    item = get_object_or_404(Product, pk=pk)
    related_item = Product.objects.filter(category=item.category).exclude(pk=pk)[0:3]
    return render(request, 'core/components/detail.html',{
        'item':item,
        'related':related_item
    })

def contact(request):
    return render(request, 'core/components/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignUpForm()

    return render(request, 'core/components/signup.html', {
        'form':form
    })

@login_required
def new(request):
    form = AddNewProduct()

    return render(request, 'core/components/form.html', {
        'form':form
    })