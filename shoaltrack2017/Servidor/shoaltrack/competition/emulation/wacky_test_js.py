#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Programa para la generacion de datos de testeo de la aplicacion ShoalTrack
# Copyright (C) 2016  CETMAR
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
# Email   : igonzalez@cetmar.org, ecounago@cetmar.org
# Web-Site: http://utmar.cetmar.org/ 

import time,os
from configobj import ConfigObj
from datetime import datetime
import numpy as np
import math
from pyproj import Proj
import json

def point_utm_to_wgs84(point_utm,epsg=32629):
    '''point = (geo_utmX,geo_utmY)
       epsg: from UTM 29T
       output: lon,lat en WGS84 'epsg:4326'
    '''
    #selecciona la proyeccion UTM:
    p_utm = Proj(init='epsg:'+str(epsg)) # para las conversiones
    WGS84_lon,WGS84_lat =p_utm(point_utm[0],point_utm[1],inverse=True) #(x,y)
    
    return (WGS84_lon,WGS84_lat)


class HIL_Race():
    '''
    Clase para la simulacion de una carrera virutual
    '''
    def __init__(self,config):
        self.config = config
        self.log_pathdir = '/mnt/ramdisk/shoaltrack/services/json'
        
        self.time_start=datetime.utcnow()
        
        
        self.marks_set = set()
        self.devices_set = set()
        self.fixed_marks_set =set()
        
        self.node={}
        self.trackings ={}
        self.calibrations ={}
        self.datas ={}
    
    
        print('marcas de boyas:')
        for item in settings['buoy_order']:
            self.node[self.config['devices'][item]['telemetry_code']] = HIL_Device(self.config['devices'][item]) # el dispositivo completo
            self.marks_set.add(self.config['devices'][item]['telemetry_code']) # su clasificador
            self.datas[self.config['devices'][item]['telemetry_code']]=[]#su gestion de datos
        
        print(self.marks_set)
            
        
        print('barcos participantes:')
        for item in settings['ship_order']:
            self.node[self.config['devices'][item]['telemetry_code']] = HIL_Device(self.config['devices'][item])  # el dispositivo completo
            self.devices_set.add(self.config['devices'][item]['telemetry_code']) # su clasificador
            self.datas[self.config['devices'][item]['telemetry_code']]=[]#su gestion de datos
            
        print(self.devices_set)
        
        #creo el directorio de trabajo si no existe:
        if not os.path.exists(self.log_pathdir):
            os.makedirs(self.log_pathdir)
            
    def update(self):
        for key in self.node.keys():
            self.node[key].update()
            self.datas[key].append(self.node[key].get_packet('dict'))
        
        time.sleep(0.1)
            
    def write_log(self,):
        '''
        Escribo en un archivo los utlimos datos
        '''
        #calculo el tiempo  desde el inicio en segundos que voy a mostrar:
        timeDataNow = datetime.utcnow()
        seconds_from_start = (timeDataNow-self.time_start).seconds
        
        
        ########################
        out_js = {}
        out_js['raceDate'] = '{:%d/%m/%Y %H:%M:%S}'.format(self.time_start)
        out_js['raceName'] = self.config['race']['raceName']
        out_js['time'] = seconds_from_start
        out_js['status'] =self.config['race']['status']
        
        out_js['startLine'] = [[float(self.config['race']['start_pt_1'][0]),float(self.config['race']['start_pt_1'][1])],
                               [float(self.config['race']['start_pt_2'][0]),float(self.config['race']['start_pt_2'][1])]]
        out_js['finishLine'] =[[float(self.config['race']['end_pt_1'][0]),float(self.config['race']['end_pt_1'][1])],
                               [float(self.config['race']['end_pt_2'][0]),float(self.config['race']['end_pt_2'][1])]]
        
        out_js['barcos'] = []
        out_js['boyas'] = []
        
        for key in self.node.keys():
            lastdata =self.datas[key][-1] #este es el ultimo
            #gestion de las marcas:
            if key in self.marks_set:
                mark = {}
                mark['nombre'] = self.node[key].config['nombre']
                mark['tipo'] = self.node[key].config['tipo']
                mark['localizacion'] = [lastdata['latitude_raw'],lastdata['longitude_raw']] 
                
                out_js['boyas'].append(mark)
            
            #gestion de los vehiculos:
            elif key in self.devices_set:
                dev = {}
                dev['nombre'] = self.node[key].config['nombre']
                dev['tipo'] = self.node[key].config['tipo']
                dev['color'] = '#'+self.node[key].config['color']
                dev['nombreColor'] = self.node[key].config['nombreColor']
                
                dev['localizacion'] = [lastdata['latitude_raw'],lastdata['longitude_raw']] 
                
                dev['posicion'] = lastdata['ranking']
                power = lastdata['power_volt']*lastdata['power_amp']
                dev['power'] =power
                
                dev['velocidad'] =lastdata['velocity']
                dev['direccion'] =lastdata['direction']
                
                out_js['barcos'].append(dev)
        
        out_js['windDirection'] = lastdata['direction']
        out_js['windIntensity'] = lastdata['velocity']
        
        with open(self.log_pathdir+'/last_data.json', 'w') as outfile:
            json.dump(out_js, outfile)
        
        ######################## el sistema de variables
        out_js = {}
        out_js['time'] = seconds_from_start
        out_js['variables'] = ['power','velocidad','direccion','accX',
                               'accY','accZ','temp_int','temp_air','temp_water',
                               'ldr_fr','ldr_fl','ldr_br','ldr_bl',
                               'power_volt','power_amp']
        
        out_js['barcos'] = []
        for key in self.devices_set:
            lastdata =self.datas[key][-1] #este es el ultimo
            dev = {}
            dev['nombre'] = self.node[key].config['nombre']
            dev['color'] = '#'+self.node[key].config['color']
            dev['posicion'] = lastdata['ranking']
            power = lastdata['power_volt']*lastdata['power_amp']
            dev['power'] =power
            dev['velocidad'] =lastdata['velocity']
            dev['direccion'] =lastdata['direction']
            
            dev['accX'] =lastdata['accX_raw']
            dev['accY'] =lastdata['accY_raw']
            dev['accZ'] =lastdata['accZ_raw']
            
            dev['temp_int'] =lastdata['temp_int_raw']
            dev['temp_air'] =lastdata['temp_air_raw']
            dev['temp_water'] =lastdata['temp_water_raw']
            dev['ldr_fr'] =lastdata['ldr_fr_raw']
            dev['ldr_fl'] =lastdata['ldr_fl_raw']
            dev['ldr_br'] =lastdata['ldr_br_raw']
            dev['ldr_bl'] =lastdata['ldr_bl_raw']
            
            dev['power_volt'] =lastdata['power_volt']
            dev['power_amp'] =lastdata['power_amp']
            
            
            out_js['barcos'].append(dev)
            
        
        with open(self.log_pathdir+'/last_variables.json', 'w') as outfile:
            json.dump(out_js, outfile)
        

class HIL_Device():
    '''
    Clase para la simulacion de un dispositivo virutual
    '''
    def __init__(self,config):
        self.config = config
        
        self.time_start=datetime.utcnow()
        
        self.ldr = [0,0,0,0]
        self.temp_water=1900
        self.temp_air=2400
        self.temp_int=4000
        self.accx= 0
        self.accy= 0
        self.accz= 0
        self.gyrx= 0
        self.gyry= 0
        self.gyrz= 0
        self.magx= 0
        self.magy= 0
        self.magz = 0
        self.voltage=0
        self.ampere=0
        
        self.ref_air_temp = 24.000
        self.ref_pressure = 1024.0
        self.ref_humidity_relative = 1024.0
        self.ref_wind_module = 1.0
        self.ref_wind_direction = 0
        
        self.ranking = 0
        self.velocity = 0
        self.direction = 0
        
        self.time_now=datetime.utcnow()
        self.millisecond = 0
        self.position=(float(self.config['track']['start']['utmx']),
                               float(self.config['track']['start']['utmy']))
        
        self.target_position=(float(self.config['track']['interm_1']['utmx']),
                                          float(self.config['track']['interm_1']['utmy']))
        
        self.target_count=0
    

    def calc_ligth_intense(self):
        points =(0,10,20,30,40,60,80,100,150,1023)
        coef =(0.05, 0.05,0.1, 0.1,0.2,0.28,0.15,0.05,0.01,0.01)
        ldr = np.random.choice(points,4, p=coef)
        
        count=0
        for item in ldr:
            if item == points[0]:
                data_low = points[0]
                data_high=points[1]
                
            elif item == points[1]:
                data_low = points[1]
                data_high=points[2]
            elif item == points[2]:
                data_low = points[2]
                data_high=points[3]
            elif item == points[3]:
                data_low = points[3]
                data_high=points[4] 
            elif item == points[4]:
                data_low = points[4]
                data_high=points[5] 
            elif item == points[5]:
                data_low = points[5]
                data_high=points[6] 
            elif item == points[7]:
                data_low = points[7]
                data_high=points[8] 
            else:
                data_low = points[0]
                data_high=points[-1]
                
            raw_data = np.random.random_integers(data_low,data_high)    
            self.ldr[count]=raw_data
            count +=1
            
    def get_next_target(self):
        try:
            self.target_count += 1
            track_item = self.config['track']['track_order'][self.target_count]
            target_position=(float(self.config['track']['track_item']['utmx']),
                             float(self.config['track']['track_item']['utmy']))
            
            self.ranking +=10000.0 #cuado paso por una boya, sumo una cantidd grande
            
        except:
            self.target_count = 0
            target_position=(float(self.config['track']['end']['utmx']),
                                              float(self.config['track']['end']['utmy']))
        return target_position
        

    def calc_power_measure(self, ligth_values):
        mean_lum = (ligth_values[0]+ligth_values[1]+ligth_values[2]+ligth_values[3])/4
        #funcion exponecial de luminosidad/potencia: f(x)=102.583*exp(-0.004033012433 X)
        teorical_power =102.583*math.exp(-0.004033012433*mean_lum)
        self.voltage = 23+(2*np.random.random())
        self.ampere = teorical_power/self.voltage
        
        #correccion a enteros de 0-5 voltios:
        self.voltage = int((self.voltage *0.208333)*204.6) 
        self.ampere = int((2.5 +self.ampere *0.125)*204.6)
        
        
        
        
    def calc_temp_water(self):
        '''Da una salida de temperatura que no difietre mucho dela anterior... estabilidad aleatoria
        '''
        points =(1400 ,1500 ,1600 ,1700 ,1800)
        coef   =(0.05, 0.25, 0.4, 0.25, 0.05)
        new = np.random.choice(points, p=coef)
        
        new =new+ np.random.random()
        
        self.temp_water=int((self.temp_water*3+new)/4)
        

    def calc_temp_air(self):
        '''Da una salida de temperatura que no difietre mucho dela anterior... estabilidad aleatoria
        '''
        points =(1900 ,2000 ,2100 ,2200 ,2300)
        coef   =(0.05, 0.25, 0.4, 0.25, 0.05)
        new = np.random.choice(points, p=coef)
        
        new =new+ np.random.random()
        
        self.temp_air=int((self.temp_air*3+new)/4)
        

    def calc_temp_int(self):
        '''Da una salida de temperatura que no difietre mucho dela anterior... estabilidad aleatoria
        '''
        points =(3500 ,2600 ,3700 ,3800 ,3900)
        coef   =(0.05, 0.25, 0.4, 0.25, 0.05)
        new = np.random.choice(points, p=coef)
        
        new =new+ np.random.random()
        
        self.temp_int=int((self.temp_int*3+new)/4)
        

    def calc_imu(self):
        factor =(0 ,1 ,2 ,3 )
        coef   =(0.5, 0.35, 0.1, 0.05)
        
        new_factor = np.random.choice(factor, p=coef)
        new =int(new_factor*100*np.random.random())
        self.accx=(self.accx+new)//2
        self.gyrx=new-self.accx
        
        new_factor = np.random.choice(factor, p=coef)
        new =int(new_factor*100*np.random.random())
        self.accy=(self.accy+new)//2
        self.gyry=new-self.accy
        
        new_factor = np.random.choice(factor, p=coef)
        new =int(new_factor*100*np.random.random())
        self.accz=(self.accz+new)//2
        self.gyrz=new-self.accz
        
        
        new_factor = np.random.choice(factor, p=coef)
        new =int(new_factor*100*np.random.random())
        self.magx=(self.magx+new)//2
        
        new_factor = np.random.choice(factor, p=coef)
        new =int(new_factor*100*np.random.random())
        self.magy=(self.magy+new)//2
        
        new_factor = np.random.choice(factor, p=coef)
        new =int(new_factor*100*np.random.random())
        self.magz=(self.magz+new)//2
        
        
    def calc_next_position(self):
        '''velocidad en funciona de la potencia consumida:
        f(x)=1,3858828045 * ln(x) + 0,06210221636
        '''
        new_time= datetime.utcnow()
        
        self.velocity = (1.3858828045*math.log(self.ampere)) + 0.06210221636
        
        time_dt = (self.time_now-new_time).seconds
        meter=self.velocity/time_dt
        #print(time_dt)
        #print(meter)
        #print(velocity)
        
        desp_x =np.random.random()
        desp_y = 1-desp_x
        
        dist_x=self.target_position[0]-self.position[0]
        self.ranking +=dist_x #a medida que me acerco a la boya, sumo puntos
        dist_y=self.target_position[1]-self.position[1]
        
        new_pos=[self.position[0],self.position[1]]
        if dist_x>0:
            new_pos[0] += desp_x
        else:
            new_pos[0] -= desp_x
        
        if dist_y>0:
            new_pos[1] += desp_y
        else:
            new_pos[1] -= desp_y
        
        self.time_now = new_time
        self.position = new_pos
        
        if dist_x < 0.25 and dist_y < 0.25:
            self.target_position = self.get_next_target()
            
        self.direction = int(((self.direction*2)+np.random.random_integers(0,359))/3)
            
    def get_gps(self,):
        
        return point_utm_to_wgs84(self.position)
    

    def update(self,param='all'):
        if param in ['all','start','ligth']:
            self.calc_ligth_intense()
        if param in ['all','start','power']:
            self.calc_power_measure(self.ldr)
        if param in ['all','start','temp']:
            self.calc_temp_water()
            self.calc_temp_air()
            self.calc_temp_int()
        if param in ['all','start','imu']:
            self.calc_imu()
        if param in ['all','move','position']:
            self.calc_next_position()
            
        #calculo nuevo timemilisec:
        new_time= datetime.utcnow()
        self.millisecond = int((new_time-self.time_start).total_seconds() * 1000)
        
        
    
        
    def get_packet(self,formato='NMEA'):
        if (formato=='dict'):
            datapack = {}
            gps = self.get_gps()
            #datapack['geom'] = 
            datapack['millisecons'] = self.millisecond
            datapack['longitude_raw'] =gps[0]
            datapack['latitude_raw'] = gps[1]
            datapack['timestamp_gps'] = datetime.utcnow()
            
            datapack['accX_raw'] = self.accx
            datapack['accX_coef'] =None
            datapack['accY_raw'] = self.accy
            datapack['accY_coef'] =None
            datapack['accZ_raw'] = self.accz
            datapack['accZ_coef'] =None
            datapack['gyrX_raw'] = self.gyrx
            datapack['gyrX_coef'] =None
            datapack['gyrY_raw'] = self.gyry
            datapack['gyrY_coef'] =None
            datapack['gyrZ_raw'] = self.gyrz
            datapack['gyrZ_coef'] =None
            datapack['magX_raw'] = self.magx
            datapack['magX_coef'] =None
            datapack['magY_raw'] = self.magy
            datapack['magY_coef'] =None 
            datapack['magZ_raw'] = self.magz
            datapack['magZ_coef'] =None
            
            datapack['press_air_raw'] = 1045.0
            datapack['press_air_coef'] =None
            datapack['temp_int_raw'] = self.temp_int
            datapack['temp_int_coef'] =None
            datapack['temp_air_raw'] = self.temp_air
            datapack['temp_air_coef'] =None
            datapack['temp_water_raw'] = self.temp_water
            datapack['temp_water_coef'] =None
            
            datapack['ldr_fr_raw'] = int(self.ldr[0])
            datapack['ldr_fr_coef'] =None
            datapack['ldr_fl_raw'] = int(self.ldr[1])
            datapack['ldr_fl_coef'] =None
            datapack['ldr_br_raw'] = int(self.ldr[2])
            datapack['ldr_br_coef'] =None
            datapack['ldr_bl_raw'] = int(self.ldr[3])
            datapack['ldr_bl_coef'] =None
            
            datapack['power_volt'] = self.voltage
            datapack['power_volt_coef'] =None
            datapack['power_amp'] = self.ampere
            datapack['power_amp_coef'] =None
            
            datapack['ref_air_temp'] = self.temp_air/100.0
            datapack['ref_pressure'] = datapack['press_air_raw']
            datapack['ref_humidity_relative'] = 56.7
            datapack['ref_wind_module'] = self.velocity
            datapack['ref_wind_direction'] =self.direction
            
            datapack['ranking'] = self.ranking
            datapack['velocity'] = self.velocity
            datapack['direction'] =self.direction
            
        else:
            datapack= ('#'+self.config['telemetry_code']+','+str(self.millisecond)+','+str(self.get_gps())+
                  ','+str(self.voltage)+','+str(self.ampere)+','+str(self.accx)+','+str(self.accy)+
                  ','+str(self.accz)+','+str(self.gyrx)+','+str(self.gyry)+','+str(self.gyrz)+','+
                  str(self.magx)+','+str(self.magy)+','+str(self.magz)+','+str(self.temp_water)+','+str(self.temp_air)+','+str(self.temp_int)+','+str(self.ldr))
        return datapack
    
    
    

####################################
#programa central
if __name__ == "__main__":
    
    settings = ConfigObj('settings.conf', encoding="ISO-8859-1")
    #print(settings)
    
    race = HIL_Race(settings)
    count = 0
    while True:
        try:
            count +=1
            race.update()
            race.write_log()
            print('Second: '+str(count))
            time.sleep(1)
        except KeyboardInterrupt:
            break
    
    
