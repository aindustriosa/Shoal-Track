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
        
        print(memory)
        start_race(memory)
        

##########################################
def create_organization(mem):
    '''sobre un diccionario, crea las organizaziones
    '''
    mem['organization'] = {}
    
    pathtotestimage= 'test_images/'
    ########[name,acronym,country,telephone,email,homepage,image]
    datas =[
            ['Organizacion','ORGNZT','Galicia','543678905','equipo@utmar.org','www.mi.com','organization.png'],
            ['Macana','CRVN','Montaña','543678905','ijia@iji.com','www.ht.com','cavern.png'],
            ['Tenebroso S.A.','TNBR','transilvania','23491913','ijia@avff.com','www.hsfv.org','tenebroso.png'],
            ['Makerlab','MKRL','Tomorrowland','9484838','ijia@adadca.es','www.adadca.es','maker.png'],
            ['Escuadron111','ES111','area51','543678905','ijia@iji.com','www.ht.com','es111.png'],
            ['PinkCat','PNKCT','Rosaland','543678905','ijia@iji.com','www.ht.com','pinkcat.png'],
            ['MetalSlug','MTLS','Arcade','543678905','ijia@iji.com','www.ht.com','metalslug.png'],
            ['La Mafia del Hormiguero','MFASA','Sicilia','543678905','ijia@iji.com','www.ht.com','mafia.png'],
            ['Paletos','PLTS','Arcansas','543678905','ijia@iji.com','www.ht.com','paletos.png'],
            ['DragsteR','DRGTS','California','543678905','ijia@iji.com','www.ht.com','dragster.png'],
            ['MountainPark','MNTPRK','Caurel','543678905','ijia@iji.com','www.ht.com','mountain.png'],
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
    datas =[['Rocomóvil',0,'ASRS01','El automóvil es un pedrusco gigante con ruedas. A veces los Hermanos Macana reconstruían su coche desde cero usando sus porras, a la vez que las usaban para potenciar su motor, el cual en algún momento se revela que está ocupado por una criatura viva.','boulder.png',600,4,3,3,mem['organization']['Macana'],[mem['contact']['Piedro'],mem['contact']['Roco']]],
            ['Espantomóvil',1,'ASRS02','Se trata de un coche con un pequeño campanario cuyo punto más alto está habitado por un dragón («con 1.000 llamaradas de fuerza») y varios fantasmas, vampiros, monstruos y brujas. El Espantomóvil es capaz de volar distancias cortas usando las alas del dragón.','creepy.png',1400,5,4,6,mem['organization']['Tenebroso S.A.'],[mem['contact']['Humanoide'],mem['contact']['Vampiro']]],
            ['Súper Convertible',2,'ASRS03','Su coche, que en principio tiene forma de barco con ruedas, es capaz de transformarse casi en cualquier cosa. Locovitch suele ayudar con sus innumerables inventos a los demás corredores a pasar por diversos obstáculos e impedimentos que, bien por causas naturales o bien por obra de Pierre, se presentan en la carrera. También los usa, a su vez, para atacar a sus rivales.','convert.png',1200,6,4,8,mem['organization']['Makerlab'],[mem['contact']['Pat']]],
            ['Stuka Rakuda',3,'ASRS04','Es un híbrido de coche y avión, capaz de volar limitadamente, normalmente lo justo para sobrepasar por encima de los corredores (individual o colectivamente) y los obstáculos que se presentan en su camino. El Stuka Rakuda también tiene montada una ametralladora, la cual es usada esporádicamente. La antigüedad del Stuka hace que el barón suela perder el control de su automóvil (e incluso su hélice), en diversas ocasiones. ','rakuda.png',800,5,6,3,mem['organization']['Escuadron111'],[mem['contact']['Hans']]],
            ['Compact Pussycat',4,'ASRS05','Es un coche femenino de color rosa sólo con accesorios maquilladores. Tales accesorios fallaban, actuando a veces como armas indirectas frente a los otros corredores; por ejemplo, haciendo que espuma de champú cayera sobre sus caras. Tiene un romance secreto con Pedro Bello, y siempre que está en apuros pide su ayuda, además de la de otros corredores','pussycat.png',500,3,3,2,mem['organization']['PinkCat'],[mem['contact']['Penélope']]],
            ['Súper Chatarra Special',5,'ASRS06','Es un vehículo militar, mitad tanque, mitad jeep. El Súper Chatarra Special hace uso de sus accesorios de tanque durante la carrera, cañón incluido. En ningún momento de la serie se mencionan los nombres propios de los pilotos en la edición española, conociéndoseles sólo como Sargento y Soldado. Pese a ser un vehículo robusto y potente','army.png',2000,5,4,6,mem['organization']['MetalSlug'],[mem['contact']['Sargento'],mem['contact']['Soldado']]],
            ['Antigualla Blindada',6,'ASRS07','un sedán de los años 1920 con consciencia de sí mismo. Su mejor baza para avanzar posiciones es la «Potencia de Fuga», consistente en que los pandilleros usen sus piernas para propulsar a la antigualla','bulletproof.png',1600,6,3,3,mem['organization']['La Mafia del Hormiguero'],[mem['contact']['Mafio'],mem['contact']['Luiggi'],mem['contact']['Petrus'],mem['contact']['Julius'],mem['contact']['Riggo'],mem['contact']['Antonio'],mem['contact']['Éolo']]],
            ['Alambique Veloz',0,'ASRS08','un carro de madera propulsado por una estufa de carbón. La estufa es el punto flaco del Alambique, cosa que los competidores aprovechan a su favor. Lucas emplea rudimentarias técnicas para avanzar en las carreras. Miedoso (haciendo honor a su nombre) teme todo lo que acontece en la carrera, poniendo a prueba (y a veces entorpeciendo) al buen Lucas','chuggabug.png',1100,4,3,3,mem['organization']['Paletos'],[mem['contact']['Luke'],mem['contact']['Blubber']]],
            ['Superheterodino',4,'ASRS09','Es un drag racer con dos grandes ruedas traseras, que suele caerse a pedazos debido a su alta fragilidad (aunque Bello lo niegue permanentemente).','turbo.png',450,6,2,1,mem['organization']['DragsteR'],[mem['contact']['Pedro']]],
            ['Troncoswagen',0,'ASRS10','una carreta de madera con sierras circulares en lugar de ruedas. Esto les da la habilidad de cortar casi cualquier cosa, dañando o destruyendo objetos. Son conductores muy agresivos y no dudan en rebanar en dos a su rival a la hora de adelantar. También emplean artefactos cortantes para abrirse paso por los obstáculos de la carrera.','troncoswagen.png',690,3,3,3,mem['organization']['MountainPark'],[mem['contact']['Rufus'],mem['contact']['Castor']]],
            ['Súper Perrari',7,'ASRS11','Se trata de un coche increíble a reacción, con cientos de armas ocultas. Intentan perjudicar lo máximo posible a sus competidores, con el único propósito de asegurarse la victoria. Esta obsesión de Pierre solía acarrearle una pérdida de tiempo valioso, haciéndole perder muchas posibles ocasiones de victoria.','mean.png',580,4,2,3,mem['organization']['Malvadiscos'],[mem['contact']['Dick'],mem['contact']['Perro']]],
            ['RaceMarkBuoy 01',100,'RMRK01','Marca virtual de posicion para la orientacion de la carrera','virtualbuoy.png',4,1,1,1,mem['organization']['Organizacion'],None],
            ['RaceMarkBuoy 02',100,'RMRK02','Marca virtual de posicion para la orientacion de la carrera','virtualbuoy.png',4,1,1,1,mem['organization']['Organizacion'],None],
            ['RaceMarkBuoy 03',101,'RMRK03','Marca de posicion para la orientacion de la carrera','racebuoy.png',4,1,1,1,mem['organization']['Organizacion'],None],
            ['RaceMarkBuoy 04',101,'RMRK04','Marca de posicion para la orientacion de la carrera','racebuoy.png',4,1,1,1,mem['organization']['Organizacion'],None],
            ['RaceMarkBuoy 05',101,'RMRK05','Marca de posicion para la orientacion de la carrera','racebuoy.png',4,1,1,1,mem['organization']['Organizacion'],None]
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
    data = ['Wacky Championship',1,'Campeonato mundial de autos locos',6,mem['organization']['Organizacion'],'champion_logo.png']
    try:
        last = Champion.objects.filter(name=data[0]).order_by('-id')[0]
        print('add new Champion Edition['+data[0]+']')
        v1 = Champion.objects.create(name=data[0],edicion=last.edicion+1,
                                    description=data[2],
                                    status=data[3],organization=data[4],
                                    image=pathtotestimage+data[5])
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
            ['Loiter race',1,'Carrera de maniobravilidad',4,mem['organization']['Organizacion'],'champion_1.jpg','SRID=4326;POLYGON((-8.846644163131712 42.124937073573435,-8.847110867500305 42.12416917925919,-8.844353556632996 42.12355246983276,-8.843570351600647 42.12459490419961,-8.846644163131712 42.124937073573435))'],
            ['Cross Speed race',1,'Carrera normal con trayectorias de cruze',4,mem['organization']['Organizacion'],'champion_2.jpg','SRID=4326;POLYGON((-8.846644163131712 42.124937073573435,-8.847110867500305 42.12416917925919,-8.844353556632996 42.12355246983276,-8.843570351600647 42.12459490419961,-8.846644163131712 42.124937073573435))'],
            ['Nocros Speed race',1,'Carrera normal sin trayectorias de cruze',4,mem['organization']['Organizacion'],'champion_2.jpg','SRID=4326;POLYGON((-8.846644163131712 42.124937073573435,-8.847110867500305 42.12416917925919,-8.844353556632996 42.12355246983276,-8.843570351600647 42.12459490419961,-8.846644163131712 42.124937073573435))'],
            ['Velocity race',1,'Carrera de velocidad',4,mem['organization']['Organizacion'],'champion_3.jpg','SRID=4326;POLYGON((-8.846644163131712 42.124937073573435,-8.847110867500305 42.12416917925919,-8.844353556632996 42.12355246983276,-8.843570351600647 42.12459490419961,-8.846644163131712 42.124937073573435))']
           ]
    for data in datas:
        posit = GEOSGeometry(data[6]) #units in WGS84
        posit.transform(32629)   # Transform to UTM29N
        try:
            last = Race.objects.filter(name=data[0]).order_by('-id')[0]
            print('add new Race Edition['+data[0]+']')
            
            v1 = Race.objects.create(name=data[0],edicion=last.edicion+1,description=data[2],
                                     status=data[3],organization=data[4],
                                     image=pathtotestimage+data[5],limit_area=posit)
        except:
            print('add new Race['+data[0]+']')
            v1 = Race.objects.create(name=data[0],edicion=data[1],description=data[2],
                                     status=data[3],organization=data[4],
                                     image=pathtotestimage+data[5],limit_area=posit)
        
        mem['races'][data[0]]= v1
    
    #meto las4 carreras en el campeonato
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Wacky Championship'],
                                                               race=mem['races']['Loiter race']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Wacky Championship'],
                                                             race=mem['races']['Loiter race'],order=1)
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Wacky Championship'],
                                                               race=mem['races']['Cross Speed race']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Wacky Championship'],
                                                             race=mem['races']['Cross Speed race'],order=2)
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Wacky Championship'],
                                                               race=mem['races']['Nocros Speed race']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Wacky Championship'],
                                                             race=mem['races']['Nocros Speed race'],order=3)
    try:
        v4 = ListTraceRaces.objects.filter(champion=mem['champion']['Wacky Championship'],
                                                               race=mem['races']['Velocity race']).get()
    except:
        v4 = ListTraceRaces.objects.create(champion=mem['champion']['Wacky Championship'],
                                                             race=mem['races']['Velocity race'],order=4)
    
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
            [mem['races']['Loiter race'],mem['devices']['RaceMarkBuoy 01'],0,0,'SRID=32629;POINT(512703.43 4663643.52)'],
            [mem['races']['Loiter race'],mem['devices']['RaceMarkBuoy 02'],1,0,'SRID=32629;POINT(512694.60 4663621.41)'],
            [mem['races']['Loiter race'],mem['devices']['RaceMarkBuoy 03'],6,1,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Loiter race'],mem['devices']['RaceMarkBuoy 04'],6,2,'SRID=32629;POINT(512721.21 4663616.82)'],
            [mem['races']['Loiter race'],mem['devices']['RaceMarkBuoy 05'],7,3,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Loiter race'],mem['devices']['RaceMarkBuoy 03'],3,4,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Loiter race'],mem['devices']['RaceMarkBuoy 05'],2,4,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Cross Speed race'],mem['devices']['RaceMarkBuoy 01'],0,0,'SRID=32629;POINT(512703.43 4663643.52)'],
            [mem['races']['Cross Speed race'],mem['devices']['RaceMarkBuoy 02'],1,0,'SRID=32629;POINT(512694.60 4663621.41)'],
            [mem['races']['Cross Speed race'],mem['devices']['RaceMarkBuoy 03'],6,1,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Cross Speed race'],mem['devices']['RaceMarkBuoy 05'],6,2,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Cross Speed race'],mem['devices']['RaceMarkBuoy 04'],7,3,'SRID=32629;POINT(512721.21 4663616.82)'],
            [mem['races']['Cross Speed race'],mem['devices']['RaceMarkBuoy 03'],2,4,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Cross Speed race'],mem['devices']['RaceMarkBuoy 05'],3,4,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Nocros Speed race'],mem['devices']['RaceMarkBuoy 01'],0,0,'SRID=32629;POINT(512703.43 4663643.52)'],
            [mem['races']['Nocros Speed race'],mem['devices']['RaceMarkBuoy 02'],1,0,'SRID=32629;POINT(512694.60 4663621.41)'],
            [mem['races']['Nocros Speed race'],mem['devices']['RaceMarkBuoy 03'],6,1,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Nocros Speed race'],mem['devices']['RaceMarkBuoy 05'],6,2,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Nocros Speed race'],mem['devices']['RaceMarkBuoy 04'],6,3,'SRID=32629;POINT(512721.21 4663616.82)'],
            [mem['races']['Nocros Speed race'],mem['devices']['RaceMarkBuoy 03'],2,4,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Nocros Speed race'],mem['devices']['RaceMarkBuoy 05'],3,4,'SRID=32629;POINT(512822.81 4663586.08)'],
            [mem['races']['Velocity race'],mem['devices']['RaceMarkBuoy 01'],0,0,'SRID=32629;POINT(512703.43 4663643.52)'],
            [mem['races']['Velocity race'],mem['devices']['RaceMarkBuoy 02'],1,0,'SRID=32629;POINT(512694.60 4663621.41)'],
            [mem['races']['Velocity race'],mem['devices']['RaceMarkBuoy 04'],4,1,'SRID=32629;POINT(512721.21 4663616.82)'],
            [mem['races']['Velocity race'],mem['devices']['RaceMarkBuoy 03'],2,2,'SRID=32629;POINT(512811.22 4663617.65)'],
            [mem['races']['Velocity race'],mem['devices']['RaceMarkBuoy 05'],3,2,'SRID=32629;POINT(512822.81 4663586.08)']
           ]
    
    #a cada carrera le meto sus marcas:
    for data in datas:
        posit = GEOSGeometry(data[4]) #units in UTM29N
        try:
            v2 = TrackGeom.objects.filter(race=data[0],device=data[1],track_pass=data[2],order=data[3]).get()
        
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
            [mem['devices']['Espantomóvil'],mem['races']['Loiter race'],'1234',0,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Rocomóvil'],mem['races']['Loiter race'],'1235',1,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Convertible'],mem['races']['Loiter race'],'1236',2,'va normal de potencia',mem['racecategory']['Test']],
            [mem['devices']['Stuka Rakuda'],mem['races']['Loiter race'],'1237',3,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Compact Pussycat'],mem['races']['Loiter race'],'1238',4,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Chatarra Special'],mem['races']['Loiter race'],'1239',5,'va normal de potencia',mem['racecategory']['Test']],
            [mem['devices']['Antigualla Blindada'],mem['races']['Loiter race'],'1240',6,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Alambique Veloz'],mem['races']['Loiter race'],'1241',7,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Superheterodino'],mem['races']['Loiter race'],'1242',8,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Troncoswagen'],mem['races']['Loiter race'],'1243',9,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Perrari'],mem['races']['Loiter race'],'1244',10,'va sobrado de potencia',mem['racecategory']['Test']],
            
            [mem['devices']['Espantomóvil'],mem['races']['Cross Speed race'],'1234',0,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Rocomóvil'],mem['races']['Cross Speed race'],'1235',1,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Convertible'],mem['races']['Cross Speed race'],'1236',2,'va normal de potencia',mem['racecategory']['Test']],
            [mem['devices']['Stuka Rakuda'],mem['races']['Cross Speed race'],'1237',3,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Compact Pussycat'],mem['races']['Cross Speed race'],'1238',4,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Chatarra Special'],mem['races']['Cross Speed race'],'1239',5,'va normal de potencia',mem['racecategory']['Test']],
            [mem['devices']['Antigualla Blindada'],mem['races']['Cross Speed race'],'1240',6,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Alambique Veloz'],mem['races']['Cross Speed race'],'1241',7,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Superheterodino'],mem['races']['Cross Speed race'],'1242',8,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Troncoswagen'],mem['races']['Cross Speed race'],'1243',9,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Perrari'],mem['races']['Cross Speed race'],'1244',10,'va sobrado de potencia',mem['racecategory']['Test']],
            
            [mem['devices']['Espantomóvil'],mem['races']['Nocros Speed race'],'1234',0,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Rocomóvil'],mem['races']['Nocros Speed race'],'1235',1,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Convertible'],mem['races']['Nocros Speed race'],'1236',2,'va normal de potencia',mem['racecategory']['Test']],
            [mem['devices']['Stuka Rakuda'],mem['races']['Nocros Speed race'],'1237',3,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Compact Pussycat'],mem['races']['Nocros Speed race'],'1238',4,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Chatarra Special'],mem['races']['Nocros Speed race'],'1239',5,'va normal de potencia',mem['racecategory']['Test']],
            [mem['devices']['Antigualla Blindada'],mem['races']['Nocros Speed race'],'1240',6,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Alambique Veloz'],mem['races']['Nocros Speed race'],'1241',7,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Superheterodino'],mem['races']['Nocros Speed race'],'1242',8,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Troncoswagen'],mem['races']['Nocros Speed race'],'1243',9,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Perrari'],mem['races']['Nocros Speed race'],'1244',10,'va sobrado de potencia',mem['racecategory']['Test']],
            
            [mem['devices']['Espantomóvil'],mem['races']['Velocity race'],'1234',0,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Rocomóvil'],mem['races']['Velocity race'],'1235',1,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Convertible'],mem['races']['Velocity race'],'1236',2,'va normal de potencia',mem['racecategory']['Test']],
            [mem['devices']['Stuka Rakuda'],mem['races']['Velocity race'],'1237',3,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Compact Pussycat'],mem['races']['Velocity race'],'1238',4,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Chatarra Special'],mem['races']['Velocity race'],'1239',5,'va normal de potencia',mem['racecategory']['Test']],
            [mem['devices']['Antigualla Blindada'],mem['races']['Velocity race'],'1240',6,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Alambique Veloz'],mem['races']['Velocity race'],'1241',7,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Superheterodino'],mem['races']['Velocity race'],'1242',8,'va sobrado de potencia',mem['racecategory']['Test']],
            [mem['devices']['Troncoswagen'],mem['races']['Velocity race'],'1243',9,'va justo de potencia',mem['racecategory']['Test']],
            [mem['devices']['Súper Perrari'],mem['races']['Velocity race'],'1244',10,'va sobrado de potencia',mem['racecategory']['Test']]
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
    vehicles =[mem['devices']['Espantomóvil'],
               mem['devices']['Rocomóvil'],
               mem['devices']['Súper Convertible'],
               mem['devices']['Stuka Rakuda'],
               mem['devices']['Compact Pussycat'],
               mem['devices']['Súper Chatarra Special'],
               mem['devices']['Antigualla Blindada'],
               mem['devices']['Alambique Veloz'],
               mem['devices']['Superheterodino'],
               mem['devices']['Troncoswagen'],
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
                  [12,0,None], #temperature_int
                  [13,0,None], #temperature_air
                  [14,0,None], #temperature_water
                  [15,3,None], #ilumination_fr
                  [16,3,None], #ilumination_fl
                  [17,3,None], #ilumination_br
                  [18,3,None], #ilumination_bl
                  [19,1,None], #voltage
                  [20,1,None], #amperes
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
            
