from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import Login

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('contact/', views.contact, name="contact"),
    path('signup/', views.signup, name="signup"),
    path('new/', views.new, name="new"),
    path('login/', auth_views.LoginView.as_view(template_name = 'core/components/login.html', authentication_form=Login), name="login"),
    path("cart/", views.cart, name="cart"),
    path("to_cart/<int:product_id>/<str:action>/", views.to_cart, name="to_cart")
]
