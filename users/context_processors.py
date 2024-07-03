from .models import Profile
from django import template

register = template.Library()

@register.simple_tag
def profile_img(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        # Comprobamos si profile.image existe y tiene un atributo 'url'
        if profile.image and hasattr(profile.image, 'url'):
            return {'profile': profile.image.url}
    return {}