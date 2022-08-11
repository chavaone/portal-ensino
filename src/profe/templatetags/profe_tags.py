from django import template
import urllib, hashlib


register = template.Library()

@register.filter(name='avatar')
def avatar(user, size=35):
    email = str(user.email.strip().lower()).encode('utf-8')
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.parse.urlencode({'s':str(size)})
    return gravatar_url
