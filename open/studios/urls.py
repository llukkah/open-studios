from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name = 'home'),
    # path('studios', views.main, name = 'home'),
    path('about', views.about, name = "about"),
    
    path('create', views.create_exhibit, name = 'create'),
    path('create/tag/', views.create_tag, name = 'tag'),
    path('create/tag/<int:tag_id>', views.edit_tag, name = 'edit_tag'),
    path('create/image/', views.create_image, name = 'create_image'),
    path('create/image/<int:image_id>', views.edit_image, name = 'edit_image'),
    
    path('featured', views.featured, name = "featured"),
    path('image/<str:name>/', views.show_image, name = 'image'),
    path('upcoming', views.upcoming, name = "upcoming"),
    
    path('upcoming/edit/<int:exhibit_id>', views.edit_exhibit, name = 'edit'),
    path('upcoming/edit/<int:exhibit_id>/tag/', views.create_tag, name = 'create_tag'),
    path('upcoming/edit/<int:exhibit_id>/tag/<int:tag_id>', views.edit_tag, name = 'edit_tag'),
    path('upcoming/edit/<int:exhibit_id>/image/', views.create_image, name = 'create_image'),
    path('upcoming/edit/<int:exhibit_id>/image/<int:image_id>', views.edit_image, name = 'edit_image'),
    
    path('register', views.register, name = "register"),
    path('login', views.login, name = "login"),
]
