from django import template

register = template.Library()



@register.filter(name='tostring')
def tostring(value):
    return str(value)
