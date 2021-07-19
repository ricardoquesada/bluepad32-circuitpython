Introduction
============

.. image:: https://github.com/ricardoquesada/bluepad32-circuitpython/workflows/Build%20CI/badge.svg
    :target: https://github.com/ricardoquesada/bluepad32-circuitpython/actions/
    :alt: Build Status


.. image:: bluepad32-circuitpython-logo.png
    :alt: Logo

Bluetooth gamepad support for CircuitPython. Requires boards with an Airlift (ESP32) module.
The companion firmware for the ESP32 is `available on Gitlab <https://gitlab.com/ricardoquesada/bluepad32>`_.


Dependencies
=============
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

.. todo:: Add a quick, simple example. It and other examples should live in the
examples folder and be included in docs/examples.rst.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/ricardoquesada/CircuitPython_Org_bluepad32/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
