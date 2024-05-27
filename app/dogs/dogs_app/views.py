from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse
from .models import TodoItem
from django.contrib.auth import authenticate, login
from .forms import PostForm
from .models import Post
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
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_success')
    else:
        form = PostForm()
    return render(request, 'entries.html', {'form': form})

'''def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})'''

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