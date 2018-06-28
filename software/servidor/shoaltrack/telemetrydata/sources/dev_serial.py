#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''Demonio de control de nodos de la plataforma ShoalTrack
   Solo lee el puerto serie y trasnforna los datos NMEA a sus respectivos valores
'''

import serial

from telemetrydata.schemas.shtrack import gpstime_parse,text_parse
from telemetrydata.schemas.shtrack import vaisala_parse,race_solar_mi_2_parse

class SerialNode:
    
    def __init__(self,source,baud):
        
        self.source = source
        if baud:
            self.baudrate = baud
        else:
            self.baudrate = 115200 #alta velocidad 115200, 57600, 38400
        self.serialLink = None
        self.enable_thread = False #variable de finalizacion de trheats
        
        self.packets_Rx =[] #buffer de lineas parseadas
        self.schemas ={} #los tipos de schemas posibles
        
    def add_schema(self,schema):
        self.schemas[schema['name']] = schema
        
        
    def start(self,):
        # Check your COM port and baud rate and configure IMU
        self.serialLink = serial.Serial() #solo creo la instancia del puerto serie control arduimu
        self.serialLink.baudrate = self.baudrate
        self.serialLink.port= self.source
        self.serialLink.timeout = 1
        try:
            self.serialLink.open()
            
        except serial.SerialException:
            #-- Error al abrir el puerto serie
            print ('Error al abrir puerto: ' + str(self.serialLink.port))
            return False
        
        return True
    
    def stop_thread(self,):
        self.enable_thread = False
    
    def close(self,):
        ''' Cierra el puerto serie de comunicacion
        '''
        if self.serialLink:
            self.serialLink.close()
        
    def get_rawline(self,parse=False):
        '''Bucle de lectura de datos del puerto serie
        '''
        if not self.enable_thread:
            line = self.serialLink.readline() # recojo la linea nueva, EOL=\n
            if not parse:
                return line
            else:
                return self.parseLine(line)
        
        else:
            print('Puerto ocupado: Demonio de lectura activo')
            
    
    def reader(self,):
        '''Bucle de lectura de datos del puerto serie
        '''
        print('Enable Serial Thread...')
        self.enable_thread = True
        while self.enable_thread:
            line = self.serialLink.readline() # recojo la linea nueva, EOL=\n
            #print(line)
            
            line = line.decode("utf-8")
            if not line:
                continue
            
            if ((line[0] == '#') or (line[0] == '$')):
                datum = self.parseLine(line) #parseo la linea
                if datum:
                    self.packets_Rx.append(datum) #la meto en el buffer
    
    def parseLine(self,line):
        
        """Parses an sentence (NMEA and SAPM), sets fields in the global structure.
           Raises an AssertionError if the checksum does not validate.
           Returns the type of sentence that was parsed.
        """
		
        # Get rid of the \r\n if it exists
        #quita todos los caracteres que no son "texto visible" a partir del FINAL del string (al inicio no los quita)
        line = line.rstrip()
        
        line = line.split(',')#separo cada bloque de comas
        
        #comprobacion del schema:
        for schema in self.schemas.keys():
            if line[self.schemas[schema]['Id_packet'][0]] == self.schemas[schema]['Id_packet'][1]: #identifica el Id
                
                if schema == 'gpstime':
                    return gpstime_parse(line)
                elif schema == 'debug':
                    return text_parse(line)
                elif schema == 'rsmi2':
                    return race_solar_mi_2_parse(line)
                elif schema == 'vaisala':
                    return vaisala_parse(line)
        
        
    def get_line(self):
        if self.packets_Rx:
            return self.packets_Rx.pop()

        
    def available_data(self):
        if self.packets_Rx:
            return len(self.packets_Rx)
        else:
            return 0


####################################
#programa central del modulo neuralLink
if __name__ == "__main__":
    import threading
    #from ..schemas.shtrack import gpstime_schema
    schema ={'name':'gpstime',
             'Id_packet':[1,'5']
            }
    
    data_module = SerialNode('/dev/ttyACM0',115200) #creo el bloque de control
    
    data_module.start()
    
    data_module.add_schema(schema)
    
    #-- Lanzar el hilo que lee del puerto serie y guarda los datos procesados
    read_data = threading.Thread(target=data_module.reader)
    read_data.start()
    
    while True:
        try:
            output =data_module.get_line()
            if output:
                print(output)
        except KeyboardInterrupt:
            break
    
    #-- Indicar al trhead the termine y esperar
    data_module.stop_thread()
    read_data.join()
        
    data_module.close()
        
        
    
    
