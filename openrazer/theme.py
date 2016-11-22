#!/usr/bin/env python
class KeyboardTheme(object):

    def __init__(self):
        self.keys = {}

    def set_color(self, key_name, key_color):
        key_name = key_name.lower()
        self.keys[key_name] = tohex(key_color)

    def __str__(self):
        return ''.join(self.keys.values())
