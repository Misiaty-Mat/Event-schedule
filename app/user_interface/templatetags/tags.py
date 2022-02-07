from django import template

register = template.Library()

@register.filter(name='countzip')
def countzip(value):
    print(dict(value))
    return sum(1 for _, i in value)