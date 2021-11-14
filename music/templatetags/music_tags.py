from django import template
from music.models import *

register = template.Library()


@register.simple_tag(name='getcat')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('music/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag('music/menu.html')
def show_menu():
    menu = [{'title': "About Site", 'url_name': 'about'},
            {'title': "Add News", 'url_name': 'add_page'},
            {'title': "Contacts", 'url_name': 'contact'},
            {'title': "Log In", 'url_name': 'login'},
            ]
    return {'menu': menu}
