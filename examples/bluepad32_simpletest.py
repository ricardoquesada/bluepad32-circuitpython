# Copyright 2020 - 2021, Ricardo Quesada, http://retro.moe
# SPDX-License-Identifier: Apache-2.0

import time

from bluepad32.bluepad32 import Bluepad32
from bluepad32 import gamepad

import board
import busio
from digitalio import DigitalInOut
from micropython import const


class SimpleTest:
    def __init__(self):

        # Connected gamepad
        self._gamepad = None

        # If you are using a board with pre-defined ESP32 Pins:
        esp32_cs = DigitalInOut(board.ESP_CS)
        esp32_ready = DigitalInOut(board.ESP_BUSY)
        esp32_reset = DigitalInOut(board.ESP_RESET)

        # If you have an AirLift Shield:
        # esp32_cs = DigitalInOut(board.D10)
        # esp32_ready = DigitalInOut(board.D7)
        # esp32_reset = DigitalInOut(board.D5)

        # If you have an AirLift Featherwing or ItsyBitsy Airlift:
        # esp32_cs = DigitalInOut(board.D13)
        # esp32_ready = DigitalInOut(board.D11)
        # esp32_reset = DigitalInOut(board.D12)

        # If you have an externally connected ESP32:
        # NOTE: You may need to change the pins to reflect your wiring
        # esp32_cs = DigitalInOut(board.D10)
        # esp32_ready = DigitalInOut(board.D9)
        # esp32_reset = DigitalInOut(board.D6)

        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self._bp32 = Bluepad32(spi, esp32_cs, esp32_ready, esp32_reset, debug=0)
        self._bp32.setup_callbacks(self.on_connect, self.on_disconnect)

        # Optionally, to enable UART logging in the ESP32
        # self._bp32.set_debug(1)

        # Delete Bluetooth stored keys. Might make connection easier (or more difficult).
        # self._bp32.forget_bluetooth_keys()

        # Should display "Bluepad32 for Airlift vXXX"
        print("Firmware version:", self._bp32.firmware_version)

    def on_connect(self, gp):
        print("on_connect")
        self._gamepad = gp

    def on_disconnect(self, gp):
        print("on_disconnect")
        self._gamepad = None

    def loop(self):
        first_time = False
        color = [0xFF, 0x00, 0x00]
        players_led = 0x01

        while True:
            self._bp32.update()

            if self._gamepad is None:
                continue

            gp = self._gamepad

            if first_time == False:
                first_time = True
                # Prints the entire gamepad state.
                # This function is used mostly for debug.
                print(gp)

                gp.set_lightbar_color(color)

            if gp.a:  # Button A pressed ?
                # Shuffle colors. "random.shuffle" not preset in CircuitPython
                color = (color[2], color[0], color[1])
                gp.set_lightbar_color(color)

            if gp.b:  # Button B pressed ?
                gp.set_player_leds(players_led)
                players_led += 1
                players_led &= 0x0F

            if gp.x:  # Button X pressed ?
                force = 128  # 0-255
                duration = 10  # 0-255
                gp.set_rumble(force, duration)

            time.sleep(0.032)


def run():
    test = SimpleTest()
    test.loop()


run()
