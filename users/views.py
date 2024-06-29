from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import ChangePasswordForm, SignUpForm, ProfileUpdateForm, ImageForm

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
    return render(request, 'update/update_profile.html', {'image_form': image_form, 'profile_form': profile_form})

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

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')

# Faltan validaciones
# Username may only contain alphanumeric characters or single hyphens, and cannot begin or end with a hyphen.
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

# Faltan validaciones en el form
@login_required
def update_password(request):
    current_user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(current_user, request.POST)
        # ¿El formulario es valido?
        if form.is_valid():
            form.save()
            messages.success(request, "")
            login(request, current_user)
            return redirect("update_user")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                return redirect("update_password")
    else:
        form = ChangePasswordForm(current_user)
        return render(request, "update_password.html", {"form": form})