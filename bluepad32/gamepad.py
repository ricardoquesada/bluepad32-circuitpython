# Copyright 2020 - 2023, Ricardo Quesada, http://retro.moe
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
from micropython import const

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


class Gamepad:  # pylint: disable=too-many-public-methods
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
        """Set the gamepad state"""
        self._state = state

    @property
    def buttons(self) -> int:
        """Return the a bitmaks that represents the buttons state"""
        return self._state["buttons"]

    @property
    def misc_buttons(self) -> int:
        """Return the a bitmaks that represents the 'misc buttons' state"""
        return self._state["misc_buttons"]

    @property
    def axis_x(self) -> int:
        """Return the value of Axis X.

        Value goes from -511 to 512.
        """
        return self._state["axis_x"]

    @property
    def axis_y(self) -> int:
        """Return the value of Axis Y.

        Value goes from -511 to 512.
        """
        return self._state["axis_y"]

    @property
    def axis_rx(self) -> int:
        """Return the value of the right Axis X.

        Value goes from -511 to 512.
        """
        return self._state["axis_rx"]

    @property
    def axis_ry(self) -> int:
        """Return the value of the right Axis Y.

        Value goes from -511 to 512.
        """
        return self._state["axis_ry"]

    @property
    def brake(self) -> int:
        """Return the value of the Brake.

        Value goes from 0 to 1023.
        """
        return self._state["brake"]

    @property
    def throttle(self) -> int:
        """Return the value of the Throttle.

        Value goes from 0 to 1023.
        """
        return self._state["throttle"]

    @property
    def gyro_x(self) -> int:
        """Return the value of Gyroscope X.

        Value goes from -511 to 512.
        """
        return self._state["gyro_x"]

    @property
    def gyro_y(self) -> int:
        """Return the value of Gyroscope Y.

        Value goes from -511 to 512.
        """
        return self._state["gyro_y"]

    @property
    def gyro_z(self) -> int:
        """Return the value of Gyroscope Z.

        Value goes from -511 to 512.
        """
        return self._state["gyro_z"]

    @property
    def accel_x(self) -> int:
        """Return the value of Accelerometer X.

        Value goes from -511 to 512.
        """
        return self._state["accel_x"]

    @property
    def accel_y(self) -> int:
        """Return the value of Accelerometer Y.

        Value goes from -511 to 512.
        """
        return self._state["accel_y"]

    @property
    def accel_z(self) -> int:
        """Return the value of Accelerometer Z.

        Value goes from -511 to 512.
        """
        return self._state["accel_z"]

    @property
    def dpad(self) -> int:
        """Return the DPAD state"""
        return self._state["dpad"]

    @property
    def button_a(self) -> int:
        """Return whether button A is pressed"""
        return self._state["buttons"] & BUTTON_A

    @property
    def button_b(self) -> int:
        """Return whether button B is pressed"""
        return self._state["buttons"] & BUTTON_B

    @property
    def button_x(self) -> int:
        """Return whether button X is pressed"""
        return self._state["buttons"] & BUTTON_X

    @property
    def button_y(self) -> int:
        """Return whether button Y is pressed"""
        return self._state["buttons"] & BUTTON_Y

    @property
    def button_l1(self) -> int:
        """Return whether button L1 is pressed"""
        return self._state["buttons"] & BUTTON_L1

    @property
    def button_l2(self) -> int:
        """Return whether button L2 is pressed"""
        return self._state["buttons"] & BUTTON_L2

    @property
    def button_r1(self) -> int:
        """Return whether button R1 is pressed"""
        return self._state["buttons"] & BUTTON_R1

    @property
    def button_r2(self) -> int:
        """Return whether button R2 is pressed"""
        return self._state["buttons"] & BUTTON_R2

    @property
    def button_thumb_l(self) -> int:
        """Return whether left thumb buttons is pressed"""
        return self._state["buttons"] & BUTTON_THUMB_L

    @property
    def button_thumb_r(self) -> int:
        """Return whether right thumb buttons is pressed"""
        return self._state["buttons"] & BUTTON_THUMB_R

    @property
    def type(self) -> int:
        """Return the gamepad type (AKA model)"""
        return self._state["type"]

    def __str__(self):
        return self._state
