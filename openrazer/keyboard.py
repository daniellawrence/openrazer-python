""" Open RazerKeyboard Helpers """
import glob
from openrazer.common import tohex


class Keyboard(object):
    """ Open RazerKeyboard """

    # pylint: disable=too-many-instance-attributes

    WAVE_LEFT = 1
    WAVE_RIGHT = 2

    def __init__(self):
        base_device_path = "/sys/bus/hid/drivers/hid-razer/"
        device_glob_path = '{0}*:*:*.*'.format(base_device_path)
        modes_glob_path = '{0}/mode_*'.format(device_glob_path)

        found_devices = glob.glob(device_glob_path)
        self.mode_paths = glob.glob(modes_glob_path)
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
        """ List all the modes supported by the keyboard """
        all_modes = []
        mode_paths = '{0}/mode_'.format(self.device)
        for mode in self.mode_paths:
            all_modes.append(mode.replace(mode_paths, ''))
        return frozenset(all_modes)

    @property
    def device_type(self):
        """ return the device type """
        with open(self.device_type_file) as device_file:
            device_type = device_file.read().strip()
        return device_type

    def __repr__(self):
        """ What is this keyboard """
        return "<Keyboard: {0.device_type}>".format(self)

    @property
    def brightness(self):
        """ Fetch the keyboard brightness """
        with open(self.brightness_file) as device_file:
            brightness = device_file.read().strip()
        return int(brightness)

    @brightness.setter
    def brightness(self, value):
        """ Set the keyboard brightness """
        with open(self.brightness_file, 'w') as device_file:
            device_file.write(str(value))
        return int(value)

    def brightness_down(self, step=10):
        """ Decreate the brightness by 10 """
        current_brightness = self.brightness
        new_brightness = current_brightness - step
        self.brightness = new_brightness

    def brightness_up(self, step=10):
        """ Increase the brightness by 10 """
        current_brightness = self.brightness
        new_brightness = current_brightness + step
        self.brightness = new_brightness

    @property
    def rows(self):
        """ Number of key rows """
        with open(self.key_rows_file) as device_file:
            rows = device_file.read().strip()
        return int(rows)

    @property
    def columns(self):
        """ Number of columns """
        with open(self.key_columns_file) as device_file:
            cols = device_file.read().strip()
        return int(cols)

    def mode_none(self):
        """ Disable all modes """
        local_mode_file = self.mode_file.format('none')

        with open(local_mode_file, 'w') as device_file:
            device_file.write(str(1))

    def mode_custom(self):
        """ Use the custom mode """
        local_mode_file = self.mode_file.format('custom')

        with open(local_mode_file, 'w') as device_file:
            device_file.write(str(1))

    def mode_static(self, color):
        """ Set all the keyboard backlights to a single color"""
        local_mode_file = self.mode_file.format('static')
        hexcolor = tohex(color)

        with open(local_mode_file, 'w') as device_file:
            device_file.write(hexcolor)

    def mode_reactive(self, color):
        """ Set the keyboard to reactive mode """
        local_mode_file = self.mode_file.format('reactive')
        hexcolor = '\x02' + tohex(color)

        with open(local_mode_file, 'w') as device_file:
            device_file.write(hexcolor)

    def mode_starlight(self, colors=None):
        """ set the keyboard to starlight mode """
        local_mode_file = self.mode_file.format('starlight')

        send = None
        if not colors:
            send = '\x01'

        elif len(colors) == 1:
            send = '\x02' + tohex(colors[0])

        elif len(colors) == 2:
            send = '\x03' + ''.join([tohex(color) for color in colors])

        with open(local_mode_file, 'w') as device_file:
            device_file.write(send)

    def mode_breath(self, colors=None):
        """ Set mode to breath """
        local_mode_file = self.mode_file.format('breath')

        send = None
        if not colors:
            send = '1'

        elif len(colors) == 1:
            send = tohex(colors[0])

        elif len(colors) == 2:
            send = ''.join([tohex(color) for color in colors])

        with open(local_mode_file, 'w') as device_file:
            device_file.write(send)

    def mode_wave(self, state=2):
        """ Set mode to wave """
        local_mode_file = self.mode_file.format('wave')

        with open(local_mode_file, 'w') as device_file:
            device_file.write(str(state))

    def all_keys_off(self, color='000000'):
        """ Turn all the keys off(black) for custom mode """
        total_keys = self.rows * self.columns
        off_color = tohex(color)
        all_off = off_color * total_keys

        with open(self.set_key_color_file, 'w') as device_file:
            device_file.write(all_off)

    def set_theme(self, theme):
        """ Set key colors based on a theme """
        theme_string = str(theme)
        with open(self.set_key_color_file, 'w') as device_file:
            device_file.write(theme_string)
