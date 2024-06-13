from django.shortcuts import render, redirect
from .models import Post, Comment
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import SignUpForm, PostCreate
from django.contrib import messages

# Create your views here.
def home(request):
    all_post = Post.objects.all()
    return render(request, 'home.html', {'all_post': all_post})

def post(request, pk):
    post = Post.objects.filter(id=pk)
    comments = Comment.objects.filter(post=pk)
    return render(request, 'post.html', {'post': post, 'comments': comments})

def my_post(request):
    if request.user.is_authenticated:
        my_post = Post.objects.filter(user=request.user)
        return render(request, 'my_post.html', {'my_post': my_post})
    else:
        messages.success(request, 'You must log in to access that web page')
        return redirect("home")


def create_post(request):
    if request.user.is_authenticated:
        form = PostCreate(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, "Your post has been created")
                return redirect('my_post')
        else:
            return render(request, 'create_post.html', {'form': form})
    else:
        messages.error(request, 'You must log in to access that web page')
        return redirect('home')


def update_post(request, pk):
    pass


def delete_post(request):
    pass


def search(request):
    pass

#
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in')
            return redirect('home')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Incorrect password, please try again')
                return redirect('login')
            else:
                messages.error(request, 'Incorrect user, please try again')
                return redirect('login')
    else:
        return render(request, 'login.html')

#
def logout_user(request):
    logout(request)
    return redirect('home')

# 
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'User created successfully')
            return redirect('home')
        else:
            messages.error(request, 'Whoops!! There was a problem registerin, please try again..')
            return redirect("register")
    else:
        return render(request, 'register.html', {'form': form})