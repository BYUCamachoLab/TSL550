import sys

import serial

class TSL550:
    def __init__(self, address, baudrate=9600, terminator="\r"):
        """
        Connect to the TSL550. Address is the serial port, baudrate
        can be set on the device, terminator is the string the marks
        the end of the command.
        """

        self.device = serial.Serial(address, baudrate=baudrate, timeout=None)

        if sys.version_info.major >= 3: # Python 3 compatibility: convert to bytes
            terminator = terminator.encode("ASCII")
        self.terminator = terminator

        # Make sure the laser is off
        self.off()

    def write(self, command):
        """
        Write a command to the TSL550. Returns the response (if any).
        """

        # Convert to bytes (Python 3 compatibility)
        if sys.version_info.major >= 3:
            command = command.encode("ASCII")

        # Write the command
        self.device.write(command + self.terminator)

        # Read response
        response = ""
        in_byte = self.device.read()
        while in_byte != self.terminator:
            if sys.version_info.major >= 3:
                response += in_byte.decode("ASCII")
            else:
                response += in_byte

            in_byte = self.device.read()

        return response

    def on(self):
        """Turn on the laser diode"""

        self.on = True
        self.write("LO")

    def off(self):
        """Turn off the laser diode"""

        self.on = False
        self.write("LF")

    def wavelength(self, val=None):
        """
        Tune the laser to a new wavelength. If a value is not
        specified, return the current one. Units: nm.
        """

        if val is not None:
            command = "WA{:.4f}".format(val) # Put the value rounded to 4 decimal places
        else:
            command = "WA"

        response = self.write(command)
        return float(response)

    def frequency(self, val=None):
        """
        Tune the laser to a new wavelength. If a value is not
        specified, return the current one. Units: THz.
        """

        if val is not None:
            command = "FQ{:.4f}".format(val) # Put the value rounded to 4 decimal places
        else:
            command = "FQ"

        response = self.write(command)
        return float(response)
