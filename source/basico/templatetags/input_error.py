# -*- coding: utf-8 -*-
u"""."""

from django import template

register = template.Library()

@register.inclusion_tag('input_error.html')
def show_input_error(form_error):
    return { 'form_error': form_error} 