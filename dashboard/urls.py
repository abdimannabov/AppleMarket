from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit')
]