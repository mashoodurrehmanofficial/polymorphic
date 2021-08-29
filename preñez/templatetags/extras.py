from django import template

register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)