from django import template
from ..models import Wallet

register = template.Library()


@register.simple_tag
def get_wallet(**filters):
    return Wallet.objects.filter(**filters).first()
