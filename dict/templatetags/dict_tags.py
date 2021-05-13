from django import template
from dict.models import Dictionary


register = template.Library()


@register.inclusion_tag('dict/includes/_navbar.html')
def show_navbar():
    dictionaries = Dictionary.objects.all()
    return {'dictionaries': dictionaries}
