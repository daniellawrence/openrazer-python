#!/usr/bin/env python
import glob

from common import tohex

WAVE_LEFT = 1
WAVE_RIGHT = 2


class Keyboard(object):

    def __init__(self):
        BASE_DEVICE_PATH = "/sys/bus/hid/drivers/hid-razer/"
        DEVICE_GLOB_PATH = '{0}*:*:*.*'.format(BASE_DEVICE_PATH)
        MODES_GLOB_PATH = '{0}/mode_*'.format(DEVICE_GLOB_PATH)

        found_devices = glob.glob(DEVICE_GLOB_PATH)
        self.mode_paths = glob.glob(MODES_GLOB_PATH)
        self.device = found_devices[0]
        self.brightness_file = '{0.device}/brightness'.format(self)
        self.key_rows_file = '{0.device}/get_key_rows'.format(self)
        self.key_columns_file = '{0.device}/get_key_columns'.format(self)
        self.set_key_color_file = '{0.device}/set_key_colors'.format(self)
        self.device_type_file = '{0.device}/device_type'.format(self)
        self.mode_file = '{0.device}/mode_{{0}}'.format(self)
        self.known_mode = None

    @property
    def modes(self):
        all_modes = []
        mode_paths = '{0}/mode_'.format(self.device)
        for mode in self.mode_paths:
            all_modes.append(mode.replace(mode_paths, ''))
        return frozenset(all_modes)

    @property
    def device_type(self):
        with open(self.device_type_file) as f:
            device_type = f.read().strip()
        return device_type

    def __repr__(self):
        return "<Keyboard: {0.device_type}>".format(self)

    @property
    def brightness(self):
        with open(self.brightness_file) as f:
            brightness = f.read().strip()
        return int(brightness)

    @brightness.setter
    def brightness(self, value):
        with open(self.brightness_file, 'w') as f:
            f.write(str(value))
        return int(value)

    def brightness_down(self, step=10):
        current_brightness = self.brightness
        new_brightness = current_brightness - step
        self.brightness = new_brightness

    def brightness_up(self, step=10):
        current_brightness = self.brightness
        new_brightness = current_brightness + step
        self.brightness = new_brightness

    @property
    def rows(self):
        with open(self.key_rows_file) as f:
            rows = f.read().strip()
        return int(rows)

    @property
    def columns(self):
        with open(self.key_columns_file) as f:
            cols = f.read().strip()
        return int(cols)

    def mode_none(self):
        local_mode_file = self.mode_file.format('none')

        with open(local_mode_file, 'w') as f:
            f.write(str(1))

    def mode_custom(self):
        local_mode_file = self.mode_file.format('custom')

        with open(local_mode_file, 'w') as f:
            f.write(str(1))

    def mode_static(self, color):
        local_mode_file = self.mode_file.format('static')
        hexcolor = tohex(color)

        with open(local_mode_file, 'w') as f:
            f.write(hexcolor)

    def mode_reactive(self, color):
        local_mode_file = self.mode_file.format('reactive')
        hexcolor = '\x02' + tohex(color)

        with open(local_mode_file, 'w') as f:
            f.write(hexcolor)

    def mode_startlight(self, colors=[]):
        local_mode_file = self.mode_file.format('starlight')

        send = None
        if not colors:
            send = '\x01'

        elif len(colors) == 1:
            send = '\x02' + tohex(colors[0])

        elif len(colors) == 2:
            send = '\x03' + ''.join([tohex(color) for color in colors])

        with open(local_mode_file, 'w') as f:
            f.write(send)

    def mode_breath(self, colors=[]):
        local_mode_file = self.mode_file.format('breath')

        send = None
        if not colors:
            send = '1'

        elif len(colors) == 1:
            send = tohex(colors[0])

        elif len(colors) == 2:
            send = ''.join([tohex(color) for color in colors])

        with open(local_mode_file, 'w') as f:
            f.write(send)

    def mode_wave(self, state=2):
        local_mode_file = self.mode_file.format('wave')

        with open(local_mode_file, 'w') as f:
            f.write(str(state))

    def all_keys_off(self, key, color):
        total_keys = self.rows * self.columns
        OFF = tohex('000000')
        ALL_OFF = OFF * total_keys

        with open(self.set_key_color_file, 'w') as f:
            f.write(ALL_OFF)

    def set_key(self, key, color):
        total_keys = self.rows * self.columns
        OFF = tohex('000000')
        ALL_OFF = OFF * total_keys

        with open(self.set_key_color_file, 'w') as f:
            f.write(ALL_OFF)

    def set_theme(self, theme):
        theme_string = str(theme)
        with open(self.set_key_color_file, 'w') as f:
            f.write(theme_string)
