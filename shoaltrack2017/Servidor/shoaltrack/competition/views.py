from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django_tables2   import RequestConfig

from competition.models import Race, TrackGeom, Champion,ListTraceRaces,RaceTracking
from telemetrydata.models import DeviceDataRaw,DataProcessing

from competition.tables import parse_championship_device,parse_championship_team

# Create your views here.

from sys import getsizeof

def summary(request, championship_slug=False):
    '''
    '''
    #recojo el campeonato
    try:
        qChampion = Champion.objects.filter(slug=championship_slug).get()
    except:
        return HttpResponse("No find Champioship entry.")
    
    
    output = str(qChampion)
    
    
    return HttpResponse(output)
    
def detail(request, championship_slug=False):
    '''
    '''
    #recojo el campeonato
    try:
        qChampion = Champion.objects.filter(slug=championship_slug).get()
    except:
        return HttpResponse("No find Champioship entry.")
    
    #su lista de carreras:
    champion_refs = ListTraceRaces.objects.filter(champion=qChampion).order_by('order').select_related("race")
    
    race_list = []
    race_detail = []
    for item in champion_refs:
        race_list.append(str(item.race))
        
        race = {}
        race['name'] = str(item.race)
        race['description'] = item.race.description
        race['timestamp_start'] = str(item.race.timestamp_start)
        race['status'] = item.race.get_status()
        race['image_tag'] = item.race.image_tag()
        
        race['geom'] =[]
        qTrackGeom = TrackGeom.objects.filter(race=item.race).order_by('order').select_related("device")
        for qTrack in qTrackGeom:
            track = {}
            track['codigo'] = qTrack.device.acronym
            track['image_tag'] = qTrack.device.image_tag()
            track['order'] = qTrack.order
            track['track_pass'] = qTrack.get_pass()
            track['geojson'] = qTrack.geom_JSN()
            
            race['geom'].append(track)
            
        race_detail.append(race)
    
    
    print(race_list)
    print(race_detail)
    
    
    
    
def devices(request, championship_slug=False):
    '''
    '''
    #recojo el campeonato
    try:
        qChampion = Champion.objects.filter(slug=championship_slug).get()
    except:
        return HttpResponse("No find Champioship entry.")
    
    print (str(qChampion))
    
    #su lista de carreras:
    champion_refs = ListTraceRaces.objects.filter(champion=qChampion).order_by('order').select_related("race")
    
    #de cada carrera, los dispositvos:
    list_devices = []
    
    name_devices = []
    qTrackDevices = []
    for item in champion_refs:
        #obtengo el traking de los dispositivos de la carrera
        qTrackings =RaceTracking.objects.filter(race=item.race
                                            ).select_related('category','device')
        
        for qTracking in qTrackings:
            if not str(qTracking.device) in  name_devices:
                qTrackDevices.append(qTracking)
                name_devices.append(str(qTracking.device))
                list_devices.append(parse_championship_device(qTracking.device))
                
    
    #para cada dispositivo:
    #   sus porpiedades,
    #   su porpietario
    #   sus integrantes
    
    content_to_html = {'devices':list_devices,
                       }

    return render(request, 'champion_device.html', {'content': content_to_html})
    
    
    
    
def teams(request, championship_slug=False):
    '''
    '''
    #recojo el campeonato
    try:
        qChampion = Champion.objects.filter(slug=championship_slug).get()
    except:
        return HttpResponse("No find Champioship entry.")
    
    #su lista de carreras:
    champion_refs = ListTraceRaces.objects.filter(champion=qChampion).order_by('order').select_related("race")
    
    #de cada carrera, los dispositvos:
    list_teams = []
    
    name_devices = []
    qTrackDevices = []
    for item in champion_refs:
        #obtengo el traking de los dispositivos de la carrera
        qTrackings =RaceTracking.objects.filter(race=item.race
                                            ).select_related('category','device')
        
        for qTracking in qTrackings:
            if not str(qTracking.device) in  name_devices:
                qTrackDevices.append(qTracking)
                name_devices.append(str(qTracking.device))
                list_teams.append(parse_championship_team(qTracking.device))
    
    
    
    content_to_html = {'teams':list_teams,
                       }

    return render(request, 'champion_team.html', {'content': content_to_html})
    
    
def adwars(request, championship_slug=False):
    '''
    '''
    #recojo el campeonato
    try:
        qChampion = Champion.objects.filter(slug=championship_slug).get()
    except:
        return HttpResponse("No find Champioship entry.")
    
    #su lista de carreras:
    champion_refs = ListTraceRaces.objects.filter(champion=qChampion).order_by('order').select_related("race")
    
    #de cada carrera, los dispositvos:
    list_races = ['Vehículo','Total'] #['total',name1,naem2,...]
    dev_results = {} #'name':[point1,point2....],name2:[,]
    
    count_race = 1 #para saber cuantas carreras voy teniendo
    for item_race in champion_refs:
        list_races.append(item_race.race.name)
        
        #obtengo el traking de los dispositivos de la carrera
        qTrackings =RaceTracking.objects.filter(race=item_race.race
                                            ).select_related('category','device')
        
        for qTracking in qTrackings:
            try:
                dev_results[qTracking.device.name].append(0)
            except:
                dev_results[qTracking.device.name] = []
                for i in range(count_race):
                    dev_results[qTracking.device.name].append(0)
                    
            dev_results[qTracking.device.name][count_race-1] = qTracking.get_points()
            
        count_race += 1 #incremento la cuenta de la carrera
        
        
    #sumo los tottales y genero el row de la tabla:
    #list_races.append('total')
    points=[]
    for dev_name in dev_results.keys():
        total = 0
        dev_point = [dev_name,0] #nombre y total
        for point in dev_results[dev_name]:
            dev_point[1] += point # los sumo al total
            dev_point.append(point) #lo añado al order
        
        points.append(dev_point)
        
    
    #los ordeno por puntuacion total:
    points = sorted(points, reverse=True, key=lambda ptemp: ptemp[1])   # sort by points
    
    results = {'races':list_races,
               'points':points}
    
    
    print(results)
    content_to_html = {'races':list_races,
                       'points':points
                       }

    return render(request, 'champion_adwars.html', {'content': content_to_html})
    
    
    
    
def adward_results(request, slug=False):
    '''
    maqueto la pagina de mostrar resultados del campeonato, con sus premios
    '''
    
def champion_results(request, slug=False):
    '''
    maqueto la pagina de mostrar resultados del campeonato
    '''
    
def race_results(request, slug=False):
    '''
    maqueto la pagina de mostrar resultados de la carrera
    '''

def node_results(request, code=False):
    '''
    maqueto la pagina de mostrar resultados de un vehuclo en particular
    '''
    
def update_data(request, service=False):
    '''
    actualizo las variables de entorno y genero los archivos .js estaticos
    '''
    
def last_data(request, championship_slug=False,amount=None):
    '''
    obtengo los ultimos datos del campeonato: la ultima carrera activa.
    '''
    if not amount:
        amount =1
    else:
        amount =int(amount)
    
    #obtengo la carrera activa:
    try:
        qListRaces = ListTraceRaces.objects.filter(champion__slug=championship_slug,
                                                                            is_enable=True).order_by('-order').select_related('race')
    except:
        return HttpResponse("No find Races in this champion.")
    
    #obtengo la carrera que estaempezada en waiting
    for qListRace in qListRaces:
        if qListRace.race.status > 4:
            qRace = qListRace.race
            break
        else:
            qRace = None
    
    if not qRace:
        return HttpResponse("No find Active Race.")
    
    #obtengo sus marcas delimitadores y su trayecto por orden ascendente
    qTracks = TrackGeom.objects.filter(race=qRace).order_by('order').select_related("device")
    
    #obtengo el traking de los dispositivos de la carrera
    qTrackings =RaceTracking.objects.filter(race=qRace
                                            ).select_related('category','device')
    
    #para cada dispositvo obtengo los X datos anerioriores y sus sus coeficientes:
    qDatas = []
    
    live_data={'time_array':[],'code_id':[],'type':[],'name':[],'color':[],'color_name':[],
                      'ranking':[],'power':[],'velocity':[],'position':[],'direcction':[]}
    for qTracking in qTrackings:
        '''
        qDatasByDevice = DeviceDataRaw.objects.filter(device=qTracking.device,
                                                   timestamp__gte=qRace.timestamp_start,
                                                   timestamp__lt=qRace.timestamp_finish).order_by('-timestamp').select_related('accX_coef','accY_coef','accZ_coef',
                                                                                              'gyrX_coef','gyrY_coef','gyrZ_coef',
                                                                                              'magX_coef','magY_coef','magZ_coef',
                                                                                              'press_air_coef',
                                                                                              'temp_int_coef','temp_air_coef','temp_water_coef',
                                                                                              'ldr_fr_coef','ldr_fl_coef','ldr_br_coef','ldr_bl_coef',
                                                                                              'power_volt_coef','power_amp_coef')[:amount]
        '''
        #sin select_related 1,1seg //con select_related 2,2seg
        qDatasByDevice = DeviceDataRaw.objects.filter(device=qTracking.device,
                                                  timestamp__gte=qRace.timestamp_start,
                                                  timestamp__lt=qRace.timestamp_finish).order_by('-timestamp')[:amount]
                                                   
        qDatas.append(qDatasByDevice)
        live_data['code_id'].append(qTracking.code)
        live_data['type'].append(qTracking.device.get_type())
        live_data['name'].append(qTracking.device.name)
        live_data['color_name'].append(qTracking.get_color())
        live_data['color'].append(qTracking.get_color_html())
        
        array_position = []
        array_time = []
        array_power =[]
        array_direcction =[]
        array_ranking =[]
        array_velocity =[]
        for qData in reversed(qDatasByDevice):
            pos = [qData.longitude(WGS84=True),qData.latitude(WGS84=True)]
            array_position.append(pos)
            
            seconds_from_start = (qData.timestamp-qRace.timestamp_start).seconds
            array_time.append(seconds_from_start)
            
            power = qData.power_volt*qData.power_amp
            array_power.append(power)
            
            direcction = qData.ldr_fr_raw
            array_direcction.append(direcction)
            
            velocity = qData.ldr_fl_raw
            array_velocity.append(velocity)
            
            ranking = qData.accX_raw
            array_ranking.append(ranking)
            
        live_data['position'].append(array_position)
        live_data['time_array'].append(array_time)
        live_data['power'].append(array_power)
        live_data['direcction'].append(array_direcction)
        live_data['ranking'].append(array_ranking)
        live_data['velocity'].append(array_velocity)
        
        
    
    #genero tabla .js
    #print(qDatas)
    
    graph_data={}
    dev_name=[]
    dev_type =[]
    dev_color_html =[]
    dev_color_name =[]
    for qTrack in qTracks:
        dev_name.append(qTrack.device.name)
        dev_type.append(qTrack.device.get_type())
    graph_data['name']=dev_name
    graph_data['type']=dev_type
    
    
    output ='var graph_data={'
    output +='name:' + str(graph_data['name'])
    output +=',type:' + str(graph_data['type'])
    output +='}'
    
    
    out_js ='var live_data={'
    for key in live_data.keys():
        out_js +=key+ ':' + str(live_data[key])+','
    
    out_js = out_js[:-1] #lequit oel ultimo(la coma)
    out_js +='}'
    
    
    out_js = '{'
    out_js +='"raceDate":"{:%d/%m/%Y %H:%M:%S}",'.format(qRace.timestamp_start)
    out_js +='"raceName":"{}",'.format(str(qRace))
    out_js +='"status":"{}",'.format(qRace.get_status())
    out_js +='"windDirection":"{}",'.format(23)
    out_js +='"windIntensity":"{}",'.format(34)
    
    out_js +='}'
    
    
    print('Memory size of file.js: ',getsizeof(out_js)/1024,'Kbytes')
    
    return HttpResponse(out_js)

def last_telemetry(request, championship_slug=False):
    '''
    obtengo el ultimo dato del campeonato de la ultima carrera activa.
    '''
    #obtengo la carrera activa:
    try:
        qListRaces = ListTraceRaces.objects.filter(champion__slug=championship_slug,
                                                   is_enable=True).order_by('-order').select_related('race')
    except:
        return HttpResponse("No find Races in this champion.")
    
    #obtengo la carrera que estaempezada en waiting
    for qListRace in qListRaces:
        if qListRace.race.status > 4:
            qRace = qListRace.race
            break
        else:
            qRace = None
    
    if not qRace:
        return HttpResponse("No find Active Race.")
    
    #calcular la hora de la que voy a pedir los datos:
    #si la carrera ha erminado (status>x)->cojo la fecha de finalizacion 
    #sino, cojo la fecha actual como referencia
    #calculo los segundos sobre el inicio de carrera... (pueden ser negativos si la carrera no ha empezado
    
    
    
    
    #obtengo sus marcas delimitadores y su trayecto por orden ascendente
    qTrackGeoms = TrackGeom.objects.filter(race=qRace).order_by('order').select_related("device")
    
    race_marks = []
    for qTrackGeom in qTrackGeoms:
        mark ='{'
        mark += '"nombre":"{}",'.format(qTrackGeom.device.name)
        mark += '"tipo":"{}",'.format(qTrackGeom.device.get_type())
        mark += '"localizacion":[{}]'.format('-8.89,42.988')
        mark +='}'
        
        race_marks.append(mark)
    
    #obtengo el traking de los dispositivos de la carrera
    race_devs = []
    qTrackings =RaceTracking.objects.filter(race=qRace
                                            ).select_related('category','device')
    for qTracking in qTrackings:
        dev ='{'
        dev += '"nombre":"{}",'.format(qTracking.device.name)
        dev += '"tipo":"{}",'.format(qTracking.device.get_type())
        dev += '"color":"{}",'.format(qTracking.get_color_html())
        dev += '"nombreColor":"{}",'.format(qTracking.get_color())
        
        #busco el ultimo dato perteneciente a la carrera (entre tiemosqueesta asociadoala carrera)
        if not qTracking.timestamp_exit:
            qData = DeviceDataRaw.objects.filter(device=qTracking.device,
                                                  timestamp__gte=qTracking.timestamp_integrate).order_by('-timestamp')[0]
        else:
            qData = DeviceDataRaw.objects.filter(device=qTracking.device,
                                                  timestamp__gte=qTracking.timestamp_integrate,
                                                  timestamp__lt=qTracking.timestamp_exit).order_by('-timestamp')[0]
        
        seconds_from_start = (qData.timestamp-qRace.timestamp_start).seconds
        
        dev += '"posicion":{},'.format(qData.ranking)
        
        power = qData.get_unit_SI('power_volt')*qData.get_unit_SI('power_amp')
        dev += '"power":{},'.format(power)
        
        dev += '"velocidad":{},'.format(qData.velocity)
        dev += '"direccion":{},'.format(qData.direcction)
        dev += '"localizacion":[{},{}]'.format(qData.longitude(WGS84=True),
                                                                qData.latitude(WGS84=True))
        
        dev +='}'
        
        race_devs.append(dev)
        
        
    
    
    
    out_js = '{'
    out_js +='"raceDate":"{:%d/%m/%Y %H:%M:%S}",'.format(qRace.timestamp_start)
    out_js +='"raceName":"{}",'.format(str(qRace))
    out_js +='"time":"{}",'.format(seconds_from_start)
    out_js +='"status":"{}",'.format(qRace.get_status())
    out_js +='"windDirection":{},'.format(23)
    out_js +='"windIntensity":{},'.format(34)
    
    out_js +='"barcos":['
    out_js +=','.join(race_devs)
    out_js +=']'
    
    out_js +='"boyas":['
    out_js +=','.join(race_marks)
    out_js +=']'
    
    out_js +='}'
    
    
    print('Memory size of file.js: ',getsizeof(out_js)/1024,'Kbytes')
    
    return HttpResponse(out_js)
