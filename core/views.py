from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from core.forms import SignUpForm, AddNewProduct, EditProduct
from core.models import *
from django.db.models import Q
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
    if request.method == "POST":
        form = AddNewProduct(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('core:index')
    else:
        form = AddNewProduct()


    return render(request, 'core/components/form.html', {
        'form':form,
        'title':"New Item"
    })

def search(request):
    query = request.GET.get('query', '')
    items = Product.objects.all()

    if query:
        items = items.filter(Q(name__contains=query) | Q(description__icontains=query))

    return render(request, 'core/components/search.html', {
        'items': items,
        'query':query
    })