from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('create.exhibit', views.create_exhibit, name = 'create_exhibit'),
]
