#!/usr/bin/env python
def rgbtohex(r, g, b):
    return chr(r) + chr(g) + chr(b)


def htmltohex(html_color):
    rbg = tuple(map(ord, html_color.decode('hex')))
    return rgbtohex(*rbg)


def tohex(color):
    length = len(color)

    if length == 6:
        return htmltohex(color)

    if isinstance(color, tuple):
        return rgbtohex(color)

    return color
