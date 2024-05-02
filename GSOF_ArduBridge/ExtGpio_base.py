#!/usr/bin/env python
"""
    This file is part of GSOF_ArduBridge.

    GSOF_ArduBridge is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GSOF_ArduBridge is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GSOF_ArduBridge.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
The __init__ method initializes the class with a reference to an I2C object and the
device ID of the external GPIO device. It also has some class variables for storing the
I2C register addresses for various functions of the device, such as setting the device
mode or reading/writing to the device ports.
The class has several methods for interacting with the external GPIO device.
The modeSet method can be used to set the operating mode of the device, either "normal" or "shutdown".
The modeGet method can be used to read the current operating mode of the device.
The bankModeSet and bankModeGet methods can be used to set and get the direction
(input or output) of the individual pins on the device. The portWrite and portRead methods
can be used to write values to and read values from the device ports, respectively.
The pinMode and pinRead methods can be used to set the direction and read the value
of an individual pin, respectively.
"""

__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = "Copyright 2024"
__credits__ = [""]
__license__ = "GPL-3.0-or-later"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Production"

def pinPortMask(pin, pinsInPort=8):
    port  = int(pin/pinsInPort)
    pin   = int(pin%pinsInPort)
    mask  = int(1<<pin)
    return (pin, port, mask)

class ExtGPIO_base():
    maxPorts = 0
    maxPins = 0
    OUTPUT = 0
    INPUT  = 1
    RES = {1:'OK', 0:'ERR', -1:'ERR'}

    def __init__(self, comm=False, devID=0x00, v=False):
        self.ID = 'ExtendedGPIO-ID 0x%02x'%(devID)
        self.v = v
        self.comm = comm
        self.devID = devID

### Device level API
    def setMode(self, mode=0) -> int:
        return -1

    def getMode(self) -> int:
        return -1
        
    def clearAllPins(self) -> None:
        return

    def setAllPinsToOutput(self) -> int:
        return 1

    def getAllPinsModes(self) -> list:
        return [0]*self.maxPins
        
### Port level API
    def setPortMode(self, port, val) -> list:
        if type(val) == int:
            val = [val]
        return [1]*len(val)

    def setBankMode(self, port, val) -> list:
        if type(val) == int:
            val = [val]
        return [1]*len(val)

    def getPortMode(self, port=0, N=1) -> list:
        return [0]*N

    def setPort(self, port, val) -> int:
        """Set the state of the specific port#"""
        return 1

    def getPort(self, port) -> int:
        """Read the state of the specific port#"""
        return 1

### Pin level API
    def setPinMode(self, pin, mode):
        """Set the direction of an individual pin"""
        return 1

    def setPin(self, pin, valList):
        """Set the state of the specific pin(s)#"""
        if type(valList) == int:
            valList = [valList]
        return [1]*len(pinList)

    def getPin(self, pinList):
        """Read the state of the specific pin(s)#"""
        if type(pinList) == int:
            pinList = [pinList]
        return [1]*len(pinList)
