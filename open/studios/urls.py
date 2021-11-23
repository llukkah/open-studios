from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name = 'home'),
    path('studios', views.main, name = 'home'),
    path('create', views.create_exhibit, name = 'create_exhibit'),
    path('featured', views.featured, name = "featured"),
    path('about', views.about, name = "about"),
    path('upcoming', views.upcoming, name = "upcoming"),
    path('register', views.register, name = "register"),
    path('login', views.login, name = "login"),
]
