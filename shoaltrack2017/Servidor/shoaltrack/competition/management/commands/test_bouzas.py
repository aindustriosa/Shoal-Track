from django.core.management.base import BaseCommand

from datetime import timedelta
import time

from django.contrib.gis.geos import GEOSGeometry

from django.contrib.auth.models import User
from profiles.models import Contact,Organization,Monitor
from devices.models import Device, TeamTrace
from competition.models import Race, TrackGeom, Champion,ListTraceRaces, RaceTracking,Penalty,RaceTrackingNode,PenaltyTracking,RaceCategory
from telemetrydata.models import DeviceDataRaw,DataProcessing

from competition.emulation import wacky_test
from configobj import ConfigObj

from competition.monitoring import MonitoringRace
from telemetrydata.packethandle import decode_packet

class Command(BaseCommand):
    args = '<table_id table_id ...>'
    help = 'Start simulation une race in a championship'

    def handle(self, *args, **options):
        print('Inicialize tables...')
        memory = {}
        memory = create_organization(memory)
        memory = create_contacts(memory)
        memory = create_devices(memory)
        
        
        
        memory = create_champion(memory)
        memory = create_race(memory)
        memory = create_category_race(memory)
        memory = create_tracks(memory)
        
        memory = create_drivers(memory)
        create_calibrations(memory)
        
        #print(memory)
        #start_race(memory)
        

##########################################
def create_organization(mem):
    '''sobre un diccionario, crea las organizaziones
    '''
    mem['organization'] = {}
    
    pathtotestimage= 'test_images/'
    ########[name,acronym,country,telephone,email,homepage,image]
    datas =[
            ['Organizacion','ORGNZT','Galicia','543678905','equipo@utmar.org','www.mi.com','organization.png'],
            ['La Mafia del Hormiguero','MFASA','Sicilia','543678905','ijia@iji.com','www.ht.com','mafia.png'],
            ['Makerlab','MKRL','Tomorrowland','9484838','ijia@adadca.es','www.adadca.es','maker.png'],
            ['Malvadiscos','MLVDS','Pesadilla','543678905','ijia@iji.com','www.ht.com','malevolo.png']
           ]
    for data in datas:
        try:
            v1 = Organization.objects.filter(acronym=data[1]).get()
        except:
            print('add new Organization['+data[0]+']')
            v1 = Organization.objects.create(name=data[0],acronym=data[1],country=data[2],
                                                                telephone=data[3],email=data[4],
                                                                homepage=data[5],image=pathtotestimage+data[6])
            
        mem['organization'][data[0]]= v1
    
    return mem

def create_contacts(mem):
    '''sobre un diccionario, crea los contactos
    '''
    mem['contact'] = {}
    
    pathtotestimage= 'test_images/'
    ########[fisrt_name,last_name,acronym,email,image]
    datas =[['Pat','Locovitch','profesor','plocovitch@mac.com','locovitch.png'],
            ['Mafio','Hormin','mafio','mhormin@mac.com','mafio.png'],
            ['Luiggi','Hormin','cosquillas','lhormin@mac.com','mafio_1.png'],
            ['Petrus','Hormin','acero','phormin@mac.com','mafio_2.png'],
            ['Julius','Hormin','pequeñin','jhormin@mac.com','mafio_3.png'],
            ['Riggo','Hormin','escape','rhormin@mac.com','mafio_4.png'],
            ['Antonio','Hormin','gatillo','ahormin@mac.com','mafio_5.png'],
            ['Éolo','Hormin','risitas','ehormin@mac.com','mafio_6.png'],
            ['Dick','Dastardly','Nodoyuna','dnodoyuna@mac.com','pierre.png'],
            ['Perro','Muttley','Patán','ppatan@mac.com','patan.png']
           ]
    for data in datas:
        try:
            v1 = Contact.objects.filter(acronym=data[2]).get()
        except:
            print('add new Contact['+data[0]+']')
            v1 = Contact.objects.create(fisrt_name=data[0],last_name=data[1],
                                        acronym=data[2],
                                        email=data[3],image=pathtotestimage+data[4])
            
        mem['contact'][data[0]]= v1
    
    return mem


def create_devices(mem):
    '''sobre un diccionario, crea las organizaziones
    '''
    mem['devices'] = {}
    
    pathtotestimage= 'test_images/'
    ########[name,category,acronym,description,image,weight,length,sleeve,draft,owner,team]
    datas =[
            ['Súper Convertible',2,'ASRS09','Su coche, que en principio tiene forma de barco con ruedas, es capaz de transformarse casi en cualquier cosa. Locovitch suele ayudar con sus innumerables inventos a los demás corredores a pasar por diversos obstáculos e impedimentos que, bien por causas naturales o bien por obra de Pierre, se presentan en la carrera. También los usa, a su vez, para atacar a sus rivales.','convert.png',1200,6,4,8,mem['organization']['Makerlab'],[mem['contact']['Pat']]],
            ['Antigualla Blindada',6,'ASRS10','un sedán de los años 1920 con consciencia de sí mismo. Su mejor baza para avanzar posiciones es la «Potencia de Fuga», consistente en que los pandilleros usen sus piernas para propulsar a la antigualla','bulletproof.png',1600,6,3,3,mem['organization']['La Mafia del Hormiguero'],[mem['contact']['Mafio'],mem['contact']['Luiggi'],mem['contact']['Petrus'],mem['contact']['Julius'],mem['contact']['Riggo'],mem['contact']['Antonio'],mem['contact']['Éolo']]],
            ['Súper Perrari',7,'ASRS11','Se trata de un coche increíble a reacción, con cientos de armas ocultas. Intentan perjudicar lo máximo posible a sus competidores, con el único propósito de asegurarse la victoria. Esta obsesión de Pierre solía acarrearle una pérdida de tiempo valioso, haciéndole perder muchas posibles ocasiones de victoria.','mean.png',580,4,2,3,mem['organization']['Malvadiscos'],[mem['contact']['Dick'],mem['contact']['Perro']]],
            ['VirtualMarkBuoy 01',100,'VMRK01','Marca virtual de posicion para el inicio de la carrera','virtualbuoy.png',4,1,1,1,mem['organization']['Organizacion'],None],
            ['VirtualMarkBuoy 02',100,'VMRK02','Marca virtual de posicion para el inicio de la carrera','virtualbuoy.png',4,1,1,1,mem['organization']['Organizacion'],None],
            ['RaceMarkBuoy 01',101,'RMRK01','Marca de posicion para la orientacion de la carrera','racebuoy.png',4,1,1,1,mem['organization']['Organizacion'],None],
            ['RaceMarkBuoy 02',101,'RMRK02','Marca de posicion para la orientacion de la carrera','racebuoy.png',4,1,1,1,mem['organization']['Organizacion'],None],
            ['RaceMarkBuoy 03',101,'RMRK03','Marca de posicion para la orientacion de la carrera','racebuoy.png',4,1,1,1,mem['organization']['Organizacion'],None],
            ['GatewayMark 01',102,'GTWN01','Zona donde esta el concentrador principal','gate.png',4,1,1,1,mem['organization']['Organizacion'],None]
           ]
    for data in datas:
        #añado los dispositivos
        try:
            v1 = Device.objects.filter(acronym=data[2]).get()
        except:
            print('add new Device['+data[0]+']')
            v1 = Device.objects.create(name=data[0],category=data[1],acronym=data[2],
                                       description=data[3],image=pathtotestimage+data[4],
                                       weight=data[5],length=data[6],
                                       sleeve=data[7],draft=data[8],owner=data[9])
            
            if data[10]:
                for contact in data[10]:
                    v2 = TeamTrace.objects.create(device=v1,contact=contact,
                                                  rol=8)
                
            
        mem['devices'][data[0]]= v1
    
    return mem


def create_champion(mem):
    '''sobre un diccionario, crea un campeonato
    '''
    mem['champion'] = {}
    
    pathtotestimage= 'test_images/'
    data = ['Campeonato de pollos sin cabeza',1,'Campeonato test de pruebas..',6,mem['organization']['Organizacion'],'champion_logo.png']
    try:
        v1 = Champion.objects.filter(name=data[0]).order_by('-id')[0]
    except:
        print('add new Champion['+data[0]+']')
        v1 = Champion.objects.create(name=data[0],edicion=data[1],
                                    description=data[2],
                                    status=data[3],organization=data[4],
                                    image=pathtotestimage+data[5])
    
    mem['champion'][data[0]]= v1
    
    return mem

def create_race(mem):
    '''sobre un diccionario, crea un campeonato
    '''
    mem['races'] = {}
    
    pathtotestimage= 'test_images/'
    ########[name,edicion,description,status,organization,image]
    datas =[
            ['Carrera de pruebas A',1,'Carrera de pruebas para probar conceptos',3,mem['organization']['Organizacion'],'champion_1.jpg','SRID=4326;POLYGON((-8.75309944152832 42.22743770535969,-8.752402067184448 42.22757673428881,-8.751940727233887 42.22660749766682,-8.752718567848206 42.22634135221978,-8.75309944152832 42.22743770535969))'],
            ['Carrera de pruebas B',2,'Carrera de pruebas para probar conceptos',3,mem['organization']['Organizacion'],'champion_1.jpg','SRID=4326;POLYGON((-8.75309944152832 42.22743770535969,-8.752402067184448 42.22757673428881,-8.751940727233887 42.22660749766682,-8.752718567848206 42.22634135221978,-8.75309944152832 42.22743770535969))'],
            ['Carrera de pruebas C',3,'Carrera de pruebas para probar conceptos',3,mem['organization']['Organizacion'],'champion_1.jpg','SRID=4326;POLYGON((-8.75309944152832 42.22743770535969,-8.752402067184448 42.22757673428881,-8.751940727233887 42.22660749766682,-8.752718567848206 42.22634135221978,-8.75309944152832 42.22743770535969))'],
            ['Carrera de pruebas D',4,'Carrera de pruebas para probar conceptos',3,mem['organization']['Organizacion'],'champion_1.jpg','SRID=4326;POLYGON((-8.75309944152832 42.22743770535969,-8.752402067184448 42.22757673428881,-8.751940727233887 42.22660749766682,-8.752718567848206 42.22634135221978,-8.75309944152832 42.22743770535969))']
           ]
    for data in datas:
        posit = GEOSGeometry(data[6]) #units in WGS84
        posit.transform(32629)   # Transform to UTM29N
        try:
            v1 = Race.objects.filter(name=data[0]).order_by('-id')[0]
        except:
            print('add new Race['+data[0]+']')
            v1 = Race.objects.create(name=data[0],edicion=data[1],description=data[2],
                                     status=data[3],organization=data[4],
                                     image=pathtotestimage+data[5],limit_area=posit)
        
        mem['races'][data[0]]= v1
    
    #meto las4 carreras en el campeonato
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Campeonato de pollos sin cabeza'],
                                                               race=mem['races']['Carrera de pruebas A']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Campeonato de pollos sin cabeza'],
                                                             race=mem['races']['Carrera de pruebas A'],order=1)
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Campeonato de pollos sin cabeza'],
                                                               race=mem['races']['Carrera de pruebas B']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Campeonato de pollos sin cabeza'],
                                                             race=mem['races']['Carrera de pruebas B'],order=2)
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Campeonato de pollos sin cabeza'],
                                                               race=mem['races']['Carrera de pruebas C']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Campeonato de pollos sin cabeza'],
                                                             race=mem['races']['Carrera de pruebas C'],order=3)
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Campeonato de pollos sin cabeza'],
                                                               race=mem['races']['Carrera de pruebas D']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Campeonato de pollos sin cabeza'],
                                                             race=mem['races']['Carrera de pruebas D'],order=4)
    
    return mem

def create_category_race(mem):
    mem['racecategory'] = {}
    
    ########[name,code,description]
    datas =[['Test','TST','Categoría No oficial para pruebas'],
            ['Junior','JNR','Categoría de menores de 16 años'],
            ['Senior','SNR','Categoría mayores de 16 años'],
            ['Open','OPN','Categoría abierta a todo el mundo']
           ]
    for data in datas:
        try:
            v1 = RaceCategory.objects.filter(code=data[1]).get()
        except:
            print('add new RaceCategory['+data[0]+']')
            v1 = RaceCategory.objects.create(name=data[0],
                                             code=data[1],
                                             description=data[2])
            
        mem['racecategory'][data[0]]= v1
    
    return mem

def create_tracks(mem):
    mem['tracks'] = {}
    ########[race,edicion,device,track_pass,order]
    datas =[
            [mem['races']['Carrera de pruebas A'],mem['devices']['VirtualMarkBuoy 01'],0,0,'SRID=4326;POINT(-8.752426207065582 42.227302251141445)'],
            [mem['races']['Carrera de pruebas A'],mem['devices']['VirtualMarkBuoy 02'],1,0,'SRID=4326;POINT(-8.75262200832367 42.227282389798255)'],
            [mem['races']['Carrera de pruebas A'],mem['devices']['RaceMarkBuoy 01'],14,1,'SRID=4326;POINT(-8.752431571483612 42.22688516162199)'],
            [mem['races']['Carrera de pruebas A'],mem['devices']['RaceMarkBuoy 02'],14,2,'SRID=4326;POINT(-8.752624690532684 42.22687324473809)'],
            [mem['races']['Carrera de pruebas A'],mem['devices']['RaceMarkBuoy 03'],16,3,'SRID=4326;POINT(-8.752793669700623 42.22723869482122)'],
            [mem['races']['Carrera de pruebas A'],mem['devices']['VirtualMarkBuoy 01'],2,4,'SRID=4326;POINT(-8.752426207065582 42.227302251141445)'],
            [mem['races']['Carrera de pruebas A'],mem['devices']['VirtualMarkBuoy 02'],3,4,'SRID=4326;POINT(-8.75262200832367 42.227282389798255)'],
            [mem['races']['Carrera de pruebas A'],mem['devices']['GatewayMark 01'],200,5,'SRID=4326;POINT(-8.751417696475983 42.22759222601028)'],
            
            [mem['races']['Carrera de pruebas B'],mem['devices']['VirtualMarkBuoy 01'],0,0,'SRID=4326;POINT(-8.752426207065582 42.227302251141445)'],
            [mem['races']['Carrera de pruebas B'],mem['devices']['VirtualMarkBuoy 02'],1,0,'SRID=4326;POINT(-8.75262200832367 42.227282389798255)'],
            [mem['races']['Carrera de pruebas B'],mem['devices']['RaceMarkBuoy 01'],14,1,'SRID=4326;POINT(-8.752431571483612 42.22688516162199)'],
            [mem['races']['Carrera de pruebas B'],mem['devices']['RaceMarkBuoy 02'],14,2,'SRID=4326;POINT(-8.752624690532684 42.22687324473809)'],
            [mem['races']['Carrera de pruebas B'],mem['devices']['RaceMarkBuoy 03'],16,3,'SRID=4326;POINT(-8.752793669700623 42.22723869482122)'],
            [mem['races']['Carrera de pruebas B'],mem['devices']['VirtualMarkBuoy 01'],2,4,'SRID=4326;POINT(-8.752426207065582 42.227302251141445)'],
            [mem['races']['Carrera de pruebas B'],mem['devices']['VirtualMarkBuoy 02'],3,4,'SRID=4326;POINT(-8.75262200832367 42.227282389798255)'],
            [mem['races']['Carrera de pruebas B'],mem['devices']['GatewayMark 01'],200,5,'SRID=4326;POINT(-8.751417696475983 42.22759222601028)'],
            
            [mem['races']['Carrera de pruebas C'],mem['devices']['VirtualMarkBuoy 01'],0,0,'SRID=4326;POINT(-8.752426207065582 42.227302251141445)'],
            [mem['races']['Carrera de pruebas C'],mem['devices']['VirtualMarkBuoy 02'],1,0,'SRID=4326;POINT(-8.75262200832367 42.227282389798255)'],
            [mem['races']['Carrera de pruebas C'],mem['devices']['RaceMarkBuoy 01'],14,1,'SRID=4326;POINT(-8.752431571483612 42.22688516162199)'],
            [mem['races']['Carrera de pruebas C'],mem['devices']['RaceMarkBuoy 02'],14,2,'SRID=4326;POINT(-8.752624690532684 42.22687324473809)'],
            [mem['races']['Carrera de pruebas C'],mem['devices']['RaceMarkBuoy 03'],16,3,'SRID=4326;POINT(-8.752793669700623 42.22723869482122)'],
            [mem['races']['Carrera de pruebas C'],mem['devices']['VirtualMarkBuoy 01'],2,4,'SRID=4326;POINT(-8.752426207065582 42.227302251141445)'],
            [mem['races']['Carrera de pruebas C'],mem['devices']['VirtualMarkBuoy 02'],3,4,'SRID=4326;POINT(-8.75262200832367 42.227282389798255)'],
            [mem['races']['Carrera de pruebas C'],mem['devices']['GatewayMark 01'],200,5,'SRID=4326;POINT(-8.751417696475983 42.22759222601028)'],
            
            
            [mem['races']['Carrera de pruebas D'],mem['devices']['VirtualMarkBuoy 01'],0,0,'SRID=4326;POINT(-8.752426207065582 42.227302251141445)'],
            [mem['races']['Carrera de pruebas D'],mem['devices']['VirtualMarkBuoy 02'],1,0,'SRID=4326;POINT(-8.75262200832367 42.227282389798255)'],
            [mem['races']['Carrera de pruebas D'],mem['devices']['RaceMarkBuoy 01'],14,1,'SRID=4326;POINT(-8.752431571483612 42.22688516162199)'],
            [mem['races']['Carrera de pruebas D'],mem['devices']['RaceMarkBuoy 02'],14,2,'SRID=4326;POINT(-8.752624690532684 42.22687324473809)'],
            [mem['races']['Carrera de pruebas D'],mem['devices']['RaceMarkBuoy 03'],16,3,'SRID=4326;POINT(-8.752793669700623 42.22723869482122)'],
            [mem['races']['Carrera de pruebas D'],mem['devices']['VirtualMarkBuoy 01'],2,4,'SRID=4326;POINT(-8.752426207065582 42.227302251141445)'],
            [mem['races']['Carrera de pruebas D'],mem['devices']['VirtualMarkBuoy 02'],3,4,'SRID=4326;POINT(-8.75262200832367 42.227282389798255)'],
            [mem['races']['Carrera de pruebas D'],mem['devices']['GatewayMark 01'],200,5,'SRID=4326;POINT(-8.751417696475983 42.22759222601028)'],
            
           ]
    
    #a cada carrera le meto sus marcas:
    for data in datas:
        posit = GEOSGeometry(data[4]) #units in WGS84
        posit.transform(32629)   # Transform to UTM29N
        try:
            v2 = TrackGeom.objects.filter(race=data[0],device=data[1],track_pass=data[2],order=data[3]).get()
            #if v2.device.acronym =='GTWN01':
            #    v2.geom=GEOSGeometry('SRID=32629;POINT(512670.42 4663667.96)') #units in UTM29N
            #    v2.save()
        
        except:
            v2 = TrackGeom.objects.create(race=data[0],device=data[1],track_pass=data[2],order=data[3],geom=posit)
            
    return mem

def create_drivers(mem):
    '''sobre un diccionario, crea un campeonato
    '''
    mem['RaceTracking'] = {}
    
    pathtotestimage= 'test_images/'
    ########[device,race,code,color,observations]
    datas =[
            [mem['devices']['Súper Convertible'],mem['races']['Carrera de pruebas A'],'ASRS09',0,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Antigualla Blindada'],mem['races']['Carrera de pruebas A'],'ASRS10',1,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Súper Perrari'],mem['races']['Carrera de pruebas A'],'ASRS11',2,'Un barquito',mem['racecategory']['Senior']],
            
            [mem['devices']['Súper Convertible'],mem['races']['Carrera de pruebas B'],'ASRS09',0,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Antigualla Blindada'],mem['races']['Carrera de pruebas B'],'ASRS10',1,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Súper Perrari'],mem['races']['Carrera de pruebas B'],'ASRS11',2,'Un barquito',mem['racecategory']['Senior']],
            
            [mem['devices']['Súper Convertible'],mem['races']['Carrera de pruebas C'],'ASRS09',0,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Antigualla Blindada'],mem['races']['Carrera de pruebas C'],'ASRS10',1,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Súper Perrari'],mem['races']['Carrera de pruebas C'],'ASRS11',2,'Un barquito',mem['racecategory']['Senior']],
            
            [mem['devices']['Súper Convertible'],mem['races']['Carrera de pruebas D'],'ASRS09',0,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Antigualla Blindada'],mem['races']['Carrera de pruebas D'],'ASRS10',1,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Súper Perrari'],mem['races']['Carrera de pruebas D'],'ASRS11',2,'Un barquito',mem['racecategory']['Senior']]
           ]
    
    for data in datas:
        try:
            v2 = RaceTracking.objects.filter(device=data[0],race=data[1],code=data[2]).get()
        
        except:
            v2 = RaceTracking.objects.create(device=data[0],race=data[1],code=data[2],color=data[3],observations=data[4],category=data[5])
        try:
            mem['RaceTracking'][data[1].name][data[0].acronym]= v2
        except:
            mem['RaceTracking'][data[1].name] = {}
            mem['RaceTracking'][data[1].name][data[0].acronym]= v2
    
    return mem


def create_calibrations(mem):
    '''sobre un diccionario, crea las calibraciones
    '''
    vehicles =[mem['devices']['Súper Convertible'],
               mem['devices']['Antigualla Blindada'],
               mem['devices']['Súper Perrari']]
    #parameter;ecuation;const
    calibrations=[[0,0,None], #longitud
                  [1,0,None], #latitud
                  [2,1,None], #accelerometer_x
                  [3,1,None], #accelerometer_y
                  [4,1,None], #accelerometer_z
                  [5,1,None], #gyroscope_x
                  [6,1,None], #gyroscope_y
                  [7,1,None], #gyroscope_z
                  [8,1,None], #magnetometer_x
                  [9,1,None], #magnetometer_y
                  [10,1,None], #magnetometer_z
                  [11,1,None], #pressure
                  [12,1,[0.01,0]], #temperature_int
                  [13,1,[0.01,0]], #temperature_air
                  [14,1,[0.01,0]], #temperature_water
                  [15,3,None], #ilumination_fr
                  [16,3,None], #ilumination_fl
                  [17,3,None], #ilumination_br
                  [18,3,None], #ilumination_bl
                  [19,1,[0.023866,-0.0000118]], #voltage
                  [20,1,[0.050934,-26.04537]], #amperes
                  [21,0,None], #modulo vietno
                  [22,0,None], #direcion viento
                  [23,0,None] #humedad relativa
                  ]
               
    for vehicle in vehicles:
        for calibr in calibrations:
        
            v2 = DataProcessing.objects.create(device=vehicle,
                                               type_equation=calibr[1],
                                               type_param=calibr[0])
            v2.set_args(calibr[2])
            v2.save()
        


def start_race(mem):
    '''
    simulacion de un campeonato:
    '''
    print('***************')
    #cominezo el campeonato:
    print('Start Championship: '+str(mem['champion']['Campeonato de pollos sin cabeza']))
    mem['champion']['Campeonato de pollos sin cabeza'].status = Champion.STATUS.middle
    mem['champion']['Campeonato de pollos sin cabeza'].save()
    print('***************')
    
    
    #para cada carrera:
    for race in mem['races'].keys():
        print('###############')
        print(str(mem['races'][race]))
        mem['races'][race].status = Race.STATUS.open
        mem['races'][race].save()
        print('\tStatus de Carrera: '+mem['races'][race].get_status())#paso a briefing:(validacion por parte de juez)
        time.sleep(2)
        
        #cambio el estado: (validacion por parte de juez)
        mem['races'][race].status = Race.STATUS.briefing
        mem['races'][race].save()
        print('\tStatus de Carrera: '+mem['races'][race].get_status())
        time.sleep(2)
        
        #Lanzo la gestion de la monitorizacion de la carrera:
        #muestro los barcos participantes:
        monit = MonitoringRace()
        monit.config_race(mem['races'][race])
        print('\tConfiguracion de la carrera: '+str(monit.race))
        print('\tConfiguracion del campeonato: '+str(monit.champion_ref))
        print('\tConfiguracion del track: '+str(monit.tracks))
        
        
        monit.load_devices()
        print('\tBarcos Participantes:')
        for driver in monit.trackings:
            print('\t\t'+str(driver.device))
            
        #cambio el estado: (todos a la linea de salida)
        monit.change_race_status(Race.STATUS.waiting)
        print('\tStatus de Carrera: '+monit.race.get_status())
        time.sleep(2)
        
        
        #cargo los datos del simulador de la carrera:
        virtual_hardware = [] #doden se instancias todos los dispositivos virutales
        settings = ConfigObj('competition/emulation/settings.conf', encoding="ISO-8859-1")
        for item in settings['buoy_order']:
            virtual_hardware.append((item,wacky_test.HIL_Device(settings['devices'][item])))
        
        for item in settings['ship_order']:
            virtual_hardware.append((item,wacky_test.HIL_Device(settings['devices'][item])))

        for item in virtual_hardware:
            packet = item[1].get_packet()
            packet = decode_packet(packet,'WackyTestRace')
            monit.append_telemetry(packet)
        
        monit.commit_data()
        
        #################################################
        #cambio el estado: (cuenta atras de 30 segundos)
        monit.change_race_status(Race.STATUS.launch)
        print('\tStatus de Carrera: '+monit.race.get_status())
        
        for i in range(10):
            for item in virtual_hardware:
                item[1].update('start')
                packet = item[1].get_packet()
                packet = decode_packet(packet,'WackyTestRace')
                monit.append_telemetry(packet)
        
            monit.commit_data()
                
            time.sleep(0.2)
        
        #################################################
        #cambio el estado: (cominezo de carrera)
        monit.change_race_status(Race.STATUS.start)
        print('\tStatus de Carrera: '+monit.race.get_status())
        time.sleep(3)
        
        for i in range(1000):
            for item in virtual_hardware:
                item[1].update('start')
                packet = item[1].get_packet()
                packet = decode_packet(packet,'WackyTestRace')
                monit.append_telemetry(packet)
        
            monit.commit_data()
                
            time.sleep(1)
        
        #cambio el estado: (cominezo de carrera)
        monit.change_race_status(Race.STATUS.closed)
        print('\tStatus de Carrera: '+monit.race.get_status())
            
