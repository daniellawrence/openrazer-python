""" Keyboard Themes Object for Open Razer Keyboard """
from openrazer.common import tohex


class KeyboardTheme(object):
    """ Keyboard Themes Object for Open Razer Keyboard """

    def __init__(self):
        self.keys = {}

    def set_color(self, key_name, key_color):
        """ Set the color for a key_name """
        key_name = key_name.lower()
        self.keys[key_name] = tohex(key_color)

    def get_color(self, key_name):
        """ Fetch the color for a key_name """
        return self.keys[key_name]

    def __str__(self):
        return ''.join(self.keys.values())
