from django import forms
from .models import SubCategory, Post, Comment
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('category', 'subcategory', 'title', 'subtitle', 'cover', 'content')
		widgets = {
			'category': forms.Select(attrs={'class':'form-control'}),
			'subcategory': forms.Select(attrs={'class':'form-control'}),
			'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
			'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
			'subtitle': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Subtitle'})
		}
            
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		# Comprobamos si hay un campo llamado 'category' en los datos enviados con el formulario
		if 'category' in self.data:
			# Manejamos los posibles errores al convertir el valor del campo 'category' a un entero
			try:
				category_id = int(self.data.get('category'))
				self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
			except (ValueError, TypeError):
				self.fields['subcategory'].queryset = SubCategory.objects.none()
		elif self.instance.pk:
			self.fields['subcategory'].queryset = self.instance.category.contents.order_by('name')
		else:
			self.fields['subcategory'].queryset = SubCategory.objects.none()

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)
		widgets = {
			'text': forms.TextInput(attrs={'class':'form-control form-control-sm input-comment', 'placeholder':'Write comment'})
		}
		labels = {
			'text': '',
		}