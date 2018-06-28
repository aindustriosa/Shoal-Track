 
from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry
from decimal import Decimal
    
def decode_packet(packet,schema):
    '''
    '''
    new_packet = []
    
    
        
    if schema == 'WackyTestRace':
        #['ASRS08', '0', '-8.846398926608215', ' 42.12475324015704', '1018', '602', '0', '28', '87', '0', '-16', '-6', '34', '49', '5', '729', '957', '1366', '11', ' 50', ' 16', ' 114']

        packet = packet.replace('#','')
        packet = packet.replace('(','')
        packet = packet.replace(')','')
        packet = packet.replace('[','')
        packet = packet.replace(']','')
        
        datum = packet.split(',')
        
        point = 'SRID=4326;POINT('+datum[2]+' '+ datum[3]+')'
        posit = GEOSGeometry(point) #units in WGS84
        posit.transform(32629)   # Transform to UTM29N
        
        #de id to device:
        new_packet.append(datum[0]) # codigo de Nodo
        new_packet.append(timezone.now()) # timestamp
        new_packet.append(posit) # posicion gemoetrica
        new_packet.append(int(datum[1])) # Node milisec
        
        new_packet.append(Decimal(datum[2])) # Node longitude_raw 
        new_packet.append(Decimal(datum[3])) # Node latitude_raw
        
        new_packet.append(int(datum[4])) # Node power_volt
        new_packet.append(int(datum[5])) # Node power_amp
        
        new_packet.append(int(datum[6])) # Node accX_raw
        new_packet.append(int(datum[7])) # Node accY_raw
        new_packet.append(int(datum[8])) # Node accZ_raw
        new_packet.append(int(datum[9])) # Node gyrX_raw
        new_packet.append(int(datum[10])) # Node gyrY_raw
        new_packet.append(int(datum[11])) # Node gyrZ_raw
        new_packet.append(int(datum[12])) # Node magX_raw
        new_packet.append(int(datum[13])) # Node magY_raw
        new_packet.append(int(datum[14])) # Node magZ_raw
        new_packet.append(int(datum[15])) # Node press_air_raw
        new_packet.append(int(datum[16])) # Node temp_air_raw
        new_packet.append(int(datum[17])) # Node temp_water_raw
        new_packet.append(int(datum[18])) # Node ldr_fr_raw
        new_packet.append(int(datum[19])) # Node ldr_fl_raw
        new_packet.append(int(datum[20])) # Node ldr_br_raw
        new_packet.append(int(datum[21])) # Node ldr_bl_raw
        
        
    print(new_packet)
    
    return new_packet
    
    
    '''
    class DeviceDataRaw(models.Model):
    
    device = models.ForeignKey(Device,verbose_name="dispositivo")
    timestamp = models.DateTimeField(verbose_name="fecha de adquisición",default=timezone.now)
    
    geom = models.GeometryField('punto de adquisición',srid=32629,blank=True, null=True) #coordenadas corregidas UTM29N
    
    millisecons = models.BigIntegerField('tiempo desde inicio de hardware (milissec)', default=-1) #cuando se creo la medida
    
    #to instert facilmente datos gps:
    latitude_raw = models.DecimalField('Latitud GPS (RAW)',default=Decimal('-500.0000'), max_digits=10, decimal_places=6)  #
    longitude_raw = models.DecimalField('Longitud GPS (RAW)',default=Decimal('-500.0000'),max_digits=10, decimal_places=6) #
    
    accX_raw = models.SmallIntegerField('accelerómetro X (RAW)', default=-1) #dato RAW
    accY_raw = models.SmallIntegerField('accelerómetro Y (RAW)', default=-1) #
    accZ_raw = models.SmallIntegerField('accelerómetro Z (RAW)', default=-1) #
    
    gyrX_raw = models.SmallIntegerField('giróscopo X (RAW)', default=-1) #
    gyrY_raw = models.SmallIntegerField('giróscopo Y (RAW)', default=-1) #
    gyrZ_raw = models.SmallIntegerField('giróscopo Z (RAW)', default=-1) #
    
    magX_raw = models.SmallIntegerField('magnetómetro X (RAW)', default=-1) #
    magY_raw = models.SmallIntegerField('magnetómetro Y (RAW)', default=-1) #
    magZ_raw = models.SmallIntegerField('magnetómetro Z (RAW)', default=-1) #
    
    press_air_raw = models.SmallIntegerField('presión aire (RAW)', default=-1) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    
    temp_int_raw = models.SmallIntegerField('temperatura interna (RAW)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    temp_air_raw = models.SmallIntegerField('temperatura aire (RAW)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    temp_water_raw = models.SmallIntegerField('temperatura agua (RAW)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    
    ldr_fr_raw = models.SmallIntegerField('luz incidente FrontRigth (RAW)', default=-1) #
    ldr_fl_raw = models.SmallIntegerField('luz incidente FrontLeft (RAW)', default=-1) #
    ldr_br_raw = models.SmallIntegerField('luz incidente BackRigth (RAW)', default=-1) #
    ldr_bl_raw = models.SmallIntegerField('luz incidente BackLeft (RAW)', default=-1) #
    
    power_volt = models.SmallIntegerField('voltaje solar (RAW)', default=-999) #(0,1024)
    power_amp  = models.SmallIntegerField('amperios solar (RAW)', default=-999) #(0,1024)
    '''
