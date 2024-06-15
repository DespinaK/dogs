import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse
from psycopg2 import IntegrityError
from .models import TodoItem
from django.contrib.auth import authenticate, login
from .forms import PostForm
from .models import Post
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

# Create your views here.


def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def entries(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print("lolara")
        if form.is_valid():
            print("hey ypu")
            post = form.save(commit=False)
            
            lat = request.POST.get('lat')
            lon = request.POST.get('lon')
            #lat='40.7128'
            #lon='74.0060'
            print(f"Received POST data - lat: {lat}, lon: {lon}")
            if lat is not None and lon is not None:
                try:
                    lat = float(lat)
                    lon = float(lon)
                    
                    # Debugging the converted values
                    print(f"Converted lat: {lat}, lon: {lon}")
                    
                    # Create Point with SRID and log the Point
                    #location, created = Location.objects.get_or_create(
                     #   latitude=lat,
                      #  longitude=lon,
                       # defaults={
                        #    'location': Point(lon, lat, srid=4326),
                         #   'id': uuid.uuid4()
                        #}
                   # )
                    #post.location = location
                    #post.location = Point(lon, lat, srid=4326)
                    #post.longitude = lon
                    #post.latitude = lat
                    #print(f"Created Point jhkjhkjhkjh: {post.latitude}")
                    post.save()
                    print("eleos re paidi mou")
                    return redirect('post_success')
                except IntegrityError as e:
                    return HttpResponseBadRequest(f"Database error: {e}")
                except ValueError:
                    print("lol")
                    print("lat:", lat , "lon:",lon)
                    return HttpResponseBadRequest("Invalid 'lat' or 'lon' parameter")
            else:
                return HttpResponseBadRequest("Missing 'lat' or 'lon' parameter")
    else:
        form = PostForm()
    return render(request, 'entries.html', {'form': form})

 
def posts(request):
    lat = request.POST.get('lat', '40.7128')
    lon = request.POST.get('lon', '74.0060')
    print("got it")
    #lat='40.7128'
    #lon='74.0060'
    
    if lat is None or lon is None:
        print("aloha")
        return HttpResponseBadRequest("Missing 'lat' or 'lon' parameter")
    
    try:
        point = Point(float(lat), float(lon),srid=4326)
    except ValueError:
        
        return HttpResponseBadRequest("Invalid 'lat' or 'lon' parameter")
    
    #point = Point(lon, lat, srid=4326)
    
    
    radius = request.GET.get('radius', 10)  # Default radius is 10 km
    try:
        radius = float(radius)
    except ValueError:
        return HttpResponseBadRequest("Invalid 'radius' parameter")
    
    posts = Post.objects.all()
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # If it's an AJAX request, return JSON data
        posts_data = [{"title": post.title, "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S')} for post in posts]
        return JsonResponse(posts_data, safe=False)
    
    return render(request, 'posts.html', {'posts': posts, 'radius': radius})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to custom login view after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout(request):
    return render(request, "logout.html")


def post_success(request):
    return render(request, 'post_success.html')

def view_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts})

