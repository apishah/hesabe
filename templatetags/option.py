from django import template
from hesabe_app.models import  Credential
register = template.Library()

@register.simple_tag
def show_credential():
    credential = Credential.objects.all()
    return { 'knet' : credential[0].knet,"mpgs":credential[0].mpgs }