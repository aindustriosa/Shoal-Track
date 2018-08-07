#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Programa para la adquisicion de datos de los nodos ShoalTrack y gestionarlos a
# través de una ingesta sobre DjangoREST
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

import time,os,sys
from configobj import ConfigObj
from validate import Validator

from sources.fileinput import file_input
from sources.serial import serialport

from protocols.Cardume import CardumeProtocol


class MasterSerialGateWay():
    '''
    Clase para la gestion de entrada y salida de datos hacia
    los dispositivos ShoalTrack
    '''
    def __init__(self,source, baudrate,protocol_gateway='cardume'):
        self.master = serialport(source,baudrate)
        
        self.server_alive = False
        
        if protocol_gateway == 'cardume':
            self.protocol = CardumeProtocol()
        
    def reader(self):
        #msg = m.recv_match(blocking=True) #bloqueante
        
        need = self.protocol.bytes_needed() #cuantos necesito
        if need <1:
            print('Bytes need: '+str(need))
        data_read= self.master.recv(need)
        if not data_read:#no hay nada recogido
            return None
        #if data_read:
        #   print(data_read)
        
        addr_from, packet_rcv = self.protocol.parse_packet(data_read) #proceso mensage
        
        if packet_rcv:
            #print('############################################')
            #print('llego paquete from: {} size: {}'.format(addr_from,len(packet_rcv)))
            
            msg = self.protocol.parse_header(packet_rcv) #obtengo el header del mensage
            msg['payload'] = packet_rcv
            
            return msg
        
        else:
            #print('No Correct Packet... ')
            return None
                
    def decode(self, msg,keys=None):
        msg['payload'] = self.protocol.parse_payload(msg,keys)
        
        return msg

class MasterFileGateWay():
    '''
    Clase para la gestion de entrada y salida de datos hacia
    los dispositivos ShoalTrack
    '''
    def __init__(self,source, protocol_gateway='cardume'):
        self.master = file_input(source)
        
        self.server_alive = False
        
        if protocol_gateway == 'cardume':
            self.protocol = CardumeProtocol()
        
    def reader(self):
        #msg = m.recv_match(blocking=True) #bloqueante
        
        need = self.protocol.bytes_needed() #cuantos necesito
        data_read= self.master.recv(need)
        #if data_read:
        #    print(data_read)
        
        addr_from, packet_rcv = self.protocol.parse_packet(data_read) #proceso mensage
        
        if packet_rcv:
            print('############################################')
            print('llego paquete from: {} size: {}'.format(addr_from,len(packet_rcv)))
            
            msg = self.protocol.parse_header(packet_rcv) #obtengo el header del mensage
            msg['payload'] = packet_rcv
            
            return msg
        
        else:
            return None
                
    def decode(self, msg,keys=None):
        msg['payload'] = self.protocol.parse_payload(msg,keys)
        
        return msg


def write_log(log_data):    
        with open(self.error_logfile, "a") as output_file:
            if type(error_data) is list:
                for item in error_data:
                    input_file.write(str(item)+'\n')
            else:
                input_file.write(str(error_data)+'\n')

####################################
#programa central
if __name__ == "__main__":
    
    #prctl.set_name('shoalgateway')
    logfile = 'log_telemetry.log'
    
    configspec = ConfigObj('settings_spec.conf', encoding="ISO-8859-1", list_values=False, _inspec=True)
    
    settings = ConfigObj('settings.conf', encoding="ISO-8859-1", configspec=configspec)
    val = Validator()
    test = settings.validate(val)
    if not test:
        print('Fail to parse config file..')
        sys.exit()
    
    print(settings)
    
    source_device=sys.argv[1]
    
    if (source_device == 'serial_device'):
        master_gtw = MasterSerialGateWay(settings['serial_device']['source'],
                                                         settings['serial_device']['baudrate'])
    elif (source_device == 'input_file'):
        master_gtw = MasterFileGateWay(settings['input_file']['source'],
                                                               settings['input_file']['protocol'])
    else:
        print('Source device not configured:', source_device)
        sys.exit()
    
    code = True
    while code:
        try:
            packet = master_gtw.reader()
            if packet:
                #print(packet)
                pkt = master_gtw.decode(packet)
                
                with open(logfile, "a") as output_file:
                    output_file.write(str(pkt)+'\n')
                
                if pkt['payload']['msgID']==129:
                    print('FROM:{0}\tId_Code:{1}\ttime_mark:{2}\
\tGPS:{3},{4}\tiTow:{5}\
\tPress:{6}\tLigth:{7}\tAx:{8}\tAy:{9}\tAcz:{10}\tBearing:{11}'.format(pkt['FROM'],
                                                                                                        pkt['Id_Code'],
                                                                                                        pkt['time_mark'],
                                                                                                        pkt['payload']['gps_latitude'],
                                                                                                        pkt['payload']['gps_longitude'],
                                                                                                        pkt['payload']['gps_itow'],
                                                                                                        pkt['payload']['pressure_avg'],
                                                                                                        pkt['payload']['ligth_avg'],
                                                                                                        pkt['payload']['accX_avg'],
                                                                                                        pkt['payload']['accY_avg'],
                                                                                                        pkt['payload']['accZ_avg'],
                                                                                                        pkt['payload']['bearing_avg']))
                
                elif pkt['payload']['msgID']==130:
                    print('FROM:{0}\tId_Code:{1}\tTime_mark:{2}\
\tWdir:{3}\tWspeed:{4}'.format(pkt['FROM'],
                                                                              pkt['Id_Code'],
                                                                              pkt['time_mark'],
                                                                              pkt['payload']['wind_direction_avg'],
                                                                              pkt['payload']['wind_speed_avg']))
                
                elif pkt['payload']['msgID']==131:
                    print('FROM:{0}\tId_Code:{1}\tTime_mark:{2}\
\tAirTemp:{3}\tHum:{4}\tAirPres:{5}'.format(pkt['FROM'],
                                                                              pkt['Id_Code'],
                                                                              pkt['time_mark'],
                                                                              pkt['payload']['air_temperature'],
                                                                              pkt['payload']['relative_humidity'],
                                                                              pkt['payload']['air_pressure']))
                
                elif pkt['payload']['msgID']==64:
                    print('FROM:{0}\tId_Code:{1}\tTime_mark:{2}\
\trssi:{3}\tGPS:{4},{5}\tiTow:{6}'.format(pkt['FROM'],
                                                                                             pkt['Id_Code'],
                                                                                             pkt['time_mark'],
                                                                                             pkt['payload']['rssi'],
                                                                                             pkt['payload']['gps_latitude'],
                                                                                             pkt['payload']['gps_longitude'],
                                                                                             pkt['payload']['gps_itow']))
                else:
                    print(pkt['FROM'],'|',pkt['time_mark'],'|',pkt['payload']['msgID'],pkt['payload'])
                #print(pkt)
                #if pkt['FROM'] == 11:
                #   print(pkt)
                    #print(pkt['FROM'], "| ",
                    #         pkt['payload']['accx_avg'],pkt['payload']['accx_std'],"| ",
                    #          pkt['payload']['accy_avg'],pkt['payload']['accy_std'],"| ",
                    #          pkt['payload']['accz_avg'],pkt['payload']['accz_std'])
                
        
        except KeyboardInterrupt:
            print('Exit: Cancelled by the user!!')
            code = False
    
    sys.exit()
