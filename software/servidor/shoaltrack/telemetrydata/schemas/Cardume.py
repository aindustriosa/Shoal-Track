 #!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Protocolo de trasmision de datos Cardume
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
# Email   : igonzalez@cetmar.org
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
        



class CardumeProtocol():
    '''
    Clase para la gestion del protocolo de ShoalTrack
    '''
    HEADERSIZE = 8
    
    START_PACKET_OPEN = b'\x40' #el @
    START_PACKET_CYPHER = b'\x23' #el #
    
    START_PACKET_POS = 0
    LEN_PACKET_POS   = 1
    FROM_PACKET_POS  = 2
    TO_PACKET_POS  = 3
    TIMEMARK_PACKET_POS  = 4
    MSG_PACKET_POS  = 8
    
    #STATUS PACKET DECODE
    WAITING_START_PACKET = 1
    WAITING_HEADER       = 2
    WAITING_BODY         = 3
    COMPLETE_RAW_PACKET  = 4
    ERROR_SIZE           = 4
    FINISH_OK            = 0
    
    #ID PACKETS
    CARDUME_ID_HEARTBEAT      = 0x30
    CARDUME_ID_TRACEROUTE    = 0x40
    CARDUME_ID_ACKREPORT      = 0x41
    CARDUME_ID_SENDORDEN    = 0x42
    
    CARDUME_ID_SHOALTRACK   = 0x81
    CARDUME_ID_METEOWIND    = 0x82
    CARDUME_ID_METEOTHP       = 0x83
    CARDUME_ID_METEORAIN     = 0x84
    
    IDPACKET_TELEMETRY_PULSE = 61
    IDPACKET_GPS_RAW = 62
    IDPACKET_RSSI = 63
    IDPACKET_VAISALA_WIND = 81
    IDPACKET_VAISALA_TPH = 82    
    IDPACKET_VAISALA_RAIN = 83
    
    CARDUME_SHOALTRACK_LEN   = 40
    CARDUME_METEOWIND_LEN    = 13
    CARDUME_METEOTHP_LEN       = 7
    CARDUME_METEORAIN_LEN     = 17
    
    def __init__(self,):
        print('Enable Cardume protocol...')
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
            if ((c==self.START_PACKET_OPEN) or
                 (c==self.START_PACKET_CYPHER)):
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
        
    
    def parse_header(self, raw_pack):
        '''decode the header packet'''
        header = {}
        if (bytes([raw_pack[0]]) == self.START_PACKET_OPEN):
            header['isCypher']=False;
        else:
            header['isCypher']=True;
            
        header['length'] = raw_pack[self.LEN_PACKET_POS]
        header['FROM']  = raw_pack[self.FROM_PACKET_POS]
        header['TO']  = raw_pack[self.TO_PACKET_POS]
        if (header['FROM'] == 201):
            header['Id_Code']  ='GTWN01'
        else:
            header['Id_Code']  ='ASRS'+str(header['FROM'])
    
        year     = (raw_pack[self.TIMEMARK_PACKET_POS+3]>>2)+2000 
        month  = ((raw_pack[self.TIMEMARK_PACKET_POS+3] & 0x03) <<2)+(raw_pack[self.TIMEMARK_PACKET_POS+2] >>6) # 3: 00000011
        day      = (raw_pack[self.TIMEMARK_PACKET_POS+2] & 62) >>1  # 62: 00111110
        hour     = ((raw_pack[self.TIMEMARK_PACKET_POS+2] & 1) <<4)+(raw_pack[self.TIMEMARK_PACKET_POS+1]>>4) # 1: 00000001
        minute = ((raw_pack[self.TIMEMARK_PACKET_POS+1] & 15) <<2)+(raw_pack[self.TIMEMARK_PACKET_POS] >>6) #15: 00001111
        second = (raw_pack[self.TIMEMARK_PACKET_POS] & 63) #63: 00111111
        
        #header['isCypher']=False;
        try:
            header['time_mark']=datetime(year, month, day, hour, minute, second, tzinfo=UTC)
        except:
            header['time_mark']= datetime(2000, 1, 1, 0, 0, 0, tzinfo=UTC)
        
        return header
    
    def parse_payload(self, msg,key=None):
        ''' Decodifica el payload de la trama si le proporcionas las keys'''
        payload={} #para ir metiendo los datos
        
        if msg['isCypher']:
            print('Pakete codificado..')
            #lo decodifico con la key
        
        #compruebo hash con su key, si la tiene:
        payload['HashCRC'] = 'No check'
        
        #decodifico:
        payload['msgID'] = msg['payload'][self.MSG_PACKET_POS]
        
        if payload['msgID'] ==self.CARDUME_ID_HEARTBEAT:
            payload.update(parse_heartbeat(msg['payload'][self.MSG_PACKET_POS:-4]))
            self.total_msg_received += 1
        elif payload['msgID'] ==self.CARDUME_ID_TRACEROUTE:
            payload.update(parse_traceroute(msg['payload'][self.MSG_PACKET_POS:-4]))
            self.total_msg_received += 1
        elif payload['msgID'] ==self.CARDUME_ID_SHOALTRACK:
            payload.update(parse_shoaltrack(msg['payload'][self.MSG_PACKET_POS:-4]))
            self.total_msg_received += 1
        elif payload['msgID'] ==self.CARDUME_ID_METEOWIND:
            payload.update(parse_meteowind(msg['payload'][self.MSG_PACKET_POS:-4]))
            self.total_msg_received += 1
        elif payload['msgID'] ==self.CARDUME_ID_METEOTHP:
            payload.update(parse_meteothp(msg['payload'][self.MSG_PACKET_POS:-4]))
            self.total_msg_received += 1
        elif payload['msgID'] ==self.CARDUME_ID_METEORAIN:
            payload.update(parse_meteorain(msg['payload'][self.MSG_PACKET_POS:-4]))
            self.total_msg_received += 1
        else:
            payload['raw_payload']=msg['payload']
            payload['Error']='unknown message'
        
        #deviuelvo el dict con el mensage decodificado:
        #añado si hubo problemas:
        return payload
    
        
    def get_json(self,msg):
        return json.dumps(msg)
    

def parse_heartbeat(packet):
    msg = {}
    
    return msg

def parse_traceroute(packet):
    msg = {}
    
    if (len(packet)== 16):
    
        msg['nextHop'] = packet[1]
        msg['rssi'] =int.from_bytes([packet[2]],
                                            byteorder='little',signed=True)  #-812345
        msg['gps_precision'] = packet[3]
    
        msg['gps_longitude'] = int.from_bytes([packet[4],packet[5],packet[6],packet[7]],
                                            byteorder='little',signed=True)  #-812345
        msg['gps_longitude'] = msg['gps_longitude']/10000000

        msg['gps_latitude'] = int.from_bytes([packet[8], packet[9], packet[10],packet[11]],
                                            byteorder='little',signed=True)  #-812345
        msg['gps_latitude'] = msg['gps_latitude']/10000000
        
        msg['gps_itow'] =int.from_bytes([packet[12], packet[13], packet[14],packet[15]],
                                            byteorder='little',signed=False)  #
    else:
        msg['Error']='length msg fail'
        
    return msg

def parse_shoaltrack(packet):
    msg = {}
    
    if (len(packet)== 40):
    
        msg['nextHop'] = packet[1]  #ok
        
        msg['gps_precision']=(packet[2] >>5) #ok
        
        msg['bearing_std']=(packet[2]&0x1f) #ok
        msg['bearing_avg']=packet[3]  #ok
        
        msg['gps_heading'] = packet[4]
        
        msg['acc_std_F']=packet[5]>>6 
        msg['accX_std_A']=(packet[5]&48)>>4 #48:00110000 
        msg['accY_std_A']=(packet[5]&12)>>2 #48:00001100 
        msg['accZ_std_A']=(packet[5]&3) #48:00000011 
        
        msg['gyr_std_F']=packet[6]>>6 
        msg['gyrX_std_A']=(packet[6]&48)>>4 #48:00110000 
        msg['gyrY_std_A']=(packet[6]&12)>>2 #48:00001100 
        msg['gyrZ_std_A']=(packet[6]&3) #48:00000011 
        
        msg['voltage_batt_std_A']=packet[7]>>6 
        msg['amp_batt_std_A']=(packet[7]&48)>>4 #48:00110000 
        msg['pressure_std_A']=(packet[7]&12)>>2 #48:00001100 
        msg['ligth_std_A']=(packet[7]&3) #48:00000011 
        
        #print(bin(packet[2]))
        
        msg['voltage_batt_std_B']=packet[9]>>4
        msg['voltage_batt_avg']=((packet[9] & 15)<<8)+packet[8]  #15: 00001111
        msg['voltage_batt_std'] =  msg['voltage_batt_std_A']<<4 +msg['voltage_batt_std_B']
        msg['voltage_batt_std'] =  (msg['voltage_batt_std'] *1023) /63
        #Otra manera de hacerlo:
        #msg['voltage_batt_avg2']=int.from_bytes([(packet[9]&0x0f),packet[8]],
        #                                                                 byteorder='big')
        
        msg['amp_batt_std_B']=packet[11]>>4
        if (packet[11] & 8): #8: 00001000 Si es negativo, pongo todos los 0 a negativos:
            packet[11]  |= 240
        else:
            packet[11] &= 15 #si no, los quito
        msg['amp_batt_avg'] = int.from_bytes([packet[11], packet[10]],
                                                                            byteorder='big',signed=True) 
        msg['amp_batt_std'] =  (msg['amp_batt_std_A']<<4) +msg['amp_batt_std_B']
        msg['amp_batt_std'] =  (msg['amp_batt_std'] *1023) /63

        msg['pressure_std_B']=packet[13]>>4
        msg['pressure_avg']=((packet[13] & 15)<<8)+packet[12] #15: 00001111
        msg['pressure_std'] =  (msg['pressure_std_A']<<4) +msg['pressure_std_B']
        msg['pressure_std'] =  (msg['pressure_std'] *1023) /63

        msg['ligth_std_B']=packet[15]>>4
        msg['ligth_avg']=((packet[15] & 15)<<8)+packet[14] #15: 00001111
        msg['ligth_std'] =  (msg['ligth_std_A']<<4) +msg['ligth_std_B']
        msg['ligth_std'] =  (msg['ligth_std'] *1023) /63
            
        
        msg['accX_std_B']=packet[17]>>4
        if (packet[17] & 8): #8: 00001000 Si es negativo, pongo todos los 0 a negativos:
            packet[17]  |= 240
        else:
            packet[17] &= 15 #si no, los quito
        msg['accX_avg'] = int.from_bytes([packet[17], packet[16]],
                                                                            byteorder='big',signed=True) 
        msg['accX_std'] =  (msg['accX_std_A']<<4) +msg['accX_std_B']
        msg['accX_std'] =  (msg['accX_std'] *1023) /63
        msg['accX_std'] = msg['accX_std']*(msg['acc_std_F']+1)
        
        msg['accY_std_B']=packet[19]>>4
        if (packet[19] & 8): #8: 00001000 Si es negativo, pongo todos los 0 a negativos:
            packet[19]  |= 240
        else:
            packet[19] &= 15 #si no, los quito
        msg['accY_avg'] = int.from_bytes([packet[19], packet[18]],
                                                                            byteorder='big',signed=True) 
        msg['accY_std'] =  (msg['accY_std_A']<<4) +msg['accY_std_B']
        msg['accY_std'] =  (msg['accY_std'] *1023) /63
        msg['accY_std'] = msg['accY_std']*(msg['acc_std_F']+1)
        
        msg['accZ_std_B']=packet[21]>>4
        if (packet[21] & 8): #8: 00001000 Si es negativo, pongo todos los 0 a negativos:
            packet[21]  |= 240
        else:
            packet[21] &= 15 #si no, los quito
        msg['accZ_avg'] = int.from_bytes([packet[21], packet[20]],
                                                                            byteorder='big',signed=True) 
        msg['accZ_std'] =  (msg['accZ_std_A']<<4) +msg['accZ_std_B']
        msg['accZ_std'] =  (msg['accZ_std'] *1023) /63
        msg['accZ_std'] = msg['accZ_std']*(msg['acc_std_F']+1)
        

        msg['gyrX_std_B']=packet[23]>>4
        if (packet[23] & 8): #8: 00001000 Si es negativo, pongo todos los 0 a negativos:
            packet[23]  |= 240
        else:
            packet[23] &= 15 #si no, los quito
        msg['gyrX_avg'] = int.from_bytes([packet[23], packet[22]],
                                                                            byteorder='big',signed=True) 
        msg['gyrX_std'] =  (msg['gyrX_std_A']<<4) +msg['gyrX_std_B']
        msg['gyrX_std'] =  (msg['gyrX_std'] *1023) /63
        msg['gyrX_std'] = msg['gyrX_std']*(msg['gyr_std_F']+1)
        
        msg['gyrY_std_B']=packet[25]>>4
        if (packet[25] & 8): #8: 00001000 Si es negativo, pongo todos los 0 a negativos:
            packet[25]  |= 240
        else:
            packet[25] &= 15 #si no, los quito
        msg['gyrY_avg'] = int.from_bytes([packet[25], packet[24]],
                                                                            byteorder='big',signed=True) 
        msg['gyrY_std'] =  msg['gyrY_std_A']<<4 +msg['gyrY_std_B']
        msg['gyrY_std'] =  (msg['gyrY_std'] *1023) /63
        msg['gyrY_std'] = msg['gyrY_std']*(msg['gyr_std_F']+1)
        
        msg['gyrZ_std_B']=packet[27]>>4
        if (packet[27] & 8): #8: 00001000 Si es negativo, pongo todos los 0 a negativos:
            packet[27]  |= 240
        else:
            packet[27] &= 15 #si no, los quito
        msg['gyrZ_avg'] = int.from_bytes([packet[27], packet[26]],
                                                                            byteorder='big',signed=True) 
        msg['gyrZ_std'] =  (msg['gyrZ_std_A']<<4) +msg['gyrZ_std_B']
        msg['gyrZ_std'] =  (msg['gyrZ_std'] *1023) /63
        msg['gyrZ_std'] = msg['gyrZ_std']*(msg['gyr_std_F']+1)
        
        msg['gps_longitude'] = int.from_bytes([packet[28],packet[29],packet[30],packet[31]],
                                            byteorder='little',signed=True)  #-812345
        msg['gps_longitude'] = msg['gps_longitude']/10000000

        msg['gps_latitude'] = int.from_bytes([packet[32], packet[33], packet[34],packet[35]],
                                            byteorder='little',signed=True)  #-812345
        msg['gps_latitude'] = msg['gps_latitude']/10000000
        
        
        msg['gps_itow'] =int.from_bytes([packet[36], packet[37], packet[38],packet[39]],
                                            byteorder='little',signed=False)  #
    
    else:
        msg['Error']='length msg fail'
        
        
    return msg
    
def parse_meteowind(packet):
    msg = {}
    if (len(packet)== 14):
        msg['seconds']=packet[1]
        
        msg['wind_direction_min']=int.from_bytes([packet[2],packet[3]],
                                                                        byteorder='little') 
        msg['wind_direction_avg']=int.from_bytes([packet[4],packet[5]],
                                                                        byteorder='little') 
        msg['wind_direction_max']=int.from_bytes([packet[6],packet[7]],
                                                                        byteorder='little') 
        msg['wind_speed_min']=int.from_bytes([packet[8],packet[9]],
                                                                        byteorder='little')
        msg['wind_speed_min'] = msg['wind_speed_min']/100
        msg['wind_speed_avg']=int.from_bytes([packet[10],packet[11]],
                                                                        byteorder='little')
        msg['wind_speed_avg'] = msg['wind_speed_avg']/100
        msg['wind_speed_max']=int.from_bytes([packet[12],packet[13]],
                                                                        byteorder='little') 
        msg['wind_speed_max'] = msg['wind_speed_max']/100
        
    else:
        msg['Error']='length msg fail'
        
    return msg
    
def parse_meteothp(packet):
    msg = {}
    if (len(packet)== 8):
        msg['seconds']=packet[1]
        
        msg['air_temperature'] = int.from_bytes([packet[2],packet[3]],
                                                                        byteorder='little',signed=True)  #-812345
        msg['air_temperature'] = msg['air_temperature']/100
        msg['relative_humidity']=int.from_bytes([packet[4],packet[5]],
                                                                        byteorder='little')
        msg['relative_humidity'] = msg['relative_humidity']/100
        msg['air_pressure']=int.from_bytes([packet[6],packet[7]],
                                                                        byteorder='little') 
    
    else:
        msg['Error']='length msg fail'
        
    return msg
    
def parse_meteorain(packet):
    msg = {}
    
    if (len(packet)== 18):
        
        msg['seconds']=packet[1]
    
        msg['rain_accumulation']=(packet[2]<<8) +packet[3]
        msg['rain_duration']=(packet[4]<<8) +packet[5]
        msg['rain_intensity']=(packet[6]<<8) +packet[7]
        msg['hail_accumulation']=(packet[8]<<8) +packet[9]
        msg['hail_duration']=(packet[10]<<8) +packet[11]
        msg['hail_intensity']=(packet[12]<<8) +packet[13]
        msg['rain_peak_intensity']=(packet[14]<<8) +packet[15]
        msg['hail_peak_intensity']=(packet[16]<<8) +packet[17]
    else:
        msg['Error']='length msg fail'
    
    return msg
