from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class ProfileUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

# Aca falta el Password update!!!!

class ImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        required = {
            'image': False,
        }

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('category', 'subcategory', 'title', 'subtitle', 'cover', 'body')
		widgets = {
			'category': forms.Select(attrs={'class':'form-control', 'placeholder':'Select Category'}),
			'subcategory': forms.Select(attrs={'class':'form-control', 'placeholder':'Select Category'}),
			'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
			'subtitle': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Subtitle'}),
			'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
			'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Body'})
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)
		widgets = {
			'text': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write comment'})
		}