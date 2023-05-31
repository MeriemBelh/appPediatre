from django import template

register = template.Library()


@register.filter
def break_at_periods(value):
    paragraphs = value.split('. ')
    paragraphs_with_periods = [paragraph + '.' for paragraph in paragraphs]
    return '<br>'.join(paragraphs_with_periods)
