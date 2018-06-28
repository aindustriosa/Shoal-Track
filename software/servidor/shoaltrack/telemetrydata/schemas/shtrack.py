#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''Definicion de los schemas de los protocolos de datos para la adquisicion y parseo de los packetes
'''
from datetime import datetime
from django.utils import timezone
from pytz import UTC
from pyproj import Proj

def text_schema():
    schema ={'name':'debug',
             'Id_packet':[0,'#DEBUG']
            }
    return schema

def text_parse(datum):
    '''#DEBUG,[ComLinkRF], Request to: 2
    '''
    data_dict = {}
    data_dict['Id_packet'] = 0
    
    data_dict['label'] = datum[0][1:]
    data_dict['module'] = datum[1][1:-1]
    data_dict['information'] = datum[2]
    
    return data_dict
    
def gpstime_schema():
    schema ={'name':'gpstime',
             'Id_packet':[1,'5']
            }
    return schema

def gpstime_parse(datum):
    '''
    $GTWN01,5,422278758,-87514065,17,6,7,12,52,19,00
    '''
    
    data_dict = {}
    
    data_dict['Id_Code'] = datum[0][1:]
    data_dict['Id_packet'] = int(datum[1])
    wgs84_latitude = float(datum[2][:2] + '.' + datum[2][2:])
    wgs84_longitude =float(datum[3][:2] + '.' + datum[3][2:])
     
    p_utm = Proj(init='epsg:32629')
    data_dict['gps_longitude'],data_dict['gps_latitude'] =p_utm(wgs84_longitude,wgs84_latitude)
 
    
    year = int(datum[4])+2000
    month = int(datum[5])
    day = int(datum[6])
    hour = int(datum[7])
    minute = int(datum[8])
    second = int(datum[9])
    try:
        data_dict['timestamp_gps']=datetime(year, month, day, hour, minute, second, tzinfo=UTC)
    except:
        data_dict['timestamp_gps']= timezone.now()
    
    data_dict['timestamp']= timezone.now()
    
    
    return data_dict

def vaisala_schema():
    schema ={'name':'vaisala',
             'Id_packet':[1,'6']
            }
    return schema

def vaisala_parse(datum):
    '''
    $GTWN01,6,Dn=211D,Dm=227D,Dx=240D,Sn=0.6M,Sm=1.1M,Sx=1.2M,00
    $GTWN01,6,Ta=27.0C,Ua=48.3P,Pa=1015.3H,00
    $GTWN01,6,Rc=0.0M,Rd=0s,Ri=0.0M,Hc=0.0M,Hd=0s,Hi=0.0M,Rp=0.0M,
Hp=0.0M,00
    '''
    data_dict = {}
    
    data_dict['Id_Code'] = datum[0][1:]
    data_dict['Id_packet'] = int(datum[1])
    data_dict['timestamp']= timezone.now()
    
    if  datum[2][:2] == 'Dn': #datos de viento
        
        data_dict['Wind_dir min'] = int(datum[2][3:-1]) #Deg
        data_dict['Wind_dir_avg'] = int(datum[3][3:-1]) #Deg
        data_dict['Wind_dir_max'] = int(datum[4][3:-1]) #Deg
    
        data_dict['Wind_spd_min'] = float(datum[5][3:-1]) #m/s
        data_dict['Wind_spd_avg'] = float(datum[6][3:-1]) #m/s
        data_dict['Wind_spd_max'] = float(datum[7][3:-1]) #m/s
    
    elif datum[2][:2] == 'Ta': #datos de temperatura y humedad y presion
        data_dict['Air_temp'] = float(datum[2][3:-1])     #ºC
        data_dict['Rel_humidity'] = float(datum[3][3:-1]) #%
        data_dict['Air_press'] = float(datum[4][3:-1])    #hPa
        
    elif datum[2][:2] == 'Rc': #datos de lluvia
        data_dict['Rain_accumulation'] = float(datum[2][3:-1]) #mm
        data_dict['Rain_duration'] = int(datum[3][3:-1])     #seg
        data_dict['Rain_intensity'] = float(datum[4][3:-1])         #mm/h
        data_dict['Hail_accumulation'] = float(datum[5][3:-1])         #hits/cm2h
        data_dict['Hail_duration'] = int(datum[6][3:-1])         #seg
        data_dict['Hail_intensity'] = float(datum[7][3:-1])         #hits/cm2h
        data_dict['Rain_peak_intensity'] = float(datum[8][3:-1])         #mm/h
        data_dict['Hail_peak_intensity'] = float(datum[9][3:-1])         #hits/cm2h
    
    else: #no conozco esta trama
        return None
        
    return data_dict


    
def race_solar_mi_2_schema():
    schema ={'name':'rsmi2',
             'Id_packet':[1,'15']
            }
    return schema

def race_solar_mi_2_parse(datum):
    '''
    $ASRS08,15,361289,0,422272957,-87522208,17,6,7,12,52,19,-134,-238,3910,16,4,10,-44,232,555,-452,0,511,2762,3006,2781,704,31,605,958,00
    
    $RMRK02,15,1366052,0,422272300,-87522450,17,6,7,12,52,13,-372,-38,3982,-24,2,-9,-81,392,-87,-290,0,510,-12700,-12700,-12700,224,108,131,148,00

    '''
    data_dict = {}
    
    data_dict['Id_Code'] = datum[0][1:]
    data_dict['Id_packet'] = int(datum[1])
    data_dict['timestamp']= timezone.now()
    data_dict['timestamp_ms'] = int(datum[2])
    data_dict['timestamp_cycle'] = int(datum[3])
    
    wgs84_latitude = float(datum[4][:2] + '.' + datum[4][2:])
    wgs84_longitude =float(datum[5][:2] + '.' + datum[5][2:])
     
    p_utm = Proj(init='epsg:32629')
    data_dict['gps_longitude'],data_dict['gps_latitude'] =p_utm(wgs84_longitude,wgs84_latitude)
    
    
    year = int(datum[6])+2000
    month = int(datum[7])
    day = int(datum[8])
    hour = int(datum[9])
    minute = int(datum[10])
    second = int(datum[11])
    try:
        data_dict['timestamp_gps']=datetime(year, month, day, hour, minute, second, tzinfo=UTC)
    except:
        data_dict['timestamp_gps']= timezone.now()
    
    data_dict['accx'] = int(datum[12])
    data_dict['accy'] = int(datum[13])
    data_dict['accz'] = int(datum[14])
    
    data_dict['gyrx'] = int(datum[15])
    data_dict['gyry'] = int(datum[16])
    data_dict['gyrz'] = int(datum[17])
    
    data_dict['magx'] = int(datum[18])
    data_dict['magy'] = int(datum[19])
    data_dict['magz'] = int(datum[20])
    
    data_dict['pressure'] = int(datum[21])
    
    data_dict['voltage'] = int(datum[22])
    data_dict['current'] = int(datum[23])
    
    data_dict['temp_int'] = int(datum[24])
    data_dict['temp_air'] = int(datum[25])
    data_dict['temp_water'] = int(datum[26])
    
    data_dict['ldr_fr'] = int(datum[27])
    data_dict['ldr_fl'] = int(datum[28])
    data_dict['ldr_br'] = int(datum[29])
    data_dict['ldr_bl'] = int(datum[30])
    
    
    return data_dict


    
