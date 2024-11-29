# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.

def home(request):
    images = getAllImages()  # Obtén todas las imágenes
    favourite_list = []  # Puedes implementar favoritos si lo necesitas
    if request.user.is_authenticated:
        # Obtén los favoritos del usuario autenticado
        favourite_list = getAllFavouritesByUser(request)
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

def search(request):
    search_msg = request.POST.get('query', '').strip()  # Limpia el texto ingresado

    if not search_msg:
        # Si no se ingresa texto, muestra todas las imágenes
        return redirect('home')

    # Filtra las imágenes basándote en el texto ingresado
    images = getAllImages(input=search_msg)
    favourite_list = []  # Implementa favoritos si es necesario

    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

import requests

def getAllImages(input=None):
    url = f"https://rickandmortyapi.com/api/character/?name={input}" if input else "https://rickandmortyapi.com/api/character"
    response = requests.get(url)
    if response.status_code != 200:
        return []  # Manejo de error
    data = response.json()
    print(data)  # Verifica qué datos estás obteniendo desde la API
    characters = data.get('results', [])
    cards = []
    for character in characters:
        cards.append({
            'name': character['name'],
            'image': character['image'],
            'status': character['status'],
            'location': character['location']['name'],
            'episode': character['episode'][0].split("/")[-1]
        })
    return cards

# Estas funciones se usan cuando el usuario está logueado en la aplicación.

# Manejo de inicio de sesión
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'index.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'index.html')

# Cerrar sesión
@login_required
def exit(request):
    logout(request)
    return redirect('index')

# Manejo de registro de usuarios
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el nuevo usuario 
            login(request, user)  # inicia sesión automanicamente
            print(f"Usuario {user.username} registrado y autenticado.")  # Verificación
            return redirect('index') #Vuelve al inicio
        else:
            print(form.errors)  # Ver los errores de validación
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# Obtener favoritos del usuario
@login_required
def getAllFavouritesByUser(request):
    favourites = list(request.user.favourites.values())  # Lista de favoritos
    return render(request, 'favourites.html', {'favourites': favourites})


# Guardar favorito
from .models import Favourite 
from django.contrib import messages
@login_required
def saveFavourite(request):
    if request.method == 'POST':
        # Obtén los datos enviados por el formulario
        name = request.POST.get('name')
        image= request.POST.get('image')
        status = request.POST.get('status')
        last_location = request.POST.get('last_location')
        first_seen = request.POST.get('first_seen')

        # Crea o guarda el favorito en la base de datos
        Favourite.objects.create(
            user=request.user,  # El usuario actual
            name=name,
            image=image,
            status=status,
            last_location=last_location,
            first_seen=first_seen,
        )
        messages.success(request, "¡El personaje ha sido añadido a favoritos!")
        return redirect('home')  # Redirige a la página actual (o donde prefieras)

    return redirect('home')  # Si no es POST, redirige a home

# Eliminar favorito
@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        fav_id = request.POST.get('id')
        if fav_id:
            request.user.favourites.filter(id=fav_id).delete()
    return redirect('home')


