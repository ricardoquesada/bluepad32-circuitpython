Introduction
============


.. image:: https://github.com/ricardoquesada/bluepad32-circuitpython/workflows/Build%20CI/badge.svg
    :target: https://github.com/ricardoquesada/bluepad32-circuitpython/actions/
    :alt: Build Status


.. image:: https://img.shields.io/discord/775177861665521725.svg
    :target: https://discord.gg/r5aMn6Cw5q
    :alt: Discord


.. image:: img/bluepad32-circuitpython-logo.png
    :alt: Logo

Bluetooth gamepad support for CircuitPython. Requires boards with an AirLift (ESP32) module,
like the `Adafruit MatrixPortal M4 <https://www.adafruit.com/product/4745>`_.


Supported gamepads
==================

.. image:: https://lh3.googleusercontent.com/pw/AM-JKLWUZS_vlkMmd3o8EKzXlYCS0uriEW_gXfOoiFqZlABJi_dM1GWYHGafrdMnTP-VHgVdCdVA4pUageZgyI98RH1SHtydac2yyrx_vJVXgWPYBFN-SJoOikdlGuOowPoDqYOwfKU39yketYPJyRJlIPwjEw=-no
    :alt: Supported gamepads

With this library you can use any modern Bluetooth gamepad in CircuitPython.
Some of the supported gamepads, but not limited to, are:

* Sony family: DualSense (PS5), DualShock 4 (PS4), DualShock 3 (PS3)
* Nintendo family: Switch gamepads, Switch JoyCons, Wii, Wii U
* Xbox One S
* Android gamepads
* Window gamepads
* and more

For a complete list, see: https://gitlab.com/ricardoquesada/bluepad32/-/blob/main/docs/supported_gamepads.md


How does it work
================

As mentioned above, only boards with the AirLift (ESP32) co-processor are supported.
This is because the project consists of two parts:

* "Bluepad32 library for CircuitPython", runs on the main processor: "C"
* "Bluepad32 firmware", runs on the AirLift co-processor: "B"

.. image:: img/bluepad32-how-does-it-work.png
    :alt: How does it work

The gamepads (A), using Bluetooth, connect to the AirLift co-processor (B).

And AirLift (B) sends the gamepad data to the main processor (C). In this case the
main processor is the SAMD 51, but it could be different on other boards.

So, in order to use the library you have to flash the "Bluepad32 firmware" on AirLift.
This is a simple step that needs to be done just once, and can be undone at any time.
Info about Bluepad32 firmware is avaiable here:


* Bluepad32 firmware doc: https://gitlab.com/ricardoquesada/bluepad32/-/blob/master/docs/plat_airlift.md
* Download: https://gitlab.com/ricardoquesada/bluepad32/-/releases

Dependencies
============

This driver depends on:

* `Adafruit ESP32SPI <https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.



Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install bluepad32

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

A complete working example is available here:

* `bluepad32_simpletest.py <examples/bluepad32_simpletest.py>`_


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/ricardoquesada/CircuitPython_Org_bluepad32/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
