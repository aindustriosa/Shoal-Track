
import os

from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry,LineString, Point
 
from profiles.models import Contact,Organization,Monitor
from devices.models import Device, TeamTrace
from competition.models import Race, TrackGeom, Champion,ListTraceRaces, RaceTracking,Penalty,RaceTrackingNode,PenaltyTracking,RaceCategory
from telemetrydata.models import DeviceDataRaw,DataProcessing

import math
from pyproj import Proj
import json

def initial_datapack():
    datapack ={}
    datapack['latitudeUTM_Y_raw'] =-500.0
    datapack['longitudeUTM_X_raw'] =-500.0
    datapack['geom'] =Point(datapack['longitudeUTM_X_raw'],
                                            datapack['latitudeUTM_Y_raw'],
                                            srid=32629) # UTM29N
    datapack['geom_WGS84'] =datapack['geom']
    datapack['geom_WGS84'].transform(4326) # WSG84
    
    datapack['dgps_y']=0.0
    datapack['dgps_x']=0.0
    datapack['seconds']=0.0
    datapack['timestamp_gps']=timezone.now()
    datapack['timestamp']=timezone.now()
    datapack['timestamp_ms']=0
    datapack['timestamp_cycle']=0
    
    datapack['Wind_dir min'] =0
    datapack['Wind_dir_avg']=0
    datapack['Wind_dir_max']=0
    datapack['Wind_spd_min']=0.0
    datapack['Wind_spd_avg']=0.0
    datapack['Wind_spd_max']=0.0
    
    datapack['Air_temp'] =0.0
    datapack['Rel_humidity']=0.0
    datapack['Air_press']=0.0
    
    datapack['Rain_accumulation']=0.0
    datapack['Rain_duration']=0
    datapack['Rain_intensity']=0
    datapack['Hail_accumulation']=0 
    datapack['Hail_duration'] =0
    datapack['Hail_intensity']=0
    datapack['Rain_peak_intensity']=0 
    datapack['Hail_peak_intensity']=0
    
    datapack['accx']=0
    datapack['accx_si']=0
    datapack['accx_coef'] = None
    datapack['accy'] =0
    datapack['accy_si']=0
    datapack['accy_coef'] = None
    datapack['accz'] =0
    datapack['accz_si']=0
    datapack['accz_coef'] = None
    
    datapack['gyrx']=0
    datapack['gyrx_coef'] = None
    datapack['gyry'] =0
    datapack['gyry_coef'] = None
    datapack['gyrz'] =0
    datapack['gyrz_coef'] = None
    
    datapack['magx']=0
    datapack['magx_coef'] = None
    datapack['magy'] =0
    datapack['magy_coef'] = None
    datapack['magz'] =0
    datapack['magz_coef'] = None
    
    datapack['pressure']=0
    datapack['pressure_si']=0
    datapack['pressure_coef'] = None
    
    datapack['voltage']=0
    datapack['voltage_si']=0
    datapack['voltage_coef'] = None
    datapack['current']=0
    datapack['current_si']=0
    datapack['current_coef'] = None
    
    datapack['temp_int']=0
    datapack['temp_int_si']=0
    datapack['temp_int_coef'] = None
    datapack['temp_air'] =0
    datapack['temp_air_si'] =0
    datapack['temp_air_coef'] = None
    datapack['temp_water']=0
    datapack['temp_water_si']=0
    datapack['temp_water_coef'] = None
    datapack['ldr_fr']=0
    datapack['ldr_fr_si']=0
    datapack['ldr_fr_coef'] = None
    datapack['ldr_fl']=0
    datapack['ldr_fl_si']=0
    datapack['ldr_fl_coef'] = None
    datapack['ldr_br']=0
    datapack['ldr_br_si']=0
    datapack['ldr_br_coef'] = None
    datapack['ldr_bl']=0
    datapack['ldr_bl_si']=0
    datapack['ldr_bl_coef'] = None
    
    datapack['ranking']=0
    datapack['velocity']=0.0
    datapack['direction']=0
    datapack['distance']=0
    
    return datapack
    

class MonitoringRace():
    '''
    Clase para la monitorizacion de una carrera
    Se carga unas consultas para no estar constanteemente pidiendo los datos
    '''
    def __init__(self,):
        self.enable_log = False #para activar o desactivar el log a ficheros
        self.log_pathdir = '/mnt/ramdisk/shoaltrack/services/json'
        self.champion = None
        self.race         = None
        
        self.gateway_id='' #el codigo del dispositivo que hace de Gateway
        
        self.marks_set = set()
        self.marks_order=[] # el orden de las marcas para
        self.devices_set = set()
        self.fixed_marks_set =set()
        
        self.node={}
        self.trackings ={}
        self.calibrations ={}
        self.datas ={}
        self.lines_cross=[] #es una lista de lineas de puntos:
        self.lines_geom=[] #es una lista de geometrias UTM29N
        self.lines_geom_wsg84=[] #es una lista de geometrias WSG84
        self.devices_crosstrack ={} #es la cuenta de por donde voy pasando 
        
        #para el almacenage de los valores a guardad en la DB
        self.telemetry_items =[]
        
        self.count_last_data = 60#cuando guardo, aprox 1 minuto
        
        #variables:
        self.time_now ={'config':timezone.now()-timezone.timedelta(seconds=10),
                        'load':timezone.now()-timezone.timedelta(seconds=10),
                        'calibration':timezone.now()-timezone.timedelta(seconds=10),
                        'commit':timezone.now()-timezone.timedelta(seconds=10),
                        'logwrite':timezone.now()-timezone.timedelta(seconds=10)
                       }
        
        #creo el directorio de trabajo si no existe:
        if not os.path.exists(self.log_pathdir):
            os.makedirs(self.log_pathdir)
        
        
    def config_race(self, race_to_monitoring=None,force=False):
        '''race_to_monitoring = [name,edicion]
        '''
        #carga la carrera, su campeonato y su track cada 5 seg:
        new_time = timezone.now()
        if ((new_time-self.time_now['config']).seconds > 5) or (force==True):
        
            if not race_to_monitoring:
                self.race = Race.objects.filter(pk=self.race.pk).get() #actualizo el query
                
            elif isinstance(race_to_monitoring, str):
                self.race = Race.objects.filter(slug=race_to_monitoring).get()
                
            else:#ya es una instancia de query
                self.race = race_to_monitoring
            
            #obtengo a que campeonato pertenece y su ordnedentro de el
            trace_champion = ListTraceRaces.objects.filter(race=self.race).select_related("champion").get()
            
            self.champion = trace_champion.champion
            
            #obtengo sus marcas delimitadores y su trayecto por orden ascendente
            marks_tracks = TrackGeom.objects.filter(race=self.race).order_by('order').select_related("device")
            self.marks_set = set() #reseteo la variable
            for track in marks_tracks:
                self.node[track.device.acronym] = track.device # el dispositivo completo
                self.trackings[track.device.acronym] = track # su traking
                self.marks_set.add(track.device.acronym) # su clasificador
                self.datas[track.device.acronym]=[]#su gestion de datos
                #guardo si la marca es fija
                if (track.device.category ==Device.TYPE.fixedbuoy):
                    self.fixed_marks_set.add(track.device.acronym)
                elif (track.device.category ==Device.TYPE.fixedgateway):
                    self.gateway_id=track.device.acronym
                    
                #añado las geometrias de las marcas y las trasnformo a geometria
                self.lines_cross = self.race.get_geom_marks()
                print(self.lines_cross)
                for line_cr in self.lines_cross:
                    print(line_cr)
                    line_utm = LineString(line_cr,srid=32629)
                    line_wsg84=line_utm
                    line_wsg84.transform(4326)
                    self.lines_geom.append(line_utm) #UTM29N
                    self.lines_geom_wsg84.append(line_wsg84)
                    
                #añado el id de la marca en su orden ascendente
                self.marks_order.append(track.device.acronym)
                     
                #añado una entrada de telemetria en blanco si no hay datos:
                if len(self.datas[track.device.acronym])<1:
                    self.datas[track.device.acronym].append(initial_datapack())
            
            self.time_now['config'] = new_time
    
    def load_devices(self,force=False):
        '''Carga los dispositivos
        '''
        new_time = timezone.now()
        if( (new_time-self.time_now['load']).seconds > 3) or (force==True):
            trackings =RaceTracking.objects.filter(race=self.race
                                                           ).select_related('category','device')
            
            self.devices_set = set() #reseteo la variable
            for tracking in trackings:
                self.node[tracking.device.acronym] = tracking.device # el dispositivo completo
                self.trackings[tracking.device.acronym] = tracking # el traking de cada dispositivo
                self.devices_set.add(tracking.device.acronym) # su clasificador
                self.datas[tracking.device.acronym]=[]#su gestion de datos
                self.devices_crosstrack[tracking.device.acronym] = [False]*len(self.lines_cross) #las marcas de si ha pasado
                
                #añado una entrada de telemetria en blanco si no hay datos:
                if len(self.datas[tracking.device.acronym])<1:
                    self.datas[tracking.device.acronym].append(initial_datapack())
        
            self.time_now['load'] = new_time
    
    def update_status(self,):
        self.race = Race.objects.filter(pk=self.race.pk).get() #actualizo el query
        
        return self.race.get_status(),self.race.status
         
    def update_calibration(self,force=False):
        new_time = timezone.now()
        if ((new_time-self.time_now['calibration']).seconds > 5) or (force==True):
            for key in self.node.keys():
                qDataproc ={}
                ###########Acelerometer
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.accelerometer_x).order_by('-timestamp')[0]
                    qDataproc['accelerometer_x'] =calib1
                except:
                    qDataproc['accelerometer_x'] = None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.accelerometer_y).order_by('-timestamp')[0]
                    qDataproc['accelerometer_y'] = calib1
                except:
                    qDataproc['accelerometer_y'] = None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.accelerometer_z).order_by('-timestamp')[0]
                    qDataproc['accelerometer_z'] = calib1
                except:
                    qDataproc['accelerometer_z'] =None
                ###########Gyroscopo
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.gyroscope_x).order_by('-timestamp')[0]
                    qDataproc['gyroscope_x'] = calib1
                except:
                    qDataproc['gyroscope_x'] = None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.gyroscope_y).order_by('-timestamp')[0]
                    qDataproc['gyroscope_y'] = calib1
                except:
                    qDataproc['gyroscope_y'] = None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.gyroscope_z).order_by('-timestamp')[0]
                    qDataproc['gyroscope_z'] = calib1
                except:
                    qDataproc['gyroscope_z'] = None
                ###########Magnetometro
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.magnetometer_x).order_by('-timestamp')[0]
                    qDataproc['magnetometer_x'] =calib1
                except:
                    qDataproc['magnetometer_x'] = None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.magnetometer_y).order_by('-timestamp')[0]
                    qDataproc['magnetometer_y'] = calib1
                except:
                    qDataproc['magnetometer_y'] =None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.magnetometer_z).order_by('-timestamp')[0]
                    qDataproc['magnetometer_z'] = calib1
                except:
                    qDataproc['magnetometer_z'] = None
                ##############Presion
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.pressure).order_by('-timestamp')[0]
                    qDataproc['pressure'] =calib1
                except:
                    qDataproc['pressure'] = None
                ###############temperaturas
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.temperature_int).order_by('-timestamp')[0]
                    qDataproc['temperature_int'] =calib1
                except:
                    qDataproc['temperature_int'] =None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.temperature_air).order_by('-timestamp')[0]
                    qDataproc['temperature_air'] = calib1
                except:
                    qDataproc['temperature_air'] =None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.temperature_water).order_by('-timestamp')[0]
                    qDataproc['temperature_water'] = calib1
                except:
                    qDataproc['temperature_water'] = None
                    
                ###########Iluminacion
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.ilumination_fr).order_by('-timestamp')[0]
                    qDataproc['ilumination_fr'] = calib1
                except:
                    qDataproc['ilumination_fr'] =None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.ilumination_fl).order_by('-timestamp')[0]
                    qDataproc['ilumination_fl'] =calib1
                except:
                    qDataproc['ilumination_fl'] = None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.ilumination_br).order_by('-timestamp')[0]
                    qDataproc['ilumination_br'] = calib1
                except:
                    qDataproc['ilumination_br'] = None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.ilumination_bl).order_by('-timestamp')[0]
                    qDataproc['ilumination_bl'] =calib1
                except:
                    qDataproc['ilumination_bl'] =None
                    
                ########Potencia
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.voltage).order_by('-timestamp')[0]
                    qDataproc['voltage'] = calib1
                except:
                    qDataproc['voltage'] =None
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.amperes).order_by('-timestamp')[0]
                    qDataproc['amperes'] =calib1
                except:
                    qDataproc['amperes'] =None
                
                self.calibrations[key] = qDataproc
                
            self.time_now['calibration'] = new_time 
    
    def change_race_status(self,new_status):
        self.race.status = new_status
        
        if self.race.status == Race.STATUS.closed:
            self.race.timestamp_finish = timezone.now()
        
        self.race.save()
        
    def append_telemetry(self,datum):
        '''datum: es un diccionario
        '''
        #Calculo los segundos desde el inicio de carrera:
        #calculo el tiempo  desde el inicio en segundos que voy a mostrar:
        timeDataNow = timezone.now()
        seconds_from_start = (timeDataNow-self.race.timestamp_start).total_seconds()
        
        datapack = initial_datapack()
        
        #if not (datum['Id_Code'] in self.node.keys()):
        #    return
        
        if  (datum['Id_packet'] == 0):
            return
        
        if (datum['Id_packet'] == 5): #posicion Fija GPS del gateway
            #calculo ultims datos de correccion DGPS
            datapack['geom'] =Point(self.trackings[datum['Id_Code']].longitude(),
                                                    self.trackings[datum['Id_Code']].latitude(),
                                                    srid=32629) # UTM29N
            datapack['geom_WGS84'] =datapack['geom']
            datapack['geom_WGS84'].transform(4326) # WSG84
    
            datapack['dgps_y'] =self.trackings[datum['Id_Code']].latitude() - datum['latitudeUTM_Y_raw']
            datapack['dgps_x'] =self.trackings[datum['Id_Code']].longitude()-datum['longitudeUTM_X_raw']
            
            #añado los datos del gateway:
            datapack['seconds']=seconds_from_start
            datapack['timestamp_gps'] = datum['timestamp_gps']
            datapack['latitudeUTM_Y_raw']=datum['latitudeUTM_Y_raw']
            datapack['longitudeUTM_X_raw'] =datum['longitudeUTM_X_raw']
            datapack['timestamp']= datum['timestamp']
            
            #repito los ultimos datos:
            datapack['Wind_dir_avg'] =self.datas[datum['Id_Code']][-1]['Wind_dir_avg'] #
            datapack['Wind_spd_avg']= self.datas[datum['Id_Code']][-1]['Wind_spd_avg']
            datapack['Air_temp'] =self.datas[datum['Id_Code']][-1]['Air_temp']
            datapack['Rel_humidity'] = self.datas[datum['Id_Code']][-1]['Rel_humidity']
            datapack['Air_press']= self.datas[datum['Id_Code']][-1]['Air_press']
            
        elif (datum['Id_packet'] == 6):#data from vaisala
            #añado los datos del gateway:
            datapack['seconds'] =seconds_from_start
            
            if 'Wind_dir_avg' in datum.keys(): #es el datum de viento
                datapack['Wind_dir_avg']=datum['Wind_dir_avg']
                datapack['Wind_spd_avg']=datum['Wind_spd_avg']
                #meto los otros repetidos:
                datapack['Air_temp']= self.datas[datum['Id_Code']][-1]['Air_temp']
                datapack['Rel_humidity']=self.datas[datum['Id_Code']][-1]['Rel_humidity']
                datapack['Air_press']=self.datas[datum['Id_Code']][-1]['Air_press']
                
            elif 'Air_temp' in datum.keys(): #es el datum de temp y humedad
                datapack['Air_temp']=datum['Air_temp']
                datapack['Rel_humidity']=datum['Rel_humidity']
                datapack['Air_press']=datum['Rel_humidity']
                #meto los otros repetidos:
                datapack['Wind_dir_avg']=self.datas[datum['Id_Code']][-1]['Wind_dir_avg']
                datapack['Wind_spd_avg']=self.datas[datum['Id_Code']][-1]['Wind_spd_avg']
                
            else:
                #repito los ultimos datos:
                datapack['Wind_dir_avg']=self.datas[datum['Id_Code']][-1]['Wind_dir_avg']#
                datapack['Wind_spd_avg']=self.datas[datum['Id_Code']][-1]['Wind_spd_avg']
                datapack['Air_temp']=self.datas[datum['Id_Code']][-1]['Air_temp']
                datapack['Rel_humidity']=self.datas[datum['Id_Code']][-1]['Rel_humidity']
                datapack['Air_press']=self.datas[datum['Id_Code']][-1]['Air_press']
                
            #cubro los datos comunes repetidos:
            datapack['timestamp_gps']=self.datas[datum['Id_Code']][-1]['timestamp_gps']
            datapack['dgps_x']=self.datas[datum['Id_Code']][-1]['dgps_x']
            datapack['dgps_y']=self.datas[datum['Id_Code']][-1]['dgps_y']
            datapack['latitudeUTM_Y_raw']=self.datas[datum['Id_Code']][-1]['latitudeUTM_Y_raw']
            datapack['longitudeUTM_X_raw']=self.datas[datum['Id_Code']][-1]['longitudeUTM_X_raw']
            datapack['geom'] =self.datas[datum['Id_Code']][-1]['geom']
            datapack['geom_WGS84'] =self.datas[datum['Id_Code']][-1]['geom_WGS84']
            
            
        elif (datum['Id_packet'] == 15): #añade un pack de datos
            #calculo GPS corregido:
            datapack['latitudeUTM_Y'] = datum['latitudeUTM_Y_raw'] +self.datas[self.gateway_id][-1]['dgps_y']
            datapack['longitudeUTM_X'] = datum['longitudeUTM_X_raw'] +self.datas[self.gateway_id][-1]['dgps_x'] 
            
            datapack['geom'] =Point(datapack['longitudeUTM_X'],
                                                    datapack['latitudeUTM_Y'],
                                                    srid=32629) # UTM29N
            datapack['geom_WGS84'] =datapack['geom']
            datapack['geom_WGS84'].transform(4326) # WSG84
            
            datapack['seconds']=seconds_from_start
            datapack['timestamp_gps']=datum['timestamp_gps']
            datapack['timestamp']=datum['timestamp']
            datapack['timestamp_ms']=datum['timestamp_ms']
            datapack['timestamp_cycle']=datum['timestamp_cycle']
            
            #grabo los valores RAW: FUCK!!!!!!!!!!!!!!
            datapack['latitudeUTM_Y_raw'] = datum['latitudeUTM_Y_raw']
            datapack['longitudeUTM_X_raw'] = datum['longitudeUTM_X_raw']
            datapack['accx'] = datum['accx']
            datapack['accy'] = datum['accy']
            datapack['accz'] = datum['accz']
            datapack['gyrx'] = datum['gyrx']
            datapack['gyry'] = datum['gyry']
            datapack['gyrz'] = datum['gyrz']
            datapack['magx'] = datum['magx']
            datapack['magy'] = datum['magy']
            datapack['magz'] = datum['magz']
            datapack['pressure'] = datum['pressure']
            datapack['voltage'] = datum['voltage']
            datapack['current'] = datum['current']
            datapack['temp_int'] = datum['temp_int']
            datapack['temp_air'] = datum['temp_air']
            datapack['temp_water'] = datum['temp_water']
            datapack['ldr_fr'] = datum['ldr_fr']
            datapack['ldr_fl'] = datum['ldr_fl']
            datapack['ldr_br'] = datum['ldr_br']
            datapack['ldr_bl'] = datum['ldr_bl']
            #se acaboel Fuck, estaparte es fucional....
            
            #valores con transformacion: 
            calibration = self.calibrations[datum['Id_Code']]
            if calibration['accelerometer_x']:
                datapack['accx_si'] = calibration['accelerometer_x'].raw_to_SI(datum['accx'])
                datapack['accx_coef'] =calibration['accelerometer_x']
            else:
                datapack['accx_si'] = datum['accx']
                
            if calibration['accelerometer_y']:
                datapack['accy_si'] = calibration['accelerometer_y'].raw_to_SI(datum['accy'])
                datapack['accy_coef'] =calibration['accelerometer_y']
            else:
                datapack['accy_si'] = datum['accy']
            
            if calibration['accelerometer_z']:
                datapack['accz_si'] = calibration['accelerometer_z'].raw_to_SI(datum['accz'])
                datapack['accz_coef'] =calibration['accelerometer_z']
            else:
                datapack['accz_si'] = datum['accz']
            ####################################################
            if calibration['gyroscope_x']:
                datapack['gyrx_si'] = calibration['gyroscope_x'].raw_to_SI(datum['gyrx'])
                datapack['gyrx_coef'] =calibration['gyroscope_x']
            else:
                datapack['gyrx_si'] = datum['gyrx']
                
            if calibration['gyroscope_y']:
                datapack['gyry_si'] = calibration['gyroscope_y'].raw_to_SI(datum['gyry'])
                datapack['gyry_coef'] =calibration['gyroscope_y']
            else:
                datapack['gyry_si'] = datum['gyry']
            
            if calibration['gyroscope_z']:
                datapack['gyrz_si'] = calibration['gyroscope_z'].raw_to_SI(datum['gyrz'])
                datapack['gyrz_coef'] =calibration['gyroscope_z']
            else:
                datapack['gyrz_si'] = datum['gyrz']
            ####################################################
            if calibration['magnetometer_x']:
                datapack['magx_si'] = calibration['magnetometer_x'].raw_to_SI(datum['magx'])
                datapack['magx_coef'] =calibration['magnetometer_x']
            else:
                datapack['magx_si'] = datum['magx']
                
            if calibration['magnetometer_y']:
                datapack['magy_si'] = calibration['magnetometer_y'].raw_to_SI(datum['magy'])
                datapack['magy_coef'] =calibration['magnetometer_y']
            else:
                datapack['magy_si'] = datum['magy']
            
            if calibration['magnetometer_z']:
                datapack['magz_si'] = calibration['magnetometer_z'].raw_to_SI(datum['magz'])
                datapack['magz_coef'] =calibration['magnetometer_z']
            else:
                datapack['magz_si'] = datum['magz']
            ####################################################
            if calibration['pressure']:
                datapack['pressure_si'] = calibration['pressure'].raw_to_SI(datum['pressure'])
                datapack['pressure_coef'] =calibration['pressure']
            else:
                datapack['pressure_si'] = datum['pressure']
            ####################################################
            if calibration['voltage']:
                datapack['voltage_si'] = calibration['voltage'].raw_to_SI(datum['voltage'])
                datapack['voltage_coef'] =calibration['voltage']
            else:
                datapack['voltage_si'] = datum['voltage']
                
            if calibration['amperes']:
                datapack['current_si'] = calibration['amperes'].raw_to_SI(datum['current'])
                datapack['current_coef'] =calibration['amperes']
            else:
                datapack['current_si'] = datum['current']
                
            ####################################################
            if calibration['temperature_int']:
                datapack['temp_int_si'] = calibration['temperature_int'].raw_to_SI(datum['temp_int'])
                datapack['temp_int_coef'] =calibration['temperature_int']
            else:
                datapack['temp_int_si'] = datum['temp_int']
                
            if calibration['temperature_air']:
                datapack['temp_air_si'] = calibration['temperature_air'].raw_to_SI(datum['temp_air'])
                datapack['temp_air_coef'] =calibration['temperature_air']
            else:
                datapack['temp_air_si'] = datum['temp_air']
            
            if calibration['temperature_water']:
                datapack['temp_water_si'] = calibration['temperature_water'].raw_to_SI(datum['temp_water'])
                datapack['temp_water_coef'] =calibration['temperature_water']
            else:
                datapack['temp_water_si'] = datum['temp_water']
            ####################################################
            if calibration['ilumination_fr']:
                datapack['ldr_fr_si'] = calibration['ilumination_fr'].raw_to_SI(datum['ldr_fr'])
                datapack['ldr_fr_coef'] =calibration['ilumination_fr']
            else:
                datapack['ldr_fr_si'] = datum['ldr_fr']
                
            if calibration['ilumination_fl']:
                datapack['ldr_fl_si'] = calibration['ilumination_fl'].raw_to_SI(datum['ldr_fl'])
                datapack['ldr_fl_coef'] =calibration['ilumination_fl']
            else:
                datapack['ldr_fl_si'] = datum['ldr_fl']
            
            if calibration['ilumination_br']:
                datapack['ldr_br_si'] = calibration['ilumination_br'].raw_to_SI(datum['ldr_br'])
                datapack['ldr_br_coef'] =calibration['ilumination_br']
            else:
                datapack['ldr_br_si'] = datum['ldr_br']
                
            if calibration['ilumination_bl']:
                datapack['ldr_bl_si'] = calibration['ilumination_bl'].raw_to_SI(datum['ldr_bl'])
                datapack['ldr_bl_coef'] =calibration['ilumination_bl']
            else:
                datapack['ldr_bl_si'] = datum['ldr_bl']
            
    
            if (datum['Id_Code'] in self.devices_set): #hago cosa de dispositivos
                #calcula ranking:
                datapack['ranking']=0
                #para cada  self.devices_crosstrack
                #sumo 1000 sies true, si es false, salgo
                #sumo la cantidaddemetros que hay de su posicion gps hasta la linea de marca
                #para cada punto de chequeo 
                
                #Si ya ha llegado al final , 
                if self.devices_crosstrack[datum['Id_Code']][-1] == True:
                    datapack['ranking']=self.datas[datum['Id_Code']][-1]['ranking']+1
                    #simplemente le sumo uno mas para estar siempre de primero
                else:#sino, hace el calculo
                    count_mark=0
                    for cross in self.devices_crosstrack[datum['Id_Code']]:
                        if not cross: #miro si no lo he pasado todavia:
                            break
                        else:
                            datapack['ranking'] +=1000.0 #lo he pasado y sumo mucho
                            count_mark+=1
                    #calculo si he intersectado la marca:
                    #hago una linea de los ultimos 5 datos 
                    estela_points= []
                    for i in range(5):
                        try:
                            estela_points.append([self.datas[datum['Id_Code']][-1-i]['geom'].x,
                                                                 self.datas[datum['Id_Code']][-1-i]['geom'].y  ])
                        except: 
                            estela_points.append([self.datas[datum['Id_Code']][-1]['geom'].x,
                                                                 self.datas[datum['Id_Code']][-1]['geom'].y  ])
                            break
                    estela =LineString(estela_points,srid=32629)
                    
                    #y la intersecto con la marca
                    if self.lines_geom[count_mark].intersects(estela):
                        datapack['ranking'] +=1000.0 #lo he pasado y sumo mucho
                        self.devices_crosstrack[datum['Id_Code']][count_mark] =True
                        #la añado al traking de la DB
                        id_mark = self.marks_order[count_mark]
                        track_check = RaceTrackingNode.objects.create(trackgeom=self.trackings[id_mark],
                                                                      racetracking=self.trackings[datum['Id_Code']],
                                                                      timestamp_pass=datapack['timestamp'])
                        count_mark+=1 #salto ala sigiuente marca
                    
                    #calcuo la distancia respecto a la linea de la siguente marca:
                    datapack['ranking'] +=datapack['geom'].distance(self.lines_geom[count_mark])
                
                #calcula velocidad y direccion
                #posicion anterior posicion actual, tiempo -> velocidad, direccion
                Ax=datapack['geom'].distance(self.datas[datum['Id_Code']][-1]['geom'])
                At=datapack['seconds']-self.datas[datum['Id_Code']][-1]['seconds']
                datapack['velocity']=Ax/At
                
                ejeX=datapack['geom'].x-self.datas[datum['Id_Code']][-1]['geom'].x
                ejeY=datapack['geom'].y-self.datas[datum['Id_Code']][-1]['geom'].y
                try:
                    radianes= math.atan(ejeY/ejeX)
                except:
                    radianes=0
                datapack['direction']=int(math.degrees(radianes))+90
            
        ##############################
        #meto todos los datos en la cache:
        self.datas[datum['Id_Code']].append(datapack)
        
        #solodejo los ultimos 60 datos:
        if len(self.datas[datum['Id_Code']]) > self.count_last_data:
            temp = self.datas[datum['Id_Code']].pop()
                
        #meto en la cola el dato para grabar
        self.telemetry_items.append(
                DeviceDataRaw(device=self.node[datum['Id_Code']],
                                         timestamp=datapack['timestamp'],
                                         geom=datapack['geom'],
                                         millisecons=datapack['timestamp_ms'],
                                         longitude_raw=datapack['longitudeUTM_X_raw'],
                                         latitude_raw=datapack['latitudeUTM_Y_raw'],
                                         timestamp_gps=datapack['timestamp_gps'],
                                         
                                         accX_raw=datapack['accx'],
                                         accX_coef=datapack['accx_coef'],
                                         accY_raw=datapack['accy'],
                                         accY_coef=datapack['accy_coef'],
                                         accZ_raw=datapack['accz'],
                                         accZ_coef=datapack['accz_coef'],
                                         
                                         gyrX_raw=datapack['gyrx'],
                                         gyrX_coef=datapack['gyrx_coef'],
                                         gyrY_raw=datapack['gyry'],
                                         gyrY_coef=datapack['gyry_coef'],
                                         gyrZ_raw=datapack['gyrz'],
                                         gyrZ_coef=datapack['gyrz_coef'],
                                         
                                         magX_raw=datapack['magx'],
                                         magX_coef=datapack['magx_coef'],
                                         magY_raw=datapack['magy'],
                                         magY_coef=datapack['magy_coef'],
                                         magZ_raw=datapack['magz'],
                                         magZ_coef=datapack['magz_coef'],
                                         
                                         press_air_raw=datapack['pressure'],
                                         press_air_coef=datapack['pressure_coef'],
                                         
                                         temp_int_raw=datapack['temp_int'],
                                         temp_int_coef=datapack['temp_int_coef'],
                                         temp_air_raw=datapack['temp_air'],
                                         temp_air_coef=datapack['temp_air_coef'],
                                         temp_water_raw=datapack['temp_water'],
                                         temp_water_coef=datapack['temp_water_coef'],
                                         
                                         ldr_fr_raw=datapack['ldr_fr'],
                                         ldr_fr_coef=datapack['ldr_fr_coef'],
                                         ldr_fl_raw=datapack['ldr_fl'],
                                         ldr_fl_coef=datapack['ldr_fl_coef'],
                                         ldr_br_raw=datapack['ldr_br'],
                                         ldr_br_coef=datapack['ldr_br_coef'],
                                         ldr_bl_raw=datapack['ldr_bl'],
                                         ldr_bl_coef=datapack['ldr_bl_coef'],
                                         
                                         power_volt=datapack['voltage'],
                                         power_volt_coef=datapack['voltage_coef'],
                                         power_amp=datapack['current'],
                                         power_amp_coef=datapack['current_coef'],
                                         
                                         ref_air_temp=datapack['Air_temp'],
                                         ref_pressure=datapack['Air_press'],
                                         ref_humidity_relative=datapack['Rel_humidity'],
                                         ref_wind_module=datapack['Wind_spd_avg'],
                                         ref_wind_direction=datapack['Wind_dir_avg'],
                                         
                                         ranking=datapack['ranking'],
                                         velocity=datapack['velocity'],
                                         direction=datapack['direction'])
                )
        
        #cada 1 segundos graba un log nuevo con los ultimos datos (hace estimacion futura de posicion con la velocidad y direccion)
        
        new_time = timezone.now()
        
        if (new_time-self.time_now['logwrite']).seconds > 1:
            if self.enable_log:
                self.write_log()
            self.time_now['logwrite'] = new_time 
            
            
        #cada 5 segundos haceun commit de todo
        new_time = timezone.now()
        if (new_time-self.time_now['commit']).seconds > 5:
            self.commit_data()
            self.time_now['commit'] = new_time 
            
    
    def commit_data(self,):
        DeviceDataRaw.objects.bulk_create(self.telemetry_items)
        
        #actualizo la DB round robin:
        
        
        #ya los puedo borrar
        self.telemetry_items = []
        
    def write_log(self,):
        '''
        Escribo en un archivo los utlimos datos
        '''
        #calculo el tiempo  desde el inicio en segundos que voy a mostrar:
        timeDataNow = timezone.now()
        seconds_from_start = (timeDataNow-self.race.timestamp_start).seconds
        
        p_utm = Proj(init='epsg:'+str(32629)) # para las conversiones de UTM a WSG84
        
        ########################
        out_js = {}
        out_js['raceDate'] = '{:%d/%m/%Y %H:%M:%S}'.format(self.race.timestamp_start)
        out_js['raceName'] = str(self.race)
        out_js['time'] = seconds_from_start
        out_js['status'] =self.race.get_status()
        
        out_js['startLine'] = [[self.lines_geom_wsg84[0][0][1],self.lines_geom_wsg84[0][0][0]],
                                         [self.lines_geom_wsg84[0][1][1],self.lines_geom_wsg84[0][1][0]]
                                        ]
        out_js['finishLine'] =[[self.lines_geom_wsg84[-1][0][1],self.lines_geom_wsg84[-1][0][0]],
                                         [self.lines_geom_wsg84[-1][1][1],self.lines_geom_wsg84[-1][1][0]]
                                        ]
        
        out_js['barcos'] = []
        out_js['boyas'] = []
        
        for key in self.node.keys():
            lastdata =self.datas[key][-1] #este es el ultimo
            #gestion de las marcas:
            if key in self.marks_set:
                mark = {}
                mark['nombre'] = self.node[key].name
                mark['tipo'] = self.node[key].get_type()
                mark['localizacion'] =[lastdata['geom_WGS84'].y,
                                                  lastdata['geom_WGS84'].x] 
                
                out_js['boyas'].append(mark)
            
            #gestion de los vehiculos:
            elif key in self.devices_set:
                dev = {}
                dev['nombre'] = self.node[key].name
                dev['tipo'] = self.node[key].get_type()
                dev['color'] = self.trackings[key].get_color_html()
                dev['nombreColor'] = self.trackings[key].get_color()
                
                last_seconds_from_start = (lastdata['timestamp']-self.race.timestamp_start).seconds #calc los segunsos del ultimo dato
                #si la diferencia es menor de 1.5 segundos, lo tomo como en el mismo tiempo
                #if (seconds_from_start-last_seconds_from_start) < 1.5:
                WGS84 =[0,0]
                WGS84[0] = lastdata['geom_WGS84'].x
                WGS84[1] =  lastdata['geom_WGS84'].y
                '''
                else:#sino, estimo a futuros los datos de posicion:
                    #calculo los vectores de velocidad:
                    vx=lastdata['velocity']*math.cos(90-lastdata['direction'])
                    vy=lastdata['velocity']*math.sin(90-lastdata['direction'])
                    
                    #calculo sus nuevas posicones:
                    dt=(timeDataNow-lastdata['timestamp']).total_seconds()
                    sx= lastdata['geom'].x+(vx*dt)
                    sy= lastdata['geom'].y+(vy*dt)
                    #transformo UTM a WGS84 
                    WGS84=p_utm(sx,sy,inverse=True) #(x,y)
                '''
                    
                dev['localizacion'] =[WGS84[1],WGS84[0]] 
                dev['posicion'] = lastdata['ranking']
                power = lastdata['voltage_si']*lastdata['current_si']
                dev['power'] =power
                
                dev['velocidad'] =lastdata['velocity']
                dev['direccion'] =lastdata['direction']
                
                out_js['barcos'].append(dev)
        
        out_js['windDirection'] = self.datas[self.gateway_id][-1]['Wind_dir_avg']
        out_js['windIntensity'] =  self.datas[self.gateway_id][-1]['Wind_spd_avg']
        
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
            dev['nombre'] = self.node[key].name
            dev['color'] = self.trackings[key].get_color_html()
            dev['posicion'] = lastdata['ranking']
            power = lastdata['voltage_si']*lastdata['current_si']
            dev['power'] =power
            dev['velocidad'] =lastdata['velocity']
            dev['direccion'] =lastdata['direction']
            
            dev['accX'] =lastdata['accx_si']
            dev['accY'] =lastdata['accy_si']
            dev['accZ'] =lastdata['accz_si']
            
            dev['temp_int'] =lastdata['temp_int_si']
            dev['temp_air'] =lastdata['temp_air_si']
            dev['temp_water'] =lastdata['temp_water_si']
            dev['ldr_fr'] =lastdata['ldr_fr_si']
            dev['ldr_fl'] =lastdata['ldr_fl_si']
            dev['ldr_br'] =lastdata['ldr_br_si']
            dev['ldr_bl'] =lastdata['ldr_bl_si']
            
            dev['power_volt'] =lastdata['voltage_si']
            dev['power_amp'] =lastdata['current_si']
            
            
            out_js['barcos'].append(dev)
            
        
        with open(self.log_pathdir+'/last_variables.json', 'w') as outfile:
            json.dump(out_js, outfile)
        
