import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from core.forms import SignUpForm, AddNewProduct, CustomerForm, AddressForm
from core.models import *
from django.db.models import Q
from core.utils import get_cart_data, CartForUser
from django.contrib import messages

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
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    if query:
        items = items.filter(Q(name__contains=query) | Q(description__icontains=query))

    if category_id:
        items = items.filter(category_id = category_id)

    return render(request, 'core/components/search.html', {
        'items': items,
        'query':query,
        'categories':categories,
        'category_id':int(category_id)
    })

def cart(request):
    cart_info = get_cart_data(request)

    context = {
        "products":cart_info["products"],
        "order":cart_info["order"],
        "total_quantity":cart_info["cart_total_quantity"],
        "total_price":cart_info["cart_total_price"],
        "customer_form": CustomerForm(),
        "address_form": AddressForm(),
        "title":"Cart"
    }
    return render(request, "core/cart.html", context)

def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForUser(request, product_id, action)
        return redirect("/cart/")
    else:
        messages.error(request, "You are not authenticated")
        return redirect("/login/")

def payment(request):
    from market import settings
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForUser(request)
        cart_info = user_cart.get_cart_info()
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.name = customer_form.cleaned_data['name']
            customer.email = customer_form.cleaned_data['email']
        address_form = AddressForm(data=request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()
        total_price = cart_info["cart_total_price"]
        total_quantity = cart_info["cart_total_quantity"]
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data":{
                        "currency":"usd",
                        "product_data":{
                            'name':"products of TOTEMBO"
                        },
                        "unit_amount":int(total_price)
                    },
                    "quantity":total_quantity
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("core:success")),
            cancel_url=request.build_absolute_uri(reverse("core:cancel"))
        )
    return redirect(session.url, 303)

def success_payment(request):
    return render(request, "core/success.html")

def cancel_payment(request):
    return render(request, "core/cancel.html")