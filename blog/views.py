from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import SignUpForm, PostForm, CommentForm
from django.contrib import messages

# Create your views here.
def home(request):
    all_post = Post.objects.all()
    return render(request, 'home.html', {'all_post': all_post})

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'post.html', {'post': post, 'comments': comments, 'form': form})

def my_post(request):
    if request.user.is_authenticated:
        my_posts = Post.objects.filter(author=request.user)
        return render(request, 'my_post.html', {'my_posts': my_posts})
    else:
        messages.success(request, 'You must log in to access that web page')
        return redirect("home")

# Faltan validaciones
def create_post(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request, 'Your post has been created')
                return redirect('my_post')
        else:
            return render(request, 'CRUD/create_post.html', {'form': form})
    else:
        messages.error(request, 'You must log in to access that web page')
        return redirect('home')


def edit_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id, author=request.user)
        if request.method == 'POST':
            form = PostForm(request.POST or None, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, "Your post has been update succesfuly")
                return redirect('post', post_id=post.id)
        else:
            form = PostForm(instance=post)
            return render(request, 'CRUD/edit_post.html', {'form': form})
    else:
        messages.error(request, 'You must log in to access that web page')
        return redirect('home')


def delete_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id, author=request.user)
        if request.method == 'POST':
            post.delete()
            messages.error(request, 'You have delete post')
            return redirect('my_post')
        else:
            messages.error(request, 'You must log in to access that web page')
            return render(request, 'CRUD/delete_post.html', {'post': post})
    else:
        messages.error(request, 'You must log in to access that web page')
        return redirect('home')


def comment_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post', post_id)
    else:
        messages.error(request, 'You must log in to access that web page')
        
    return redirect('post', post_id)

def search(request):
    pass

# Faltan validaciones
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

# Faltan validaciones
def logout_user(request):
    logout(request)
    return redirect('home')

# Faltan validaciones
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