from django.urls import path
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
    
    # Tag actions on create page
    path('create/tag/', views.create_tag, name = 'addTag'),
    path('create/tag/<int:tag_id>', views.edit_tag, name = 'editTag'),
    
    # Image actions on create page
    path('create/image/', views.create_image, name = 'addImage'),
    path('create/image/<int:image_id>', views.edit_image, name = 'editImage'),
    
    # Edit exhibit
    path('upcoming/edit/<int:exhibit_id>', views.edit_exhibit, name = 'edit'),
    
    # Tag actions on edit page
    path('upcoming/edit/<int:exhibit_id>/tag/', views.create_tag, name = 'addTag'),
    path('upcoming/edit/<int:exhibit_id>/tag/<int:tag_id>', views.edit_tag, name = 'editTag'),
    
    # Image actions on edit page
    path('upcoming/edit/<int:exhibit_id>/image/', views.create_image, name = 'addImage'),
    path('upcoming/edit/<int:exhibit_id>/image/<int:image_id>', views.edit_image, name = 'editImage'),
    
    # User actions on post MVP
    path('register', views.register, name = "register"),
    path('login', views.login, name = "login"),
]
