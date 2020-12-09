# -*- coding: utf-8 -*-
u"""."""

from django import template

from basico import menu

register = template.Library()


@register.inclusion_tag('menu.html')
def show_menu_site(user=None):
    u"""."""
    lst = menu.get_list(user)
    stack = [[]]

    level_with_flag = -1

    for level, item, url, img, flag in lst:
        if flag:
            if level_with_flag == -1 or level_with_flag > level:
                level_with_flag = -1
                while len(stack) > level:
                    stack.pop()
                while len(stack) <= level:
                    node = (item, url, img, flag, [])
                    stack[-1].append(node)
                    stack.append(node[4])
        else:
            pass

    result = stack[0]
    return {'menulist': result}

@register.inclusion_tag('menu_user.html')
def show_menu_user(user=None):
    
    return {'user': user}