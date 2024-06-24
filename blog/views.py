from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from .models import Profile, Post
from .forms import SignUpForm, ProfileUpdateForm, ImageForm, PostForm, CommentForm

# Create your views here.
def home(request):
    all_post = Post.objects.all()
    return render(request, 'home.html', {'all_post': all_post})

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'post.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def my_post(request):
    my_posts = Post.objects.filter(author=request.user)
    return render(request, 'my_post.html', {'my_posts': my_posts})

# Faltan validaciones
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created')
            return redirect('my_post')
    else:
        form = PostForm()
        
    return render(request, 'CRUD/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Your post has been update succesfuly")
            return redirect('post', post_id=post.id)
        else:
            messages.error(request, "error")
            return redirect('post', post_id=post.id)
    else:
        form = PostForm(instance=post)
        return render(request, 'CRUD/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.error(request, 'You have delete post')
        return redirect('my_post')
    else:
        messages.error(request, 'You must log in to access that web page')
        return render(request, 'delete_post.html', {'post': post})

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post', post_id)

@login_required
def profile(request):
    current_user = User.objects.get(id=request.user.id)
    image_user = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'user': current_user, 'image': image_user})


# Faltan validaciones
@login_required
def update_profile(request):
    profile = request.user.profile
    image_form = ImageForm(request.POST or None, request.FILES or None, instance=profile)
    profile_form = ProfileUpdateForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        if image_form.is_valid():
            image_form.save()
            messages.success(request, 'Your profile picture has been updated.')
            return redirect('update_profile')
    return render(request, 'CRUD/update_profile.html', {'image_form': image_form, 'profile_form': profile_form})


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
@login_required
def logout_user(request):
    logout(request)
    return redirect('home')

# Faltan validaciones
# Al momento de que se cree un usuario se creare el perfil con una imagen default
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
    

def search(request):
    if request.method == 'POST':
        search = request.POST['searched']
        searched = Post.objects.filter(Q(title__icontains=search) | Q(subtitle__icontains=search) | Q(body__icontains=search))
        # Si no hay resultados
        if not searched:
            messages.error(request, 'The searched publication was not found.')
        else:
            return render(request, 'search.html', {'searched': searched}) 