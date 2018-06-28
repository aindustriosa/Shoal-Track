 #!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Protocolo de trasmision de datos para la red ShoalNet
# Copyright (C) 2017  CETMAR
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
# Email   : igonzalez@cetmar.org, ecounago@cetmar.org, cau
# Web-Site: http://utmar.cetmar.org/ 

from datetime import datetime
from pytz import UTC
import json

class x25crc():
    '''x25 CRC - based on checksum.h from mavlink library'''
    def __init__(self, buf=None):
        self.crc = 0xffff
        if buf is not None:
            if isinstance(buf, str):
                self.accumulate_str(buf)
            else:
                self.accumulate(buf)

    def accumulate(self, buf):
        '''add in some more bytes'''
        accum = self.crc
        for b in buf:
            tmp = b ^ (accum & 0xff)
            tmp = (tmp ^ (tmp<<4)) & 0xFF
            accum = (accum>>8) ^ (tmp<<8) ^ (tmp<<3) ^ (tmp>>4)
        self.crc = accum

    def accumulate_str(self, buf):
        '''add in some more bytes'''
        accum = self.crc
        import array
        bytes = array.array('B')
        bytes.fromstring(buf)
        self.accumulate(bytes)
        
    def check(self, HByte, LByte):
        compose = (HByte<<8)+LByte
        if compose == self.crc:
            return True
        else:
            return False
        



class ShoalNet():
    '''
    Clase para la gestion del protocolo de ShoalTrack
    '''
    HEADERSIZE = 5
    
    START_PACKET = b'\xfa'
    
    
    
    START_PACKET_POS = 0
    LEN_PACKET_POS   = 1
    FROM_PACKET_POS  = 2
    SEQ_PACKET_POS   = 3
    ID_PACKET_POS    = 4
    
    #STATUS PACKET DECODE
    WAITING_START_PACKET = 1
    WAITING_HEADER       = 2
    WAITING_BODY         = 3
    COMPLETE_RAW_PACKET  = 4
    ERROR_SIZE           = 4
    FINISH_OK            = 0
    
    #ID PACKETS
    IDPACKET_TELEMETRY_PULSE = 61
    IDPACKET_GPS_RAW = 62
    IDPACKET_RSSI = 63
    IDPACKET_VAISALA_WIND = 81
    IDPACKET_VAISALA_TPH = 82    
    IDPACKET_VAISALA_RAIN = 83 
    
    def __init__(self,):
        print('enable protocol')
        self.data = bytearray()
        self.packet_state = self.WAITING_START_PACKET
        self.packet_expected_length = 0
        self.total_bytes_received   = 0
        self.total_packets_received = 0
        self.total_msg_received     = 0
        
    def bytes_needed(self):
        '''return number of bytes needed for next parsing stage'''
        if self.packet_state == self.WAITING_START_PACKET:
            return 1
        
        elif self.packet_state == self.WAITING_HEADER:
            return self.packet_expected_length-self.total_bytes_received
        
        elif self.packet_state == self.WAITING_BODY:
            return self.packet_expected_length-self.total_bytes_received
        
        else:
            return 0
        
        
    def parse_packet(self, c):
        '''input some data bytes, possibly returning a new raw package'''
        if self.packet_state == self.WAITING_START_PACKET:
            if c==self.START_PACKET:
                self.packet_expected_length = self.HEADERSIZE
                self.total_bytes_received = 1
                self.data = bytearray(c)
                self.packet_state = self.WAITING_HEADER
                #print('llego Magic packet')
                
        elif self.packet_state == self.WAITING_HEADER:
            self.data.extend(c)
            self.total_bytes_received += len(c)
            #print(self.total_bytes_received)
            if self.total_bytes_received >=self.HEADERSIZE:
                #cuantos datos necesito:
                self.packet_expected_length = self.data[self.LEN_PACKET_POS]
                
                self.packet_state = self.WAITING_BODY
                #print('llego Header')
                
        elif self.packet_state == self.WAITING_BODY:
            self.data.extend(c)
            self.total_bytes_received += len(c)
            
            if self.total_bytes_received >=self.packet_expected_length:
                self.total_packets_received += 1
                
                self.packet_state = self.WAITING_START_PACKET
                
                return  self.data[self.FROM_PACKET_POS], self.data[0:self.packet_expected_length]
            
        return None, None
        
        
    def parse_msg(self, raw_pack):
        '''input complete pack, possibly returning a new msg'''
        msg = {}
        msg['FROM']  = raw_pack[self.FROM_PACKET_POS]
        msg['msgId'] = raw_pack[self.ID_PACKET_POS]
        msg['seq']   = raw_pack[self.SEQ_PACKET_POS]
        
        #calcular el CRC
        crc_packet = raw_pack[-2:] #los ultimos dos
        
        crc_calc = x25crc(raw_pack[0:-2]) #el crc de todo menos los dos ultimos
        
        
        if not crc_calc.check(crc_packet[-1],crc_packet[-2]):
            msg['crc'] = False
            msg['data'] = raw_pack
        
        else:
            msg['crc'] = True
            
            if msg['msgId']==self.IDPACKET_TELEMETRY_PULSE:
                msg.update(parse_telemetry_pulse(raw_pack))
                self.total_msg_received += 1
            elif msg['msgId']==self.IDPACKET_GPS_RAW:
                msg.update(parse_gps_raw(raw_pack))
                self.total_msg_received += 1
            elif msg['msgId']==self.IDPACKET_VAISALA_WIND:
                msg.update(parse_vaisala_wind(raw_pack))
                self.total_msg_received += 1
            elif msg['msgId']==self.IDPACKET_VAISALA_TPH:
                msg.update(parse_vaisala_tph(raw_pack))
                self.total_msg_received += 1
            elif msg['msgId']==self.IDPACKET_VAISALA_RAIN:
                msg.update(parse_vaisala_rain(raw_pack))
                self.total_msg_received += 1
            else:
                msg['msg_name']='None'
        
        return msg
        
    def get_json(self,msg):
        return json.dumps(msg)
    


def parse_telemetry_pulse(packet):
    msg = {}
    msg['timestamp']   = (packet[5] <<24) + (packet[6] <<16)+(packet[7] <<8)+packet[8]
    
    year     = (packet[9] >>2)+2000 
    month  = ((packet[9] & 3) <<2)+(packet[10] >>6) # 3: 00000011
    day      = (packet[10] & 62) >>1  # 62: 00111110
    hour     = ((packet[10] & 1) <<4)+(packet[11]>>4) # 1: 00000011
    minute = ((packet[11] & 15) <<2)+(packet[12] >>6) #15: 00001111
    second = (packet[12] & 63) #63: 00111111
    
    try:
        msg['gps_time']=datetime(year, month, day, hour, minute, second, tzinfo=UTC)
    except:
        msg['gps_time']= datetime(2000, 1, 1, 0, 0, 0, tzinfo=UTC)
    
    #estos valores tienen signo: Two's complement value: https://en.wikipedia.org/wiki/2%27s_complement
    
    if ((packet[13]>>7) > 0): #es negativo:
        msg['latitude']   =(((packet[13]&127) <<24) +(packet[14] <<16) +(packet[15]<<8) +packet[16])-4294967295 
    else:
        msg['latitude']   = (packet[13] <<24) +(packet[14] <<16) +(packet[15]<<8) +packet[16]
        
    if ((packet[17]>>7) > 0):#127: 01111111
        msg['longitude']   = (((packet[17]) <<24) +(packet[18] <<16) +(packet[19]<<8) +packet[20]) -4294967295 
    else:
        msg['longitude']  =(packet[17] <<24) +(packet[18] <<16) +(packet[19]<<8) +packet[20]
    
    msg['altitude'] =(packet[21] <<2) + (packet[22] >>6)
    msg['pressure']=((packet[22] & 63)<<8)+packet[23] #63: 00111111
    
    msg['acc_avg'] =[packet[24],packet[25],packet[26]]
    msg['gyr_avg'] =[packet[27],packet[28],packet[29]]
    
    msg['voltage'] = (packet[30] <<5) + (packet[31] >>3) #248: 11111000
    msg['current'] = ((packet[31] & 7) <<16)+(packet[32] <<8) +packet[33] #7:   00000111
    
    temp_int = ((packet[34] <<2) + (packet[35] >>6) -512) /10
    temp_air = (((packet[35]&63)<<5) +(packet[36]>>3) -512) /10 #63: 00111111
    temp_water = ((  ((packet[36] & 7)<<8)+(packet[37])  )-512)/10 #7:   00000111
    msg['temperature'] = [temp_int,temp_air,temp_water]
    
    msg['light'] =[packet[38], packet[39] ]
    strobe_R = (packet[40] & 192) >>6 #192: 11000000
    strobe_G = (packet[40] & 48) >>4  #48 : 00110000
    strobe_B = (packet[40] & 12) >>2  #12 : 00001100
    
    msg['strobe'] =[strobe_R,strobe_G,strobe_B] #RGB
    msg['status'] = (packet[40] & 3) # 3: 00000011
    
    return msg

def parse_gps_raw(packet):
    msg = {}
    
    return msg

def parse_vaisala_wind(packet):
    msg = {}
    
    return msg

def parse_vaisala_tph(packet):
    msg = {}
    
    return msg

def parse_vaisala_rain(packet):
    msg = {}
    
    return msg
    
