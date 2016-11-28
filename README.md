[![Build Status](https://travis-ci.org/daniellawrence/openrazer-python.svg?branch=master)](https://travis-ci.org/daniellawrence/openrazer-python)
[![Coverage Status](https://coveralls.io/repos/github/daniellawrence/openrazer-python/badge.svg?branch=master)](https://coveralls.io/github/daniellawrence/openrazer-python?branch=master)
[![PyPi version](https://pypip.in/v/openrazer/badge.png)](https://crate.io/packages/openrazer/)
[![PyPi downloads](https://pypip.in/d/openrazer/badge.png)](https://crate.io/packages/openrazer/)

Python helpers for the OpenRazer Keyboard
==================================================

In order to use this you need to have https://github.com/openrazer/openrazer-drivers setup and working.

CLI Examples
---------------

Turn off the LEDs

	$ razercli off
	
Turn all the LEDS to 'ffffff'

	$ razercli static ffffff
	
Turn all the LEDS to salom

	$ razercli static salom


API Examples
---------

Set brightness to 50

    from openrazer import Keyboard
	kb = Keyboard()
	kb.brightness = 50

Set mode to reactive

    from openrazer import Keyboard
	kb = Keyboard()
	kb.mode_reactive('ff00ff')
