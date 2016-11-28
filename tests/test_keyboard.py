from openrazer import keyboard


def mock_write_file(path, content):
    return content


def mock_read_file(path):
    return 1


def mock_glob(path):

    if path == '/sys/bus/hid/drivers/hid-razer/*:*:*.*':
        return [
            '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003'
        ]

    if path == '/sys/bus/hid/drivers/hid-razer/*:*:*.*/mode_*':
        return [
            '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/mode_reactive',
            '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/mode_breath',
            '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/mode_static',
            '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/mode_starlight',
            '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/mode_none',
            '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/mode_wave',
            '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/mode_custom',
            '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/mode_spectrum'
        ]

    return []


keyboard.glob.glob = mock_glob
keyboard.write_file = mock_write_file
keyboard.read_file = mock_read_file
kb = keyboard.Keyboard()


def test_brightness_file():
    assert kb.brightness_file == '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/brightness'


def test_mode_list():
    assert kb.modes == frozenset([
        'breath', 'custom', 'none', 'reactive', 'spectrum', 'static', 'wave', 'starlight'
    ])


def test_repr():
    assert str(kb) == '<Keyboard: 1>'


def test_brightness():
    assert kb.brightness == 1


def test_write_file():
    assert keyboard.write_file('/tmp/none', str('string')) == 'string'
