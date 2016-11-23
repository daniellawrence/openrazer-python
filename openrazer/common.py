""" Color things """
import codecs

KEY_MAP = {
    # top row
    'esc': [2],
    'f1': [3],
    'f2': [4],
    'f3': [5],
    'f4': [6],
    'f5': [7],
    'f6': [8],
    'f7': [9],
    'f8': [10],
    'f9': [11],
    'f10': [12],
    'f11': [13],
    'f12': [14],
    'ins': [15],
    'del': [16],

    # number row
    '`': [18],
    '1': [19],
    '2': [20],
    '3': [21],
    '4': [22],
    '5': [23],
    '6': [24],
    '7': [25],
    '8': [26],
    '9': [27],
    '0': [28],
    '-': [29],
    '=': [30],
    'backspace': [31, 32]
}


def rgbtohex(red=None, green=None, blue=None):
    """ Convert a (red, green, blue) tuple in to hex colors """
    return chr(red) + chr(green) + chr(blue)


def htmltohex(html_color):
    """ Conver html style HEX into python hex """
    html_color = bytes(html_color, 'utf-8')
    html_color, _ = codecs.getdecoder("hex_codec")(html_color)
    return html_color


def tohex(color):
    """ convert anything to python style hex """
    length = len(color)

    if length == 6:
        return htmltohex(color)

    if isinstance(color, tuple):
        return rgbtohex(color)

    return color
