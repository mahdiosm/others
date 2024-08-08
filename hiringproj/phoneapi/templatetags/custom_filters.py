from django import template

register = template.Library()


@register.filter
def is_required(field):
    return field.field.required
