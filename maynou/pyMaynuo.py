#!/usr/bin/env python
#
#   Copyright 2014 David Ogilvy
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

"""

Driver for Maynuo Electronic DC Loads, for communication via the Modbus RTU protocol, utilizing the minimalmodbus python module.

"""

import minimalmodbus

__author__  = "David Ogilvy"
__email__   = "github@thortek.com.au"
__license__ = "Apache License, Version 2.0"

class MaynuoDCLoad( minimalmodbus.Instrument ):
    """Instrument class for Maynuo DC Loads. 
    
    Communicates via Modbus RTU protocol (via TTL Serial), using the *MinimalModbus* Python module.    

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    Implemented with these function codes (in decimal):
        
    ==================  ====================
    Description         Modbus function code
    ==================  ====================
    Read Coils          1
    Write Coils         5
    Read registers      3
    Write registers     16
    ==================  ====================

    """
    
    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.baudrate = 9600
        #minimalmodbus expects \x00 or \x01 values. Maynuo returns random byte values where only LSB counts. Redefining minimalmodbus function to workaround.
        minimalmodbus._bitResponseToValue = self._newbitResponseToValue 
    
#########################
## Redefined functions ##
#########################
    
    def _newbitResponseToValue(self, bytestring):
        minimalmodbus._checkString(bytestring, description='bytestring', minlength=1, maxlength=1)
        returnedValue = ord(bytestring)
        returnedValue &= 0x01
        return returnedValue

###############################
## Status and Function Coils ##
###############################

    def getPC1(self):
    	"""Returns status of Remote Control mode"""
    	return self.read_bit(1280, 1)

    def setPC1(self, value):
        """Turn on and off Remote Control. Set to 1 for ON"""
        self.write_bit(1280, value, 5)
    		
    def getPC2(self):
    	"""Returns status of Local Prohibition"""
    	return self.read_bit(1281, 1)

    def setPC2(self, value):
        """Turn on and off Remote Control. Set to 1 for ON"""
        self.write_bit(1281, value, 5)  
        
    def getTrig(self):
    	"""Returns Trigger Status"""
    	return self.read_bit(1282, 1)

    def setTrig(self, value):
        """Sets Trigger remotely. Set 1 for on."""
        self.write_bit(1282, value, 5) 

    def getRemoteSense(self):
    	"""Returns remote sense status"""
    	return self.read_bit(0x0503, 1)

    def setRemoteSense(self, value):
        """Sets remote sense. Set 1 for on."""
        self.write_bit(1283, value, 5)

    def getInputStatus(self):
    	"""Returns current input status. Load ON/OFF."""
    	return self.read_bit(1296, 1)
    	
    def getTrackingStatus(self):
    	"""Returns current tracking status. 0=current 1=voltage."""
    	return self.read_bit(1297, 1)

    def getMemoryStatus(self):
    	"""Returns current ??? status. 0=? 1=?."""
    	return self.read_bit(1298, 1)

    def getKeybeepStatus(self):
    	"""Returns current key-press beeper status. 0=off 1=on."""
    	return self.read_bit(1299, 1)

    def getConnectStatus(self):
    	"""Returns current ??? status. 0=single 1=multi."""
    	return self.read_bit(1300, 1)

    def getAutoTestStatus(self):
    	"""Returns current atest status. 0=off 1=automatic test mode."""
    	return self.read_bit(1301, 1)

    def getAutoTestTriggerStatus(self):
    	"""Returns current atestun status. 0=off 1=Auto test pattern waiting for trigger."""
    	return self.read_bit(1302, 1)

    def getAutoTestResult(self):
    	"""Returns current auto test result. 0=automatic test failed 1=automatic test passed."""
    	return self.read_bit(1303, 1)

    def getOverCurrentStatus(self):
    	"""Returns over-current status flag. 0=ok 1=over."""
    	return self.read_bit(1312, 1)
    
    def getOverVoltageStatus(self):
    	"""Returns over-voltage status flag. 0=ok 1=over."""
    	return self.read_bit(1313, 1)

    def getOverPowerStatus(self):
    	"""Returns over-power status flag. 0=ok 1=over."""
    	return self.read_bit(1314, 1)

    def getOverTempStatus(self):
    	"""Returns over-heat status flag. 0=ok 1=over."""
    	return self.read_bit(1315, 1)
    
    def getReverseConnectionStatus(self):
    	"""Returns reverse connection status flag. 0=ok 1=reversed."""
    	return self.read_bit(1316, 1)

    def getUnregisteredParameterStatus(self):
    	"""Returns registered parameter failed status flag?. 0=ok 1=fail."""
    	return self.read_bit(1317, 1)

    def getEepromStatus(self):
    	"""Returns EEPROM status flag. 0=ok 1=error."""
    	return self.read_bit(1318, 1)

    def getCalDataStatus(self):
    	"""Returns calibration data status. 0=ok 1=error."""
    	return self.read_bit(1319, 1)    
    
    ## Registers and Commands
    
    def getVoltage(self):
    	"""Reads current voltage."""
    	return self.read_float(0x0B00)
    	
    def getCurrent(self):
    	"""Reads current voltage."""
    	return self.read_float(0x0B02)
    	    	
    def getModel(self):
    	"""Reads current voltage."""
    	return self.read_register(0x0B06)    	
    	
    def getVersion(self):
    	"""Reads current voltage."""
    	return self.read_register(0x0B07)  
    	
    def getConstantCurrent(self):
    	"""Reads the set Constant Current value"""
    	return self.read_float(0x0A01)
    
    def setConstantCurrent(self, value):
    	"""Reads the set Constant Current value"""
    	return self.write_float(0x0A01, value)	
    
    #remaining functions TBC


    	
