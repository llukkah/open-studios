from django.urls import path, re_path
from . import views

urlpatterns = [
    # Display paths
    path('', views.main, name = 'home'),
    path('about', views.about, name = "about"),
    path('upcoming', views.upcoming, name = "upcoming"),
    path('featured', views.featured, name = "featured"),
    path('image/<str:name>/', views.show_image, name = 'image'),
    
    # Create exhibit
    path('create', views.create_exhibit, name = 'create'),
    
    # Edit exhibit
    path('upcoming/edit/<int:exhibit_id>', views.edit_exhibit, name = 'edit'),
    
    # Tag actions on edit page
    re_path(r'^tag/create/', views.create_tag, name = 'addTag'),
    re_path(r'^tag/<int:tag_id>/', views.edit_tag, name = 'editTag'),
    
    # Image actions
    re_path(r'^image/create/', views.create_image, name = 'addImage'),
    re_path(r'^image/<int:image_id>/', views.edit_image, name = 'editImage'),
    
    # User actions on post MVP
    path('register', views.register, name = "register"),
    path('login', views.login, name = "login"),
]
