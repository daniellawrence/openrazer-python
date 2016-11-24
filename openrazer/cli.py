""" Razer Keyboard CLI """
from openrazer.keyboard import Keyboard
import click


@click.group()
def razer_cli():
    """ Razerkeyboard CLI """
    pass


@razer_cli.command()
@click.argument('color', default='ff00ff')
def static(color):
    """ Set the mode to static, default color ff00ff """
    keyboard = Keyboard()
    keyboard.mode_static(color)


@razer_cli.command()
def off():
    """ Set the mode to static, default color ff00ff """
    keyboard = Keyboard()
    keyboard.mode_none()
