from openrazer import keyboard


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


def test_smoke():
    keyboard.glob.glob = mock_glob
    kb = keyboard.Keyboard()
    assert kb.brightness_file == '/sys/bus/hid/drivers/hid-razer/0003:1532:020F.0003/brightness'
