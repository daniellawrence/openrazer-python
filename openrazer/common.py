""" Color things """


def rgbtohex(red=None, green=None, blue=None):
    """ Convert a (red, green, blue) tuple in to hex colors """
    return chr(red) + chr(green) + chr(blue)


def htmltohex(html_color):
    """ Conver html style HEX into python hex """
    (red, green, blue) = tuple(map(ord, html_color.decode('hex')))
    return rgbtohex(red, green, blue)


def tohex(color):
    """ convert anything to python style hex """
    length = len(color)

    if length == 6:
        return htmltohex(color)

    if isinstance(color, tuple):
        return rgbtohex(color)

    return color
