from django import template
from ..models import Wallet

register = template.Library()


@register.simple_tag
def get_wallet(**filters):
    return Wallet.objects.filter(**filters).first()


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
   
 
@register.filter
def index(indexable, i):
    return indexable[i]