
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
    datapack['gps_latitude'] =-500.0
    datapack['gps_longitude'] =-500.0
    datapack['geom'] =Point(datapack['gps_longitude'],
                            datapack['gps_latitude'],
                            srid=32629) # UTM29N
    datapack['geom_WGS84'] =datapack['geom']
    datapack['geom_WGS84'].transform(4326) # WSG84
    
    datapack['dgps_y']=0.0
    datapack['dgps_x']=0.0
    datapack['seconds']=0.0
    datapack['timestamp']=timezone.now()
    datapack['timestamp_rcv']=timezone.now()
    datapack['nextHop']=-1
    datapack['rssi']=0
    
    datapack['gps_precision']=-1
    datapack['gps_itow']=-1
    datapack['gps_heading']=-1
    
    
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
    
    
    datapack['bearing_avg']=0
    datapack['bearing_std']=0
    datapack['bearing_si']=0
    datapack['bearing_coef']=None
    
    datapack['voltage_batt_avg']=0
    datapack['voltage_batt_std']=0
    datapack['voltage_batt_si']=0
    datapack['voltage_batt_coef']=None
    
    datapack['amp_batt_avg']=0
    datapack['amp_batt_std']=0
    datapack['amp_batt_si']=0
    datapack['amp_batt_coef']=None
    
    datapack['pressure_avg']=0
    datapack['pressure_std']=0
    datapack['pressure_si']=0
    datapack['pressure_coef']=None
    
    datapack['ligth_avg']=0
    datapack['ligth_std']=0
    datapack['ligth_si']=0
    datapack['ligth_coef']=None
    
    datapack['accX_avg']=0
    datapack['accX_std']=0
    datapack['accX_si']=0
    datapack['accX_coef']=None
    
    datapack['accY_avg']=0
    datapack['accY_std']=0
    datapack['accY_si']=0
    datapack['accY_coef']=None
    
    datapack['accZ_avg']=0
    datapack['accZ_std']=0
    datapack['accZ_si']=0
    datapack['accZ_coef']=None
    
    datapack['gyrX_avg']=0
    datapack['gyrX_std']=0
    datapack['gyrX_si']=0
    datapack['gyrX_coef']=None
    
    datapack['gyrY_avg']=0
    datapack['gyrY_std']=0
    datapack['gyrY_si']=0
    datapack['gyrY_coef']=None
    
    datapack['gyrZ_avg']=0
    datapack['gyrZ_std']=0
    datapack['gyrZ_si']=0
    datapack['gyrZ_coef']=None
    
    
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
        self.error_logfile = '/home/www-data/log/shoaltrack_race.log'
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
                    empty_data = initial_datapack()
                    empty_data['geom_WGS84'] = track.geom
                    empty_data['geom_WGS84'].transform(4326) # WSG84
                    self.datas[track.device.acronym].append(empty_data)
            
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
                                                               type_param=DataProcessing.TYPEPARAM.orientation).order_by('-timestamp')[0]
                    qDataproc['orientation'] =calib1
                except:
                    qDataproc['orientation'] = None
                
                ##############Presion
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.pressure).order_by('-timestamp')[0]
                    qDataproc['pressure'] =calib1
                except:
                    qDataproc['pressure'] = None

                    
                ###########Iluminacion
                try:
                    calib1=DataProcessing.objects.filter(device=self.node[key],
                                                               type_param=DataProcessing.TYPEPARAM.ilumination).order_by('-timestamp')[0]
                    qDataproc['ilumination'] = calib1
                except:
                    qDataproc['ilumination'] =None
                
                    
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
        
        if not (datum['Id_Code'] in self.node.keys()):
            self.write_error(datum)
            return
        #si no hay mensaje correcto, salgo:
        try:
            id_packet = datum['msgID']
        except:
            self.write_error(datum)
            return
        
        #CARDUME_ID_TRACEROUTE y gateway
        if  ((id_packet == 48)and (datum['Id_Code']=='GTWN01')):
            
            #transfomro WSG84 a UTM:
            utm_point =Point(datum['gps_longitude'],datum['gps_latitude'],srid=4326) # WSG84
            utm_point.transform(32629) # UTM29N
            
            #posicion Fija GPS del gateway
            #calculo ultims datos de correccion DGPS
            datapack['geom'] =Point(self.trackings[datum['Id_Code']].longitude(),
                                                    self.trackings[datum['Id_Code']].latitude(),
                                                    srid=32629) # UTM29N
            
            datapack['geom_WGS84'] =datapack['geom']
            datapack['geom_WGS84'].transform(4326) # WSG84
    
            datapack['dgps_y'] =self.trackings[datum['Id_Code']].latitude() -utm_point.y
            datapack['dgps_x'] =self.trackings[datum['Id_Code']].longitude()-utm_point.x
            
            #añado los datos del gateway:
            datapack['seconds']=seconds_from_start
            datapack['gps_latitude']=utm_point.y
            datapack['gps_longitude'] =utm_point.x
            
            datapack['timestamp']=datum['time_mark']
            datapack['timestamp_rcv']=timeDataNow
            datapack['rssi']=datum['rssi']
    
            datapack['gps_precision']=datum['gps_precision']
            datapack['gps_itow']=datum['gps_itow']
            
            #repito los ultimos datos:
            datapack['Wind_dir_avg'] =self.datas[datum['Id_Code']][-1]['Wind_dir_avg'] #
            datapack['Wind_spd_avg']= self.datas[datum['Id_Code']][-1]['Wind_spd_avg']
            datapack['Air_temp'] =self.datas[datum['Id_Code']][-1]['Air_temp']
            datapack['Rel_humidity'] = self.datas[datum['Id_Code']][-1]['Rel_humidity']
            datapack['Air_press']= self.datas[datum['Id_Code']][-1]['Air_press']
            
        
        #CARDUME_ID_METEOTHP or #CARDUME_ID_METEOWIND
        elif  ((id_packet == 131)or(id_packet == 130)):
            #añado los datos del gateway:
            datapack['seconds'] =seconds_from_start
            
            if 'wind_direction_min' in datum.keys(): #es el datum de viento
                datapack['Wind_dir_avg']=datum['wind_direction_avg']
                datapack['Wind_spd_avg']=datum['wind_speed_avg']
                #meto los otros repetidos:
                datapack['Air_temp']= self.datas[datum['Id_Code']][-1]['Air_temp']
                datapack['Rel_humidity']=self.datas[datum['Id_Code']][-1]['Rel_humidity']
                datapack['Air_press']=self.datas[datum['Id_Code']][-1]['Air_press']
                
            elif 'air_temperature' in datum.keys(): #es el datum de temp y humedad
                datapack['Air_temp']=datum['air_temperature']
                datapack['Rel_humidity']=datum['relative_humidity']
                datapack['Air_press']=datum['air_pressure']
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
            datapack['timestamp']=self.datas[datum['Id_Code']][-1]['timestamp']
            datapack['dgps_x']=self.datas[datum['Id_Code']][-1]['dgps_x']
            datapack['dgps_y']=self.datas[datum['Id_Code']][-1]['dgps_y']
            datapack['gps_latitude']=self.datas[datum['Id_Code']][-1]['gps_latitude']
            datapack['gps_longitude']=self.datas[datum['Id_Code']][-1]['gps_longitude']
            datapack['geom'] =self.datas[datum['Id_Code']][-1]['geom']
            datapack['geom_WGS84'] =self.datas[datum['Id_Code']][-1]['geom_WGS84']
            
        
        #CARDUME_ID_SHOALTRACK
        elif  (id_packet == 129):
            #transfomro WSG84 a UTM:
            utm_point =Point(datum['gps_longitude'],datum['gps_latitude'],srid=4326) # WSG84
            utm_point.transform(32629) # UTM29N
            
            #calculo GPS corregido:
            datapack['latitudeUTM_Y'] = utm_point.y +self.datas[self.gateway_id][-1]['dgps_y']
            datapack['longitudeUTM_X'] = utm_point.x +self.datas[self.gateway_id][-1]['dgps_x'] 
            
            datapack['geom'] =Point(datapack['longitudeUTM_X'],
                                                    datapack['latitudeUTM_Y'],
                                                    srid=32629) # UTM29N
            datapack['geom_WGS84'] =datapack['geom']
            datapack['geom_WGS84'].transform(4326) # WSG84
            
            datapack['seconds']=seconds_from_start
            datapack['timestamp']=datum['time_mark']
            datapack['timestamp_rcv']=timeDataNow
            datapack['nextHop']=datum['nextHop']
            datapack['rssi']=0
    
            datapack['gps_precision']=datum['gps_precision']
            datapack['gps_itow']=datum['gps_itow']
            datapack['gps_heading']=datum['gps_heading']
            
            #grabo los valores RAW: FUCK!!!!!!!!!!!!!!
            datapack['gps_latitude'] = utm_point.y
            datapack['gps_longitude'] = utm_point.x
            
            datapack['bearing_avg']=datum['bearing_avg']
            datapack['bearing_std']=datum['bearing_std']
            
            datapack['voltage_batt_avg']=datum['voltage_batt_avg']
            datapack['voltage_batt_std']=datum['voltage_batt_std']
            
            datapack['amp_batt_avg']=datum['amp_batt_avg']
            datapack['amp_batt_std']=datum['amp_batt_std']
            
            datapack['pressure_avg']=datum['pressure_avg']
            datapack['pressure_std']=datum['pressure_std']
            
            datapack['ligth_avg']=datum['ligth_avg']
            datapack['ligth_std']=datum['ligth_std']
            
            datapack['accX_avg']=datum['accX_avg']
            datapack['accX_std']=datum['accX_std']
            
            datapack['accY_avg']=datum['accY_avg']
            datapack['accY_std']=datum['accY_std']
            
            datapack['accZ_avg']=datum['accZ_avg']
            datapack['accZ_std']=datum['accZ_std']
            
            datapack['gyrX_avg']=datum['gyrX_avg']
            datapack['gyrX_std']=datum['gyrX_std']
            
            datapack['gyrY_avg']=datum['gyrY_avg']
            datapack['gyrY_std']=datum['gyrY_std']
            
            datapack['gyrZ_avg']=datum['gyrZ_avg']
            datapack['gyrZ_std']=datum['gyrZ_std']
    
            #se acaboel Fuck, estaparte es fucional....
            
            #valores con transformacion: 
            calibration = self.calibrations[datum['Id_Code']]
            if calibration['accelerometer_x']:
                datapack['accX_si'] = calibration['accelerometer_x'].raw_to_SI(datum['accX_avg'])
                datapack['accX_coef'] =calibration['accelerometer_x']
            else:
                datapack['accX_si'] = datum['accX_avg']
                
            if calibration['accelerometer_y']:
                datapack['accY_si'] = calibration['accelerometer_y'].raw_to_SI(datum['accY_avg'])
                datapack['accY_coef'] =calibration['accelerometer_y']
            else:
                datapack['accY_si'] = datum['accY_avg']
            
            if calibration['accelerometer_z']:
                datapack['accZ_si'] = calibration['accelerometer_z'].raw_to_SI(datum['accZ_avg'])
                datapack['accZ_coef'] =calibration['accelerometer_z']
            else:
                datapack['accZ_si'] = datum['accZ_avg']
            ####################################################
            if calibration['gyroscope_x']:
                datapack['gyrX_si'] = calibration['gyroscope_x'].raw_to_SI(datum['gyrX_avg'])
                datapack['gyrX_coef'] =calibration['gyroscope_x']
            else:
                datapack['gyrX_si'] = datum['gyrX_avg']
                
            if calibration['gyroscope_y']:
                datapack['gyrY_si'] = calibration['gyroscope_y'].raw_to_SI(datum['gyrY_avg'])
                datapack['gyrY_coef'] =calibration['gyroscope_y']
            else:
                datapack['gyrY_si'] = datum['gyrY_avg']
            
            if calibration['gyroscope_z']:
                datapack['gyrZ_si'] = calibration['gyroscope_z'].raw_to_SI(datum['gyrZ_avg'])
                datapack['gyrZ_coef'] =calibration['gyroscope_z']
            else:
                datapack['gyrZ_si'] = datum['gyrZ_avg']
            ####################################################
            if calibration['pressure']:
                datapack['pressure_si'] = calibration['pressure'].raw_to_SI(datum['pressure_avg'])
                datapack['pressure_coef'] =calibration['pressure']
            else:
                datapack['pressure_si'] = datum['pressure_avg']
            ####################################################
            if calibration['voltage']:
                datapack['voltage_batt_si'] = calibration['voltage'].raw_to_SI(datum['voltage_batt_avg'])
                datapack['voltage_batt_coef'] =calibration['voltage']
            else:
                datapack['voltage_batt_si'] = datum['voltage_batt_avg']
                
            if calibration['amperes']:
                datapack['amp_batt_si'] = calibration['amperes'].raw_to_SI(datum['amp_batt_avg'])
                datapack['amp_batt_coef'] =calibration['amperes']
            else:
                datapack['amp_batt_si'] = datum['amp_batt_avg']
                
            ####################################################
            if calibration['ilumination']:
                datapack['ligth_si'] = calibration['ilumination'].raw_to_SI(datum['ligth_avg'])
                datapack['ligth_coef'] =calibration['ilumination']
            else:
                datapack['ligth_si'] = datum['ligth_avg']
            
    
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
                                         timestamp_rcv=datapack['timestamp_rcv'],
                                         nextHop=datapack['nextHop'],
                                         rssi=datapack['rssi'],
                                         
                                         geom=datapack['geom'],
                                         gps_precision=datapack['gps_precision'],
                                         gps_itow=datapack['gps_itow'],
                                         gps_longitude=datapack['gps_longitude'],
                                         gps_latitude=datapack['gps_latitude'],
                                         gps_heading=datapack['gps_heading'],
                                         
                                         voltage_batt_avg=datapack['voltage_batt_avg'],
                                         voltage_batt_std=datapack['voltage_batt_std'],
                                         voltage_batt_coef=datapack['voltage_batt_coef'],
                                         
                                         amp_batt_avg=datapack['amp_batt_avg'],
                                         amp_batt_std=datapack['amp_batt_std'],
                                         amp_batt_coef=datapack['amp_batt_coef'],
                                         
                                         pressure_avg=datapack['pressure_avg'],
                                         pressure_std=datapack['pressure_std'],
                                         pressure_coef=datapack['pressure_coef'],
                                         
                                         ligth_avg=datapack['ligth_avg'],
                                         ligth_std=datapack['ligth_std'],
                                         ligth_coef=datapack['ligth_coef'],
                                         
                                         accX_avg=datapack['accX_avg'],
                                         accX_std=datapack['accX_std'],
                                         accX_coef=datapack['accX_coef'],
                                         
                                         accY_avg=datapack['accY_avg'],
                                         accY_std=datapack['accY_std'],
                                         accY_coef=datapack['accY_coef'],
                                         
                                         accZ_avg=datapack['accZ_avg'],
                                         accZ_std=datapack['accZ_std'],
                                         accZ_coef=datapack['accZ_coef'],
                                         
                                         gyrX_avg=datapack['gyrX_avg'],
                                         gyrX_std=datapack['gyrX_std'],
                                         gyrX_coef=datapack['gyrX_coef'],
                                         
                                         gyrY_avg=datapack['gyrY_avg'],
                                         gyrY_std=datapack['gyrY_std'],
                                         gyrY_coef=datapack['gyrY_coef'],
                                         
                                         gyrZ_avg=datapack['gyrZ_avg'],
                                         gyrZ_std=datapack['gyrZ_std'],
                                         gyrZ_coef=datapack['gyrZ_coef'],
                                         
                                         
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
        try:
           DeviceDataRaw.objects.bulk_create(self.telemetry_items)
           self.telemetry_items = []
           
        except Exception as error:
            print ('An exception was thrown!')
            print (str(error))
            #self.write_error(self.telemetry_items)
            self.telemetry_items = []
            print ('Flush items!')
        
    def write_error(error_data):    
        with open(self.error_logfile, "a") as output_file:
            if type(error_data) is list:
                for item in error_data:
                    input_file.write(str(item)+'\n')
            else:
                input_file.write(str(error_data)+'\n')
        
        
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
                power = lastdata['voltage_batt_si']*lastdata['amp_batt_si']
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
                               'accY','accZ',
                               'ligth',
                               'power_volt','power_amp']
        
        out_js['barcos'] = []
        for key in self.devices_set:
            lastdata =self.datas[key][-1] #este es el ultimo
            dev = {}
            dev['nombre'] = self.node[key].name
            dev['color'] = self.trackings[key].get_color_html()
            dev['posicion'] = lastdata['ranking']
            power = lastdata['voltage_batt_si']*lastdata['amp_batt_si']
            dev['power'] =power
            dev['velocidad'] =lastdata['velocity']
            dev['direccion'] =lastdata['direction']
            
            dev['accX'] =lastdata['accX_si']
            dev['accY'] =lastdata['accY_si']
            dev['accZ'] =lastdata['accZ_si']
            
            dev['ligth'] =lastdata['ligth_si']
            
            dev['power_volt'] =lastdata['voltage_batt_si']
            dev['power_amp'] =lastdata['amp_batt_si']
            
            
            out_js['barcos'].append(dev)
            
        
        with open(self.log_pathdir+'/last_variables.json', 'w') as outfile:
            json.dump(out_js, outfile)
        
