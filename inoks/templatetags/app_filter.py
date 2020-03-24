from django import template

from inoks.models import Order

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_latest_situation')
def get_latest(order):
    order = Order.objects.get(pk=order.id)
    return order.latest_catch()
