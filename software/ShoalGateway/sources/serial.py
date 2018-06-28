#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Libreria para el acceso al puerto serie
# Copyright (C) 2018  AINDUSTRIOSA
#
# This Program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with This Program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email   : igonzalez@cetmar.org
# Web-Site: http://aindustriosa.org/  
 
import serial
 
class serialport(object):
    '''a serial  port interface'''
    def __init__(self, device, baud=115200, autoreconnect=False, source_system=254):
        self.baud = baud
        self.device = device
        
        self.autoreconnect = autoreconnect
        # we rather strangely set the baudrate initially to 1200, then change to the desired
        # baudrate. This works around a kernel bug on some Linux kernels where the baudrate
        # is not set correctly
        self.port = serial.Serial(self.device, 1200, timeout=0,
                                  dsrdtr=False, rtscts=False, xonxoff=False)
        
        self.source_system = source_system
        
        self.set_baudrate(self.baud)
        
        self.packet_start = None
        self.packet_len_position =None
        
        self.port.flush()
        
    def set_baudrate(self, baudrate):
        '''set baudrate'''
        try:
            self.port.setBaudrate(baudrate)
        except Exception:
            # for pySerial 3.0, which doesn't have setBaudrate()
            self.port.baudrate = baudrate
            
    def close(self):
        self.port.close()
        
    
    def recv(self,n):
        if n is None:
            n = 1
        waiting = self.port.inWaiting()
        if waiting < n:
            n = waiting
        return  self.port.read(n) # no es bloqueante, no espera a nada
    
    def write(self, buf):
        if not isinstance(buf, str):
            buf = str(buf)
            
        self.port.write(buf)
        
