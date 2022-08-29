from django.template import Library


register = Library()


@register.simple_tag
def define(standard_form=False):
    return standard_form
