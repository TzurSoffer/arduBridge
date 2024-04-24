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
The Max3700 is an comm General Purpose Input/Output (GPIO) device.
The class includes methods to control it over the comm bus.
The __init__ method initializes the class with a reference to an comm object and the
device ID of the external GPIO device. It also has some class variables for storing the
comm register addresses for various functions of the device, such as setting the device
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
__copyright__ = "Copyright 2019"
__credits__ = [""]
__license__ = "GPL-3.0-or-later"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Production"

from GSOF_ArduBridge import CON_prn

class Max3700ExtGPIO():
    RES = {1:'OK', 0:'ERR', -1:'ERR'}
    def __init__(self, comm=False, devID=0x00, v=False):
        self.v = v
        self.comm = comm
        self.devID = devID

        self.ID = 'MAX3700-ID 0x%02x'%(devID)

        self.modeReg = 0x04
        self.bankModeReg = 0x09
        self.pinReg = 0x24
        self.portReg = 0x44
        self.pinZeroOffset = 8

        self.maxPorts = 7
        self.maxPins = 20

        self.DIR = {0:'Active-Low', 1:'Active-High', 2:'Input without pullup', 3:'Input + pullup'}
        self.MODE = {0:'Shutdown', 1:'Normal'}
        self.tDet = {0:'Disable', 1:'Enable'}

    def _getRegisters(self, reg, N):
        return self.comm.readRegister(self.devID, reg, N)

    def _setRegisters(self, reg, vals):
        return self.comm.writeRegister(self.devID, reg, vals)

    def setMode(self, mode=1, transitionDetection=0) -> list:
        """mode: 0 - Shutdown; 1 - Normal operation. transitionDetection: 0 - Disable; 1 - Enable"""
        if mode != 0:
            mode = 1
        val = mode
        val |= (transitionDetection&0x1)<<7
        reply = self._writeRegisters(self.modeReg, [mode])
        if self.v:
            CON_prn.printf('%s: MODE-Set: %s',
                           par=(self.ID, self.RES[reply[0]]),
                           v=True)
        return reply[0]

    def getMode(self) -> list:
        """"""
        reply = self._readRegisters(self.modeReg, 1)
        if self.v:
            if reply != -1:
                mode = reply[0]&1
                td = (reply[0]>>7)&1
                CON_prn.printf('%s: MODE-Get: %s, Transition-Detection: %s',
                               par=(self.ID, self.MODE[mode], self.tDet[td]),
                               v=True)
        return reply

    def setBankMode(self, B=0, val=[0x55]) -> list:
        if type(val) == int:
            val = [val]
        
        N = len(val)
        if (B+N) > self.maxPorts:
            N = self.maxPorts-B #< Set upto maxPort
        reply = self._writeRegister(self.bankModeReg+B, val)
        CON_prn.printf( '%s: bankMode Set: %s', par=(self.ID, self.RES[reply[0]]) )
        return reply

    def setAllPinsToOutput(self):
        self.setMode(mode=1)
        return self.setBankMode(0, val=[0x55]*self.maxPorts)

    def getBankMode(self, B=0, N=7) -> list:
        if (B+N) > self.maxPorts:
            N = self.maxPorts-B #< Get upto maxPorts
        reply = self._readRegister(self.bankModeReg+B, N)
        CON_prn.printf( '%s: bankMode: %s', par=(self.ID, str(reply)) )
        return reply

    def getAllPinsModes(self):
        self.getMode()
        return self.getBankMode(B=0, N=self.maxPorts)
        
##    def pinMode(self, pin, mode):
##        """
##        Set the mode of the specific pin#
##        """
##        reg = pin/4 +self.pinModeOffset
##        bitField = pin%4
##        vDat = [ord('D'), pin, mode]
##        self.comm.send(vDat)
##        reply = self.comm.receive(1)
##        if self.v:
##            CON_prn.printf('DIR%d: %s - %s', par=(pin, self.DIR[mode], self.RES[reply[0]]), v=True)
##        return reply[0]

    def setPin(self, pin, valList):
        """Set the state of the specific pin(s)#"""
        if type(valList) == int:
            valList = [valList]
        for val in valList:
            if (val != 0):
                val = 1
            pinReg = self.pinReg +self.pinZeroOffset +pin
            reply = self._writeRegister(pinReg, [val])
            CON_prn.printf('%s: PIN%d-Set: %d - %s', par=(self.ID, pin, val, self.RES[reply[0]]), v=self.v)
            pin += 1
        return reply[0]

    def clearAllPins(self):
        for port in [0,8,16,24]: #range(0,self.maxPorts):
            self.setPort(port, 0x00)
        
    def setPort(self, port, val):
        """Set the state of the specific port#"""
        portReg = self.portReg +self.pinZeroOffset +port
        reply = self._writeRegister(portReg, [val&0xff])
        if self.v:
            CON_prn.printf('%s: POPT%d-Set: %s', par=(self.ID, port, self.RES[reply[0]]), v=True)
        return reply[0]

    def getPin(self, pinList):
        """Read the state of the specific pin(s)#"""
        if type(pinList) == int:
            pinList = [pinList]
        result = []
        for pin in pinList:
            pinReg = self.pinReg +self.pinZeroOffset +pin
            reply = self._readRegister(pinReg, 1)
            if reply != -1:
                CON_prn.printf('%s: PIN%d = %d', par=(self.ID, pin, reply[0]), v=self.v)
                result.append(reply[0])
            else:
                CON_prn.printf('%s: PIN%d-Get: Error', par=(self.ID, pin), v=self.v)
                result.append(-1)
        return result

    def getPort(self, port):
        """Read the state of the specific port#"""
        portReg = self.portReg +self.pinZeroOffset +port
        reply = self._readRegister(portReg, 1)
        if reply != -1:
            CON_prn.printf('%s: PORT%d = 0x%02x (%s)', par=(self.ID, port, reply[0], bin(reply[0])), v=self.v)
            return reply[0]
        CON_prn.printf('%s: PORT%d-Get: Error', par=(self.ID, port), v=self.v)
        return -1
