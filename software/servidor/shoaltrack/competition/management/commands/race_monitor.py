from django.core.management.base import BaseCommand

from django.utils import timezone
import time,sys

import threading #para el demonio de adquisiicon de datos serie

from competition.models import Race
from competition.monitoring import MonitoringRace

from telemetrydata.sources.gw_serial import SerialNode


class Command(BaseCommand):
    '''slug of the race
       source = path:port
                serial:/dev/ttyACM0:115200
                file:/home/igonzalez/test
                http://utmar.org:7000
                emulation:wecky
    '''
    args = '< name_slug@source >'
    help = 'Start monitoring Race'
    
    def add_arguments(self, parser):
        parser.add_argument('name_slug@source', type=str)
    
    def handle(self, *args, **options):
        
        #print(options)
        config = options['name_slug@source'].split('@')
        if not (len(config) ==2):
            print('No arguments complete: need name_slug@source')
            sys.exit()
        slug_race_name = config[0]
        source = config[1]
        
        #inicializo la gestion de la monitorizacion
        self.monitoring = MonitoringRace()
        self.monitoring.config_race(slug_race_name)
        
        #inicializo la fuente de datos de la telemetria
        self.telemetry_enable = False
        if  'emulation' in source:
            interface = source.split(':')[0]
            port = int(source.split(':')[1])
            
            #creo la 
            self.source_manager = None
        elif  'serial' in source:
            port = source.split(':')[1]
            baud = int(source.split(':')[2])
            self.source_manager = SerialNode(port,baud) #creo el bloque de control
            
        else:
            print('Error for source parameters: need name_slug@source')
            sys.exit()
            
        
        print('***************')
        #cominezo el campeonato:
        print('Start Monitoring Race: '+str(str(self.monitoring.race)))
        print('***************')
        
        self.monitoring.load_devices()
        print('Find Marks: ')
        print(self.monitoring.marks_set)
        print('Find Devices: ')
        print(self.monitoring.devices_set)
        
        #-- Lanzar el hilo que lee del puerto serie y guarda los datos procesados
        self.read_data = threading.Thread(target=self.source_manager.reader)
        
        code = True
        while code:
            try:
                status,code = self.update_race()
            
            except KeyboardInterrupt:
                break
            
            time.sleep(0.5)
        
        self.enable_telemetry(False)
        print('Exit Monitoring: Status: '+ status)
        
##########################################
##########################################


    def write_last_data(mem):
        '''Escribe en un fichero los ultimos datos para actualziar en clientes 
        '''
        
        return True


    def update_race(self):
        '''Vamosactualizando las acciones segun el estado:
        '''
        status,code = self.monitoring.update_status() #actualizo cada dos segundos (estado_verbose, stado_number)
        if code==Race.STATUS.abort:
            return status,False
        
        elif code in (Race.STATUS.propostal,Race.STATUS.desing):
            self.monitoring.config_race()
            self.enable_telemetry()
            count = self.source_manager.available_data()
            #print(count)
            for i in range(count):
                print(self.source_manager.get_line())
        
        elif code in (Race.STATUS.open,Race.STATUS.briefing):
            self.enable_telemetry()
            self.monitoring.load_devices()
            self.monitoring.update_calibration()
            self.monitoring.enable_log=True
        
        elif code == Race.STATUS.waiting:
            self.enable_telemetry() 
            self.monitoring.update_calibration()
            self.monitoring.enable_log=True
            #empiezo a coger datos
            for i in range(self.source_manager.available_data()):
                dict_datum = self.source_manager.get_line()
                print(dict_datum)
                self.monitoring.append_telemetry(dict_datum)
        
        elif code == Race.STATUS.launch:
            self.enable_telemetry() 
            self.monitoring.update_calibration()
            self.monitoring.enable_log=True
            #empiezo a coger datos
            for i in range(self.source_manager.available_data()):
                dict_datum = self.source_manager.get_line()
                print(dict_datum)
                self.monitoring.append_telemetry(dict_datum)
            
            #inicializo la carrear: start
            #inicializo contador-> puedo empezar a grabar output
        
        
        elif code == Race.STATUS.start:
            self.enable_telemetry() 
            self.monitoring.update_calibration()
            self.monitoring.enable_log=True
            #empiezo a coger datos
            for i in range(self.source_manager.available_data()):
                dict_datum = self.source_manager.get_line()
                print(dict_datum)
                self.monitoring.append_telemetry(dict_datum)
            
        
        elif code == Race.STATUS.middle:
            #grabo output
            #miro que psen por la boya dela manera correcta-> penalizacion
            #estoy aqui hasta que el primero llegue e la utltima boya
            pass
        elif code == Race.STATUS.ending:
            #grabo output
            #miro que psen por la boya dela manera correcta-> penalizacion
            #estoy aqui hasta que el primero lleguen todos al final
            pass
        elif code == Race.STATUS.finished:
            #sigo cogiendo datos
            pass
        elif code == Race.STATUS.deliberation:
            #paro de coger datos
            #muestro pagina de deliberacion
            #se puede ver ya el replay
            pass
        elif code == Race.STATUS.awards:
            #creo la pagina de los premios
            pass
        
        elif code == Race.STATUS.closed:
            #ya se pueden descargar los datos
            return status,False
        
        else:
            return status,False
        
        return status,True

        
    def enable_telemetry(self,enable=True):
        '''Activo la telemetria
        '''
        if (enable and (self.telemetry_enable == False)):
            self.source_manager.start()
            
            self.read_data.start()
            
            init_datum =self.source_manager.get_line()
            
            self.telemetry_enable = True
        
        elif not enable:
            self.telemetry_enable = False
            
            #-- Indicar al trhead the termine y esperar
            self.source_manager.stop_thread()
            
            self.read_data.join()
        
            self.source_manager.close()
