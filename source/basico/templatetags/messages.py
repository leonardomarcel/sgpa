from django import template

register = template.Library()

@register.inclusion_tag('messages.html')
def show_messages(messages=None):
    
    return {'messages': messages}

@register.filter('for_number') 
def range_to_number(number):
    return range(number)