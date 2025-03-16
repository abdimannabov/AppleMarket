from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Customer, ShippingAddress

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl border"

class Login(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Enter password",
        'class': "w-full py-4 px-6 rounded-xl"
    }))

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        username = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Enter username',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))
        email = forms.CharField(widget=forms.EmailInput(attrs={
            'placeholder': "Enter email",
            'class': "w-full py-4 px-6 rounded-xl"
        }))
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': "Enter password",
            'class': "w-full py-4 px-6 rounded-xl"
        }))
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': "Repeat the password",
            'class': "w-full py-4 px-6 rounded-xl"
        }))

class AddNewProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price', 'image')

        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class EditProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']
        widgets = {
            "name":forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':"Your name"
            }),
            "email": forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': "Your email"
            })
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['city', 'street', 'address']
        widgets = {
            "city":forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':"Your city"
            }),
            "street": forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Your street"
            }),
            "address": forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Your address"
            })
        }