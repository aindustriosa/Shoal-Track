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

def point_utm_to_wgs84(point_utm,epsg=32629):
    '''point = (geo_utmX,geo_utmY)
       epsg: from UTM 29T
       output: lon,lat en WGS84 'epsg:4326'
    '''
    #selecciona la proyeccion UTM:
    p_utm = Proj(init='epsg:'+str(epsg)) # para las conversiones
    WGS84_lon,WGS84_lat =p_utm(point_utm[0],point_utm[1],inverse=True) #(x,y)
    
    return (WGS84_lon,WGS84_lat)

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
        
        velocity = (1.3858828045*math.log(self.ampere)) + 0.06210221636
        
        time_dt = (self.time_now-new_time).seconds
        meter=velocity/time_dt
        #print(time_dt)
        #print(meter)
        #print(velocity)
        
        desp_x =np.random.random()
        desp_y = 1-desp_x
        
        dist_x=self.target_position[0]-self.position[0]
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
        
        
    
        
    def get_packet(self):
        out= ('#'+self.config['telemetry_code']+','+str(self.millisecond)+','+str(self.get_gps())+
                 ','+str(self.voltage)+','+str(self.ampere)+','+str(self.accx)+','+str(self.accy)+
                 ','+str(self.accz)+','+str(self.gyrx)+','+str(self.gyry)+','+str(self.gyrz)+','+
                 str(self.magx)+','+str(self.magy)+','+str(self.magz)+','+str(self.temp_water)+','+str(self.temp_air)+','+str(self.temp_int)+','+str(self.ldr))
        return out
    
    def write_log(self,):
        '''
        Escribo en un archivo los utlimos datos
        '''
        #calculo el tiempo  desde el inicio en segundos que voy a mostrar:
        timeDataNow = datetime.utcnow()
        seconds_from_start = (timeDataNow-self.time_start).seconds
        
        
        #gestion de las marcas:
        race_marks = []
        for key in self.marks.keys():
            lastdata =self.marks_datas[key][-1] #este es el ultimo
            mark ='{'
            mark += '"nombre":"{}",'.format(self.marks[key].name)
            mark += '"tipo":"{}",'.format(self.marks[key].get_type())
            mark += '"localizacion":[{},{}]'.format(lastdata.longitude(WGS84=True),
                                                    lastdata.latitude(WGS84=True))
            mark +='}'
            
            race_marks.append(mark)
            
        #gestion de la linea de salida y llegada:
        start_pt_1 = [42.1244,-8.84640]
        start_pt_2 = [42.1242,-8.84642]
        
        end_pt_1 = [42.1247,-8.84643]
        end_pt_2 = [42.1244,-8.84646]
        
        
        #gestion de los vehiculos:
        race_devs = []
        for key in self.devices.keys():
            dev ='{'
            dev += '"nombre":"{}",'.format(self.devices[key].name)
            dev += '"tipo":"{}",'.format(self.devices[key].get_type())
            dev += '"color":"{}",'.format(self.devices_tracking[key].get_color_html())
            dev += '"nombreColor":"{}",'.format(self.devices_tracking[key].get_color())
            
            #cojo los ultimos datos de tiempo,ranking,voltage,amperios,velocidad,direccion y localizacion 
            lastdata =self.devices_datas[key][-1] #este es el ultimo
            
            last_seconds_from_start = (lastdata-self.race.timestamp_start).seconds #calc los segunsos del ultimo dato
            #si la diferencia es menor de 1.5 segundos, lo tomo como en el mismo tiempo
            if (seconds_from_start-last_seconds_from_start) < 1.5:
                dev += '"localizacion":[{},{}]'.format(lastdata.longitude(WGS84=True),
                                                       lastdata.latitude(WGS84=True))
                
            else:#sino, estimo a futuros los datos de posicion:
                #calculo los vectores de velocidad:
                vx=lastdata.velocity*math.cos(90-lastdata.direcction)
                vy=lastdata.velocity*math.sin(90-lastdata.direcction)
                
                #calculo sus nuevas posicones:
                dt=(timeDataNow-lastdata).total_seconds()
                sx= lastdata.longitude()+(vx*dt)
                sy= lastdata.latitude()+(vx*dt)
                #transformo UTM a WGS84 
                p_utm = Proj(init='epsg:'+str(32629)) # para las conversiones
                WGS84_lon,WGS84_lat =p_utm(sx,sy,inverse=True) #(x,y)
                
                dev += '"localizacion":[{},{}]'.format(WGS84_lon,
                                                       WGS84_lat)
                
            
            #estos valores nunca se estiman:
            dev += '"posicion":{},'.format(lastdata.ranking)
            power = lastdata.get_unit_SI('power_volt')*lastdata.get_unit_SI('power_amp')
            dev += '"power":{},'.format(power)
            
            dev += '"velocidad":{},'.format(lastdata.velocity)
            dev += '"direccion":{},'.format(lastdata.direcction)
            
            dev +='}'
            
            race_devs.append(dev)
        
        
        #escribo la salida
        out_js = '{'
        out_js +='"raceDate":"{:%d/%m/%Y %H:%M:%S}",'.format(self.race.timestamp_start)
        out_js +='"raceName":"{}",'.format(str(self.race))
        out_js +='"time":"{}",'.format(seconds_from_start)
        out_js +='"status":"{}",'.format(self.race.get_status())
        out_js +='"windDirection":{},'.format(23)
        out_js +='"windIntensity":{},'.format(34)
        
        out_js +='"startLine":[{},{}],'.format(start_pt_1,start_pt_2)
        out_js +='"finishLine":[{},{}],'.format(end_pt_1,end_pt_2)
        
        
        out_js +='"barcos":['
        out_js +=','.join(race_devs)
        out_js +=']'
        
        out_js +='"boyas":['
        out_js +=','.join(race_marks)
        out_js +=']'
        
        out_js +='}'
        
        with open(self.log_pathdir+'/last_data.js', 'w') as file:
            file.write(out_js)
        
    

####################################
#programa central
if __name__ == "__main__":
    
    
    devices = [] #doden se instancias todos los dispositivos virutales
    
    settings = ConfigObj('settings.conf', encoding="ISO-8859-1")
    #print(settings)
    
    print('marcas de boyas:')
    for item in settings['buoy_order']:
        #print(settings['devices'][item])
        devices.append((item,HIL_Device(settings['devices'][item])))
        
    
    print('barcos participantes:')
    for item in settings['ship_order']:
        #print(settings['devices'][item])   
        devices.append((item,HIL_Device(settings['devices'][item])))
    
    
    for i in range(5):
        for item in devices:
            item[1].update()
            print(item[1].get_packet())
        
        time.sleep(0.5)
    
    
