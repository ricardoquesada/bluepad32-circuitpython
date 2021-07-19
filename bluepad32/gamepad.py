# Copyright 2020 - 2021, Ricardo Quesada, http://retro.moe
# SPDX-License-Identifier: Apache-2.0

# Bluepad32 support for CircuitPython.
# Requires the Bluepad32 firmware (instead of Nina-fw).

"""
`bluepad32_gamepad`
================================================================================

Gamepad abstraction used for Bluepad32


* Author(s): Ricardo Quesada

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

* Adafruit ESP32SPI: https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://gitlab.com/ricardoquesada/bluepad32-circuitpython.git"

# DPAD constants.
DPAD_UP = const(1 << 0)
DPAD_DOWN = const(1 << 1)
DPAD_RIGHT = const(1 << 2)
DPAD_LEFT = const(1 << 3)

# Regular gamepad buttons.
BUTTON_A = const(1 << 0)
BUTTON_B = const(1 << 1)
BUTTON_X = const(1 << 2)
BUTTON_Y = const(1 << 3)
BUTTON_L1 = const(1 << 4)
BUTTON_R1 = const(1 << 5)
BUTTON_L2 = const(1 << 6)
BUTTON_R2 = const(1 << 7)
BUTTON_THUMB_L = const(1 << 8)
BUTTON_THUMB_R = const(1 << 9)


# MISC_BUTTONS_ are buttons that are usually not used in the game, but are
# helpers like "back", "home", etc.
MISC_BUTTON_SYSTEM = const(1 << 0)  # AKA: PS, Xbox, etc.
MISC_BUTTON_BACK = const(1 << 1)  # AKA: Select, Share, -
MISC_BUTTON_HOME = const(1 << 2)  # AKA: Start, Options, +


class Gamepad:
    """Implement gamepad abstraction"""

    def __init__(self, bp32, idx: int, state: dict):
        self._state = state
        self._bp32 = bp32
        self._idx = idx

    def set_player_leds(self, leds: int) -> bool:
        """
        Set the gamepad's player LEDs.

        Some gamepads have 4 LEDs that are used to indicate, among other things,
        the "player number".

        Applicable only to gamepads that have a player's LEDs like Nintendo Wii,
        Nintendo Switch, etc.

        :param int leds: Only the 4 LSB bits are used. Each bit indicates a LED.
        :return: True if the request was successful, False otherwise.
        """
        return self._bp32.set_gamepad_player_leds(self._idx, leds)

    def set_lightbar_color(self, rgb) -> bool:
        """
        Set the gamepad's lightbar color.

        Applicable only to gamepads that have a color LED like the Sony
        DualShok 4 or DualSense.

        :param tuple[int, int, int] rgb: Red,Green,Blue values to set.
        :return: True if the request was successful, False otherwise.
        """
        return self._bp32.set_gamepad_lightbar_color(self._idx, rgb)

    def set_rumble(self, force: int, duration: int) -> bool:
        """
        Set the gamepad's rumble (AKA force-feedback).

        Applicable only to gamepads that have rumble support, like Xbox One,
        DualShok 4, Nintendo Switch, etc.

        :param int force: 8-bit value where 255 is max force, 0 nothing.
        :param int duration: 8-bit value, where 255 is about 1 second.
        :return: True if the request was successful, False otherwise.
        """
        return self._bp32.set_gamepad_rumble(self._idx, force, duration)

    def set_state(self, state):
        self._state = state

    @property
    def buttons(self) -> int:
        return self._state["buttons"]

    @property
    def misc_buttons(self) -> int:
        return self._state["misc_buttons"]

    @property
    def axis_x(self) -> int:
        return self._state["axis_x"]

    @property
    def axis_y(self) -> int:
        return self._state["axis_y"]

    @property
    def axis_rx(self) -> int:
        return self._state["axis_rx"]

    @property
    def axis_ry(self) -> int:
        return self._state["axis_ry"]

    @property
    def dpad(self) -> int:
        return self._dpad

    @property
    def a(self) -> int:
        return self._state["buttons"] & BUTTON_A

    @property
    def b(self) -> int:
        return self._state["buttons"] & BUTTON_B

    @property
    def x(self) -> int:
        return self._state["buttons"] & BUTTON_X

    @property
    def y(self) -> int:
        return self._state["buttons"] & BUTTON_Y

    @property
    def l1(self) -> int:
        return self._state["buttons"] & BUTTON_L1

    @property
    def l2(self) -> int:
        return self._state["buttons"] & BUTTON_L2

    @property
    def r1(self) -> int:
        return self._state["buttons"] & BUTTON_R1

    @property
    def r2(self) -> int:
        return self._state["buttons"] & BUTTON_R2

    @property
    def thumb_l(self) -> int:
        return self._state["buttons"] & BUTTON_THUMB_L

    @property
    def thumb_r(self) -> int:
        return self._state["buttons"] & BUTTON_THUMB_R

    @property
    def type(self) -> int:
        return self._state["type"]

    def __str__(self):
        return self._state
