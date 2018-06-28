#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Libreria para el acceso a un fichero log
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
 
 
class file_input(object):
    '''a serial  port interface'''
    def __init__(self, source):
        self.filename = source
        
        #lo leo tododde golpe...
        self.bytes_read = open(self.filename, "rb").read()
        
        self.packet_len_position =0
            
    def close(self):
        self.bytes_read=None
        self.packet_len_position =0
        
    
    def recv(self,n):
        if n is None:
            n = 1
        waiting = len(self.bytes_read)-self.packet_len_position
        if waiting < n:
            n = waiting
            
        endpos=self.packet_len_position+n
        output = self.bytes_read[self.packet_len_position:endpos]
        
        self.packet_len_position=endpos
        
        return  output
    
    def write(self, buf):
        pass
        
