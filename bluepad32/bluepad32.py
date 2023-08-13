# Copyright 2020 - 2023, Ricardo Quesada, http://retro.moe
# SPDX-License-Identifier: Apache-2.0

# Bluepad32 support for CircuitPython.
# Requires the Bluepad32 firmware (instead of Nina-fw).

"""
`bluepad32_bluepad32`
================================================================================

Gamepad support for Airlift-based board.


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

import struct

from adafruit_esp32spi import adafruit_esp32spi
from micropython import const
from bluepad32.gamepad import Gamepad  # pylint: disable=no-name-in-module


# Nina-fw commands stopped at 0x50. Bluepad32 extensions start at 0x60. See:
# https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI/blob/master/adafruit_esp32spi/adafruit_esp32spi.py
_GET_PROTOCOL_VERSION = const(0x00)
_GET_GAMEPADS_DATA = const(0x01)
_SET_GAMEPAD_PLAYER_LEDS = const(0x02)
_SET_GAMEPAD_LIGHTBAR_COLOR = const(0x03)
_SET_GAMEPAD_RUMBLE = const(0x04)
_FORGET_BLUETOOTH_KEYS = const(0x05)
_ENABLE_BLUETOOTH_CONNECTIONS = const(0x07)
_GET_CONTROLLERS_DATA = const(0x09)

_MAX_GAMEPADS = const(4)

_PROTOCOL_VERSION_HI = const(1)
_PROTOCOL_VERSION_LO = const(0)


class Bluepad32(adafruit_esp32spi.ESP_SPIcontrol):
    """Implement the SPI commands for Bluepad32"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # callbacks for when a gamepad gets connected / disconnected
        self._on_connect = None
        self._on_disconnect = None

        # known connected gamepads: bitmask
        self._prev_connected_gamepads = 0

        # gamepads
        self._gamepads = (
            Gamepad(self, 0, {}),
            Gamepad(self, 1, {}),
            Gamepad(self, 2, {}),
            Gamepad(self, 3, {}),
        )

        self._check_protocol()

    def update(self) -> list:
        """
        Return a list of connected gamepads.

        Each gamepad entry is a dictionary that represents the gamepad state:
        gamepad index, buttons pressed, axis values, dpad and more.

        :returns: List of connected gamepads.
        """
        self._send_command(_GET_CONTROLLERS_DATA)
        resp = self._wait_response_cmd(_GET_CONTROLLERS_DATA)

        connected_gamepads = 0

        # Update gamepads state
        for g in resp:
            unp = struct.unpack("<BBBiiiiiiHBiiiiiiB", g)
            state = {
                "idx": unp[0],
                "class": unp[1],
                "dpad": unp[2],
                "axis_x": unp[3],
                "axis_y": unp[4],
                "axis_rx": unp[5],
                "axis_ry": unp[6],
                "brake": unp[7],
                "throttle": unp[8],
                "buttons": unp[9],
                "misc_buttons": unp[10],
                "gyro_x": unp[11],
                "gyro_y": unp[12],
                "gyro_z": unp[13],
                "accel_x": unp[14],
                "accel_y": unp[15],
                "accel_z": unp[16],
                "battery": unp[17],
            }

            # Sanity check.
            if state["idx"] < 0 or state["idx"] >= len(self._gamepads):
                return

            self._gamepads[state["idx"]].set_state(state)

            # Update connected gamepads bitmask
            connected_gamepads |= 1 << state["idx"]

        # Any change from prev state?
        if connected_gamepads == self._prev_connected_gamepads:
            return

        for idx in range(_MAX_GAMEPADS):
            bit = 1 << idx
            current = connected_gamepads & bit
            prev = self._prev_connected_gamepads & bit

            # No change in state
            if current == prev:
                continue

            if current != 0:
                self._on_connect(self._gamepads[idx])
            else:
                self._on_disconnect(self._gamepads[idx])
        self._prev_connected_gamepads = connected_gamepads

    def set_gamepad_player_leds(self, gamepad_idx: int, leds: int) -> bool:
        """
        Set the gamepad's player LEDs.

        Some gamepads have 4 LEDs that are used to indicate, among other things,
        the "player number".

        Applicable only to gamepads that have a player's LEDs like Nintendo Wii,
        Nintendo Switch, etc.

        :param int gamepad_idx: Gamepad index, returned by get_gamepads_data().
        :param int leds: Only the 4 LSB bits are used. Each bit indicates a LED.
        :return: True if the request was successful, False otherwise.
        """
        resp = self._send_command_get_response(
            _SET_GAMEPAD_PLAYER_LEDS, ((gamepad_idx,), (leds,))
        )
        return resp[0][0] == 1

    def set_gamepad_lightbar_color(self, gamepad_idx: int, rgb) -> bool:
        """
        Set the gamepad's lightbar color.

        Applicable only to gamepads that have a color LED like the Sony
        DualShok 4 or DualSense.

        :param int gamepad_idx: Gamepad index, returned by get_gamepads_data().
        :param tuple[int, int, int] rgb: Red,Green,Blue values to set.
        :return: True if the request was successful, False otherwise.
        """
        # Typing is not supported in CircuitPython. Parameter "rgb" should be:
        #  Typing.tuple[int, int, int]
        resp = self._send_command_get_response(
            _SET_GAMEPAD_LIGHTBAR_COLOR, ((gamepad_idx,), rgb)
        )
        return resp[0][0] == 1

    def set_gamepad_rumble(self, gamepad_idx: int, force: int, duration: int) -> bool:
        """
        Set the gamepad's rumble (AKA force-feedback).

        Applicable only to gamepads that have rumble support, like Xbox One,
        DualShok 4, Nintendo Switch, etc.

        :param int gamepad_idx: Gamepad index, returned by get_gamepads_data().
        :param int force: 8-bit value where 255 is max force, 0 nothing.
        :param int duration: 8-bit value, where 255 is about 1 second.
        :return: True if the request was successful, False otherwise.
        """
        resp = self._send_command_get_response(
            _SET_GAMEPAD_RUMBLE, ((gamepad_idx,), (force, duration))
        )
        return resp[0][0] == 1

    def forget_bluetooth_keys(self) -> bool:
        """
        Forget stored Bluetooth keys.

        After establishing a Bluetooth connection, a key is saved in the ESP32.
        This is useful for a quick reconnect. Removing the keys requires to
        establish a new connection, something that might be needed in some
        circumstances.

        :return: True if the request was successful, False otherwise.
        """
        resp = self._send_command_get_response(_FORGET_BLUETOOTH_KEYS)
        return resp[0][0] == 1

    def enable_bluetooth_connections(self, enabled: bool) -> bool:
        """
        Enable / Disable new Bluetooth connections.

        When enabled, the device is put in Discovery mode, and new pairings are
        accepted. When disabled, only devices that have paired before can connect.
        Established connections are not affected.

        :return: True if the request was successful, False otherwise.
        """
        resp = self._send_command_get_response(
            _ENABLE_BLUETOOTH_CONNECTIONS, ((bool(enabled),),)
        )
        return resp[0][0] == 1

    def setup_callbacks(self, on_connect, on_disconnect) -> None:
        """
        Setup "on gamepad connect" and "on gamepad disconnect" callbacks.
        """
        self._on_connect = on_connect
        self._on_disconnect = on_disconnect

    def _check_protocol(self) -> bool:
        resp = self._send_command_get_response(_GET_PROTOCOL_VERSION)
        ver_hi = resp[0][0]
        if ver_hi != _PROTOCOL_VERSION_HI:
            ver_lo = resp[0][1]
            print(
                "ERROR: Invalid protocol version. "
                + f"Expected {_PROTOCOL_VERSION_HI}.{_PROTOCOL_VERSION_LO}, got: {ver_hi}.{ver_lo}"
            )
            return False
        return True
