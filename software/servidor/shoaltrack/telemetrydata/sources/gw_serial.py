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
from telemetrydata.schemas.Cardume import CardumeProtocol
 
class SerialNode(object):
    '''a serial  port interface'''
    def __init__(self, source, baud=115200, autoreconnect=False):
        self.baudrate = baud
        self.source = source
        
        self.autoreconnect = autoreconnect
        # we rather strangely set the baudrate initially to 1200, then change to the desired
        # baudrate. This works around a kernel bug on some Linux kernels where the baudrate
        # is not set correctly
        
        self.serialLink = None
        self.enable_thread = False #variable de finalizacion de trheats
        
        self.packets_Rx =[] #buffer de lineas parseadas
        
        self.packet_start = None
        self.packet_len_position =None
        
        self.protocol = CardumeProtocol()
        
        
    def start(self,):
        # Check your COM port and baud rate and configure IMU
        #dsrdtr=False, rtscts=False, xonxoff=False
        self.serialLink = serial.Serial() #solo creo la instancia del puerto serie control arduimu
        self.serialLink.baudrate = self.baudrate
        self.serialLink.port= self.source
        self.serialLink.timeout = 0
        try:
            self.serialLink.open()
            
        except serial.SerialException:
            #-- Error al abrir el puerto serie
            print ('Error al abrir puerto: ' + str(self.serialLink.port))
            return False
        
        self.packet_start = None
        self.packet_len_position =None
        self.serialLink.flush()
        
        return True
        
    def stop_thread(self,):
        self.enable_thread = False
    
    def close(self,):
        ''' Cierra el puerto serie de comunicacion
        '''
        if self.serialLink:
            self.serialLink.close()
        
        
    def set_baudrate(self, baudrate):
        '''set baudrate'''
        try:
            self.serialLink.setBaudrate(baudrate)
        except Exception:
            # for pySerial 3.0, which doesn't have setBaudrate()
            self.serialLink.baudrate = baudrate
            
    def reader(self,):
        '''Bucle de lectura de datos del puerto serie
        '''
        print('Enable Serial Thread...')
        self.enable_thread = True
        while self.enable_thread:
            need = self.protocol.bytes_needed() #cuantos necesito
            data_read= self.recv(need)
            
            addr_from, packet_rcv = self.protocol.parse_packet(data_read) #proceso mensage
            
            #salgo si no hay paquete
            if not packet_rcv:
                continue
            #continuo con la decodificacion:
            
            msg = self.protocol.parse_header(packet_rcv) #obtengo el header del mensage
            msg['payload'] = packet_rcv # le meto el pakete binario
            
            msg = self.decode(msg) #lo decodifico
            #solo lo meto sise decodifica bien
            try:
                if msg['msgID']:
                    self.packets_Rx.append(msg) #la meto en el buffer
            except:
                pass
        
    
    def decode(self, msg,keys=None):
        msg.update(self.protocol.parse_payload(msg,keys))
        
        return msg
    
    def recv(self,n):
        if n is None:
            n = 1
        waiting = self.serialLink.inWaiting()
        if waiting < n:
            n = waiting
        return  self.serialLink.read(n) # no es bloqueante, no espera a nada
    
    def write(self, buf):
        if not isinstance(buf, str):
            buf = str(buf)
            
        self.serialLink.write(buf)
        
    def get_line(self):
        if self.packets_Rx:
            return self.packets_Rx.pop()

        
    def available_data(self):
        if self.packets_Rx:
            return len(self.packets_Rx)
        else:
            return 0
