""" Open RazerKeyboard Helpers """
import glob
from openrazer.common import tohex, KEY_MAP


def write_file(path, content):
    """ Write a heap of bytes into a file found at path """
    if not isinstance(content, bytes):
        content = bytes(content)

    with open(path, 'wb') as device_file:
        device_file.write(content)

    return content


def read_file(path):
    """ Read a file and return a string """
    with open(path) as device_file:
        data = device_file.read()
        data = data.strip()

    return data


class Keyboard(object):
    """ Open RazerKeyboard """

    # pylint: disable=too-many-instance-attributes

    WAVE_LEFT = b'1'
    WAVE_RIGHT = b'2'
    ENABLE = b'1'

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
        return read_file(self.device_type_file)

    def __repr__(self):
        """ What is this keyboard """
        return "<Keyboard: {0.device_type}>".format(self)

    @property
    def brightness(self):
        """ Fetch the keyboard brightness """
        return int(read_file(self.brightness_file))

    @brightness.setter
    def brightness(self, value):
        """ Set the keyboard brightness """
        return write_file(self.brightness_file, value)

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

    @property
    def total_leds(self):
        """ Total number of LEDS on the keyboard """
        return self.rows * self.columns

    def mode_none(self):
        """ Disable all modes """
        local_mode_file = self.mode_file.format('none')
        write_file(local_mode_file, ENABLE)

    def mode_custom(self):
        """ Use the custom mode """
        local_mode_file = self.mode_file.format('custom')
        write_file(local_mode_file, ENABLE)

    def mode_static(self, color='00FF00'):
        """ Set all the keyboard backlights to a single color"""
        local_mode_file = self.mode_file.format('static')
        hexcolor = tohex(color)
        write_file(local_mode_file, hexcolor)

    def mode_reactive(self, color):
        """ Set the keyboard to reactive mode """
        local_mode_file = self.mode_file.format('reactive')
        hexcolor = '\x02' + tohex(color)
        write_file(local_mode_file, hexcolor)

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

        write_file(local_mode_file, send)

    def mode_breath(self, colors=None):
        """ Set mode to breath """
        local_mode_file = self.mode_file.format('breath')

        send = None
        if not colors:
            send = ENABLE

        elif len(colors) == 1:
            send = tohex(colors[0])

        elif len(colors) == 2:
            send = ''.join([tohex(color) for color in colors])

        write_file(local_mode_file, send)

    def mode_wave(self, state=WAVE_LEFT):
        """ Set mode to wave """
        assert state in [WAVE_LEFT, WAVE_RIGHT]
        
        local_mode_file = self.mode_file.format('wave')

        write_file(local_mode_file, state)

    def all_keys_off(self, color='000000'):
        """ Turn all the keys off(black) for custom mode """
        total_keys = self.rows * self.columns
        off_color = tohex(color)
        all_off = off_color * total_keys

        write_file(self.set_keys_color, all_off)

    def set_led_color(self, leds, color='ffffff'):
        """ Set the color of a single LED """
        if not isinstance(leds, list):
            leds = [leds]

        theme_string = ''
        off_color = tohex('000000')
        on_color = tohex(color)
        for index in range(1, self.total_leds + 1):
            if index in leds:
                theme_string += on_color
            else:
                theme_string += off_color
        self.set_theme(theme_string)

    def set_keys_color(self, keys, color='ffffff'):
        """ Set the color of all the LEDs for one or many keys """
        leds = []

        if not isinstance(keys, list):
            keys = [keys]

        for key in keys:
            key_leds = KEY_MAP.get(key, [])
            leds += key_leds

        self.set_led_color(leds, color)

    def set_theme(self, theme):
        """ Set key colors based on a theme """
        theme_string = bytes(theme)
        write_file(self.set_key_color_file, theme_string)
