from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('login/', views.login_user, name='login'),
    path('home/<int:page>/', views.home, name='home_page'),  # Esta ruta maneja las páginas
    path('register/', views.register_user, name='register'),
    path('favoritos/', views.getAllFavouritesByUser, name='favoritos'),
    path('save_favourite/', views.saveFavourite, name='save_favourite'),
    path('delete_favourite/', views.deleteFavourite, name='delete_favourite'),
    path('exit/', views.exit, name='exit'),
]
