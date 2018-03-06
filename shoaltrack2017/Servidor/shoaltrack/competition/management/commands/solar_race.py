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
            ['Colegio Daniel Castelao','CDCEPS','Galicia','543678905','ijia@iji.com','www.ht.com','mafia.png'],
            ['Colegio Montecastelo','CMTCEP','Galicia','23491913','ijia@avff.com','www.hsfv.org','tenebroso.png'],
            ['Colegio Hogar','CHRCEPS','Galicia','9484838','ijia@adadca.es','www.adadca.es','maker.png'],
            ['Escuelas Proval','EPVCEP','Galicia','543678905','ijia@iji.com','www.ht.com','es111.png'],
            ['MarineInstruments','MARINST','Galicia','543678905','ijia@iji.com','www.ht.com','es111.png']
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
    datas =[['Piedro','Macana','macana','pmacana@mac.com','piedro_macana.png'],
            ['Roco','Macana','macanito','rmacana@mac.com','roco_macana.png'],
            ['Humanoide','Corpulento','giganton','hcorpul@mac.com','human.png'],
            ['Vampiro','Púrpura','vampi','vampi@mac.com','vamp.png'],
            ['Pat','Locovitch','profesor','plocovitch@mac.com','locovitch.png'],
            ['Hans','Fritz','red max','redmax@mac.com','hans.png'],
            ['Penélope','Glamour','pitstop','pglamour@mac.com','penelope.png'],
            ['Sargento','Blast','sargento','sblea@stmac.com','blast.png'],
            ['Soldado','Meekly','soldadito','meekly@mac.com','meekly.png'],
            ['Mafio','Hormin','mafio','mhormin@mac.com','mafio.png'],
            ['Luiggi','Hormin','cosquillas','lhormin@mac.com','mafio_1.png'],
            ['Petrus','Hormin','acero','phormin@mac.com','mafio_2.png'],
            ['Julius','Hormin','pequeñin','jhormin@mac.com','mafio_3.png'],
            ['Riggo','Hormin','escape','rhormin@mac.com','mafio_4.png'],
            ['Antonio','Hormin','gatillo','ahormin@mac.com','mafio_5.png'],
            ['Éolo','Hormin','risitas','ehormin@mac.com','mafio_6.png'],
            ['Luke','Granjer','granjero','lgranj@mac.com','luke.png'],
            ['Blubber','Bear','miedoso','bbear@mac.com','bear.png'],
            ['Pedro','Bello','pedrito','pbello@mac.com','bello.png'],
            ['Rufus','Ruffcut','Brutus','rruff@mac.com','brutus.png'],
            ['Castor','Sawtooth','Listus','csawtoo@mac.com','listus.png'],
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
    datas =[['DC Team',6,'ASRS03','Un bicasco con tradicional con motor encapsulado','boulder.png',
             600,4,3,3,mem['organization']['Colegio Daniel Castelao'],[mem['contact']['Piedro']]],
            ['Montecastelo Racing',0,'ASRS05','Un vehiculo estilo planeador de fibra.','creepy.png',
             1400,5,4,6,mem['organization']['Colegio Montecastelo'],[mem['contact']['Humanoide']]],
            ['Los apanados',1,'ASRS04','Un catamaran normal ','convert.png',
             1200,6,4,8,mem['organization']['Colegio Daniel Castelao'],[mem['contact']['Pat']]],
            ['Iluminados del Caribe',6,'ASRS06','Es un trimaran pequeñito','rakuda.png',
             800,5,6,3,mem['organization']['Colegio Montecastelo'],[mem['contact']['Hans']]],
            ['Hogar_1',6,'ASRS07','Es un trimaran con forma de vaina pod de star wars','pussycat.png',
             500,3,3,2,mem['organization']['Colegio Hogar'],[mem['contact']['Penélope']]],
            ['Hogar_2',1,'ASRS08','Un bicasco simple','army.png',
             2000,5,4,6,mem['organization']['Colegio Hogar'],[mem['contact']['Sargento'],mem['contact']['Soldado']]],
            ['Os Secos',0,'ASRS01','No se lo que es','bulletproof.png',
             1600,6,3,3,mem['organization']['Escuelas Proval'],[mem['contact']['Mafio'],mem['contact']['Luiggi']]],
            ['Naverga',0,'ASRS02','Otro wue no he id a visitar','chuggabug.png',
             1100,4,3,3,mem['organization']['Escuelas Proval'],[mem['contact']['Luke'],mem['contact']['Blubber']]],
            ['MarineDor',1,'ASRS09','Un bicaco con hidrofoil','turbo.png',
             450,6,2,1,mem['organization']['MarineInstruments'],[mem['contact']['Pedro']]],
            ['Vehiculo_Test_01',0,'ASRS10','Una persona con un sensor en la cabeza','troncoswagen.png',690,3,3,3,mem['organization']['Organizacion'],[mem['contact']['Rufus'],mem['contact']['Castor']]],
            ['Vehiculo_Test_02',1,'ASRS11','corriendo como pollos sin cabeza','mean.png',
             580,4,2,3,mem['organization']['Organizacion'],[mem['contact']['Dick'],mem['contact']['Perro']]],
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
    data = ['Regata Solar MarineInstruments',2,'Campeonato educacional de barcos propulsados por energia solar',6,mem['organization']['Organizacion'],'champion_logo.png']
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
            ['Carrera de pruebas',1,'Carrera de pruebas para probar conceptos',3,mem['organization']['Organizacion'],'champion_1.jpg','SRID=4326;POLYGON((-8.846644163131712 42.124937073573435,-8.847110867500305 42.12416917925919,-8.844353556632996 42.12355246983276,-8.843570351600647 42.12459490419961,-8.846644163131712 42.124937073573435))'],
            ['Carrera de Maniobrabilidad',1,'Carrera normal con trayectorias de cruze',3,mem['organization']['Organizacion'],'champion_1.jpg','SRID=4326;POLYGON((-8.846644163131712 42.124937073573435,-8.847110867500305 42.12416917925919,-8.844353556632996 42.12355246983276,-8.843570351600647 42.12459490419961,-8.846644163131712 42.124937073573435))'],
            ['Carrera de velocidad',1,'Una carrera de velocidad en linea recta',3,mem['organization']['Organizacion'],'champion_2.jpg','SRID=4326;POLYGON((-8.846644163131712 42.124937073573435,-8.847110867500305 42.12416917925919,-8.844353556632996 42.12355246983276,-8.843570351600647 42.12459490419961,-8.846644163131712 42.124937073573435))'],
            ['Carrera de Resistencia',1,'Carrera normal sin trayectorias de cruze',4,mem['organization']['Organizacion'],'champion_3.jpg','SRID=4326;POLYGON((-8.846644163131712 42.124937073573435,-8.847110867500305 42.12416917925919,-8.844353556632996 42.12355246983276,-8.843570351600647 42.12459490419961,-8.846644163131712 42.124937073573435))']
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
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Regata Solar MarineInstruments'],
                                                               race=mem['races']['Carrera de pruebas']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Regata Solar MarineInstruments'],
                                                             race=mem['races']['Carrera de pruebas'],order=1)
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Regata Solar MarineInstruments'],
                                                               race=mem['races']['Carrera de Maniobrabilidad']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Regata Solar MarineInstruments'],
                                                             race=mem['races']['Carrera de Maniobrabilidad'],order=2)
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Regata Solar MarineInstruments'],
                                                               race=mem['races']['Carrera de velocidad']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Regata Solar MarineInstruments'],
                                                             race=mem['races']['Carrera de velocidad'],order=3)
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Regata Solar MarineInstruments'],
                                                               race=mem['races']['Carrera de Resistencia']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Regata Solar MarineInstruments'],
                                                             race=mem['races']['Carrera de Resistencia'],order=4)
    
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
            [mem['races']['Carrera de pruebas'],mem['devices']['VirtualMarkBuoy 01'],0,0,'SRID=32629;POINT(512703.43 4663643.52)'],
            [mem['races']['Carrera de pruebas'],mem['devices']['VirtualMarkBuoy 02'],1,0,'SRID=32629;POINT(512694.60 4663621.41)'],
            [mem['races']['Carrera de pruebas'],mem['devices']['RaceMarkBuoy 01'],13,1,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Carrera de pruebas'],mem['devices']['RaceMarkBuoy 02'],17,2,'SRID=32629;POINT(512721.21 4663616.82)'],
            [mem['races']['Carrera de pruebas'],mem['devices']['RaceMarkBuoy 03'],13,3,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Carrera de pruebas'],mem['devices']['RaceMarkBuoy 03'],2,4,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Carrera de pruebas'],mem['devices']['RaceMarkBuoy 01'],3,4,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Carrera de pruebas'],mem['devices']['GatewayMark 01'],200,5,'SRID=32629;POINT(512703.43 4663643.52)'],
            
            [mem['races']['Carrera de Maniobrabilidad'],mem['devices']['VirtualMarkBuoy 01'],0,0,'SRID=32629;POINT(512703.43 4663643.52)'],
            [mem['races']['Carrera de Maniobrabilidad'],mem['devices']['VirtualMarkBuoy 02'],1,0,'SRID=32629;POINT(512694.60 4663621.41)'],
            [mem['races']['Carrera de Maniobrabilidad'],mem['devices']['RaceMarkBuoy 03'],13,1,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Carrera de Maniobrabilidad'],mem['devices']['RaceMarkBuoy 02'],17,2,'SRID=32629;POINT(512721.21 4663616.82)'],
            [mem['races']['Carrera de Maniobrabilidad'],mem['devices']['RaceMarkBuoy 01'],13,3,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Carrera de Maniobrabilidad'],mem['devices']['RaceMarkBuoy 03'],3,4,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Carrera de Maniobrabilidad'],mem['devices']['RaceMarkBuoy 01'],2,4,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Carrera de Maniobrabilidad'],mem['devices']['GatewayMark 01'],200,5,'SRID=32629;POINT(512703.43 4663643.52)'],
            
            [mem['races']['Carrera de velocidad'],mem['devices']['VirtualMarkBuoy 01'],0,0,'SRID=32629;POINT(512703.43 4663643.52)'],
            [mem['races']['Carrera de velocidad'],mem['devices']['VirtualMarkBuoy 02'],1,0,'SRID=32629;POINT(512694.60 4663621.41)'],
            [mem['races']['Carrera de velocidad'],mem['devices']['RaceMarkBuoy 03'],3,1,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Carrera de velocidad'],mem['devices']['RaceMarkBuoy 01'],2,1,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Carrera de velocidad'],mem['devices']['GatewayMark 01'],200,2,'SRID=32629;POINT(512703.43 4663643.52)'],
            
            
            [mem['races']['Carrera de Resistencia'],mem['devices']['VirtualMarkBuoy 01'],0,0,'SRID=32629;POINT(512703.43 4663643.52)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['VirtualMarkBuoy 02'],1,0,'SRID=32629;POINT(512694.60 4663621.41)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['RaceMarkBuoy 01'],13,1,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['RaceMarkBuoy 03'],13,2,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['RaceMarkBuoy 02'],17,3,'SRID=32629;POINT(512721.21 4663616.82)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['RaceMarkBuoy 01'],13,4,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['RaceMarkBuoy 03'],13,5,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['RaceMarkBuoy 02'],17,6,'SRID=32629;POINT(512721.21 4663616.82)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['RaceMarkBuoy 03'],3,7,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['RaceMarkBuoy 01'],2,7,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Carrera de Resistencia'],mem['devices']['GatewayMark 01'],200,8,'SRID=32629;POINT(512703.43 4663643.52)']
            
           ]
    
    #a cada carrera le meto sus marcas:
    for data in datas:
        posit = GEOSGeometry(data[4]) #units in UTM29N
        try:
            v2 = TrackGeom.objects.filter(race=data[0],device=data[1],track_pass=data[2],order=data[3]).get()
            if v2.device.acronym =='GTWN01':
                v2.geom=GEOSGeometry('SRID=32629;POINT(512670.42 4663667.96)') #units in UTM29N
                v2.save()
        
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
            [mem['devices']['DC Team'],mem['races']['Carrera de pruebas'],'ASRS03',0,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Montecastelo Racing'],mem['races']['Carrera de pruebas'],'ASRS05',1,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Los apanados'],mem['races']['Carrera de pruebas'],'ASRS04',2,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Iluminados del Caribe'],mem['races']['Carrera de pruebas'],'ASRS06',3,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Hogar_1'],mem['races']['Carrera de pruebas'],'ASRS07',4,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Hogar_2'],mem['races']['Carrera de pruebas'],'ASRS08',5,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Os Secos'],mem['races']['Carrera de pruebas'],'ASRS01',6,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Naverga'],mem['races']['Carrera de pruebas'],'ASRS02',7,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['MarineDor'],mem['races']['Carrera de pruebas'],'ASRS09',8,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Vehiculo_Test_01'],mem['races']['Carrera de pruebas'],'ASRS10',9,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Vehiculo_Test_02'],mem['races']['Carrera de pruebas'],'ASRS11',10,'Un barquito',mem['racecategory']['Senior']],
            
            [mem['devices']['DC Team'],mem['races']['Carrera de Maniobrabilidad'],'ASRS03',0,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Montecastelo Racing'],mem['races']['Carrera de Maniobrabilidad'],'ASRS05',1,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Los apanados'],mem['races']['Carrera de Maniobrabilidad'],'ASRS04',2,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Iluminados del Caribe'],mem['races']['Carrera de Maniobrabilidad'],'ASRS06',3,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Hogar_1'],mem['races']['Carrera de Maniobrabilidad'],'ASRS07',4,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Hogar_2'],mem['races']['Carrera de Maniobrabilidad'],'ASRS08',5,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Os Secos'],mem['races']['Carrera de Maniobrabilidad'],'ASRS01',6,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Naverga'],mem['races']['Carrera de Maniobrabilidad'],'ASRS02',7,'Un barquito',mem['racecategory']['Senior']],
            
            [mem['devices']['DC Team'],mem['races']['Carrera de velocidad'],'ASRS03',0,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Montecastelo Racing'],mem['races']['Carrera de velocidad'],'ASRS05',1,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Los apanados'],mem['races']['Carrera de velocidad'],'ASRS04',2,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Iluminados del Caribe'],mem['races']['Carrera de velocidad'],'ASRS06',3,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Hogar_1'],mem['races']['Carrera de velocidad'],'ASRS07',4,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Hogar_2'],mem['races']['Carrera de velocidad'],'ASRS08',5,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Os Secos'],mem['races']['Carrera de velocidad'],'ASRS01',6,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Naverga'],mem['races']['Carrera de velocidad'],'ASRS02',7,'Un barquito',mem['racecategory']['Senior']],
            
            [mem['devices']['DC Team'],mem['races']['Carrera de Resistencia'],'ASRS03',0,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Montecastelo Racing'],mem['races']['Carrera de Resistencia'],'ASRS05',1,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Los apanados'],mem['races']['Carrera de Resistencia'],'ASRS04',2,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Iluminados del Caribe'],mem['races']['Carrera de Resistencia'],'ASRS06',3,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Hogar_1'],mem['races']['Carrera de Resistencia'],'ASRS07',4,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Hogar_2'],mem['races']['Carrera de Resistencia'],'ASRS08',5,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Os Secos'],mem['races']['Carrera de Resistencia'],'ASRS01',6,'Un barquito',mem['racecategory']['Senior']],
            [mem['devices']['Naverga'],mem['races']['Carrera de Resistencia'],'ASRS02',7,'Un barquito',mem['racecategory']['Senior']],
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
    vehicles =[mem['devices']['DC Team'],
               mem['devices']['Montecastelo Racing'],
               mem['devices']['Los apanados'],
               mem['devices']['Iluminados del Caribe'],
               mem['devices']['Hogar_1'],
               mem['devices']['Hogar_2'],
               mem['devices']['Os Secos'],
               mem['devices']['Naverga'],
               mem['devices']['MarineDor'],
               mem['devices']['Vehiculo_Test_01'],
               mem['devices']['Vehiculo_Test_02']]
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
    print('Start Championship: '+str(mem['champion']['Wacky Championship']))
    mem['champion']['Wacky Championship'].status = Champion.STATUS.middle
    mem['champion']['Wacky Championship'].save()
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
            
