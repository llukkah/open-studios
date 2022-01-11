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
    
    # Edit exhibit
    path('upcoming/edit/<int:exhibit_id>', views.edit_exhibit, name = 'edit'),
    
    # Image actions
    path('create/image/', views.create_image, name = 'createImage'),
    path('/image/<int:image_id>/', views.create_edit_image, name = 'creatEImage'),
    path('image/', views.upcoming_create_image, name = 'addImage'),
    
    # User actions on post MVP
    path('register', views.register, name = "register"),
    path('login', views.login_user, name = "login"),    
    path('logout', views.logout_user, name = "logout"),
]
