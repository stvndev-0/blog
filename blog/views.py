from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .models import Category, SubCategory, Post
from .forms import PostForm, CommentForm

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

# Carga de subcategorias
def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)


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


def search(request):
    if request.method == 'POST':
        search = request.POST['searched']
        searched = Post.objects.filter(Q(title__icontains=search) | Q(subtitle__icontains=search) | Q(body__icontains=search))
        # Si no hay resultados
        if not searched:
            messages.error(request, 'The searched publication was not found.')
        else:
            return render(request, 'search.html', {'searched': searched}) 


def seccion(request, name):
    category = get_object_or_404(Category, name=name)
    subCategories = category.subcategories.all()
    return render(request, 'seccion.html', {'subCategories': subCategories})


def category(request, categoryName):
    subCategory = SubCategory.objects.get(name=categoryName)
    post_category = subCategory.posts.all()
    return render(request, 'category.html', {'post_category': post_category})