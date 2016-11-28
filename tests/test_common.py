from openrazer import common

import pytest

# @pytest.mark.parametrize('red,green,blue,hexcolor,html', [
#    (00, 00, 00, b'\x00\x00\x00', '000000'),
#    (255, 00, 00, b'\xff\x00\x00', 'FF0000'),
#    (255, 255, 00, b'\xff\xff\x00', 'ffff00'),
#    (255, 255, 255, b'\xff\xff\xff', 'ffffff'),
# ])
# def test_rgbandhtml(red, green, blue, hexcolor, html):
#    assert common.rgbtohex(red, green, blue) == hexcolor


@pytest.mark.parametrize('name,hexcolor', [
    ('black', b'\x00\x00\x00'),
    ('000000', b'\x00\x00\x00'),
])
def test_tohex(name, hexcolor):
    assert common.tohex(name) == hexcolor
