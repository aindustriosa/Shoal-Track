from django.contrib.gis.db import models
from model_utils import Choices
from django.utils import timezone
from decimal import Decimal

from devices.models import Device
from .dataprocessing import DataProcessing

class DeviceDataRaw(models.Model):
    
    device = models.ForeignKey(Device,verbose_name="dispositivo")
    timestamp = models.DateTimeField(verbose_name="fecha de envio",default=timezone.now)
    timestamp_rcv = models.DateTimeField(verbose_name="fecha recibido",default=timezone.now)
    
    nextHop = models.SmallIntegerField('siguiente Salto', default=-1)
    rssi = models.SmallIntegerField('intensidad señal', default=0)
    
    #########GPS#########
    geom = models.GeometryField('punto de adquisición',srid=32629,blank=True, null=True) #coordenadas corregidas UTM29N
    
    gps_precision = models.SmallIntegerField('Precision del GPS', default=-1)
    gps_itow = models.BigIntegerField('tiempo desde inicio de GPS (milissec)', default=-1) #cuando se creo la medida
    gps_latitude = models.FloatField('Latitud GPS UTM29N (RAW)',default=-500.0)  #
    gps_longitude = models.FloatField('Longitud GPS UTM29N (RAW)',default=-500.0) #
    gps_heading = models.SmallIntegerField('orientacion del GPS', default=-1)
    
    ########MEASURE DATA RAW############
    #to instert facilmente datos gps:
    bearing_avg = models.SmallIntegerField('orientacion del magnetómetro (media) (RAW)', default=-1)
    bearing_std = models.SmallIntegerField('orientacion del magnetómetro (dsv_std) (RAW)', default=-1)
    bearing_coef = models.ForeignKey(DataProcessing,verbose_name="calibración de orientacion",related_name='data_bearing_coef',blank=True, null=True)
    
    voltage_batt_avg=models.SmallIntegerField('volt bateria (media) (RAW)', default=-1) #dato RAW
    voltage_batt_std=models.SmallIntegerField('volt bateria (dsv_std) (RAW)', default=-1) #dato RAW
    voltage_batt_coef = models.ForeignKey(DataProcessing,verbose_name="calibración voltaje bateria",related_name='data_voltage_batt_coef',blank=True, null=True)
    
    amp_batt_avg=models.SmallIntegerField('amp bateria (media) (RAW)', default=-32768) #dato RAW
    amp_batt_std=models.SmallIntegerField('amp bateria (dsv_std) (RAW)', default=-32768) #dato RAW
    amp_batt_coef = models.ForeignKey(DataProcessing,verbose_name="calibración amperios bateria",related_name='data_amp_batt_coef',blank=True, null=True)
    
    pressure_avg=models.SmallIntegerField('presion (media) (RAW)', default=-1) #dato RAW
    pressure_std=models.SmallIntegerField('presion (dsv_std) (RAW)', default=-1) #dato RAW
    pressure_coef = models.ForeignKey(DataProcessing,verbose_name="calibración presión aire",related_name='data_pressure_coef',blank=True, null=True)
    
    ligth_avg=models.SmallIntegerField('luz (media) (RAW)', default=-1) #dato RAW
    ligth_std=models.SmallIntegerField('luz (dsv_std) (RAW)', default=-1) #dato RAW
    ligth_coef = models.ForeignKey(DataProcessing,verbose_name="calibración luz",related_name='data_ligth_coef',blank=True, null=True)
    
    #accelerometro
    accX_avg=models.SmallIntegerField('accelerómetro (media) X (RAW)', default=-32768) #dato RAW
    accX_std=models.SmallIntegerField('accelerómetro (dsv_std) X (RAW)', default=-1) #dato RAW
    accX_coef = models.ForeignKey(DataProcessing,verbose_name="calibración accelerómetro X",related_name='data_accX_coef',blank=True, null=True)
    
    accY_avg=models.SmallIntegerField('accelerómetro (media) Y (RAW)', default=-32768) #dato RAW
    accY_std=models.SmallIntegerField('accelerómetro (dsv_std) Y (RAW)', default=-1) #dato RAW
    accY_coef = models.ForeignKey(DataProcessing,verbose_name="calibración accelerómetro Y",related_name='data_accY_coef',blank=True, null=True)
    
    accZ_avg=models.SmallIntegerField('accelerómetro (media) Z (RAW)', default=-32768) #dato RAW
    accZ_std=models.SmallIntegerField('accelerómetro (dsv_std) Z (RAW)', default=-1) #dato RAW
    accZ_coef = models.ForeignKey(DataProcessing,verbose_name="calibración accelerómetro Z",related_name='data_accZ_coef',blank=True, null=True)
    
    #giroscopo
    gyrX_avg=models.SmallIntegerField('giroscopo (media) X (RAW)', default=-32768) #dato RAW
    gyrX_std=models.SmallIntegerField('giroscopo (dsv_std) X (RAW)', default=-1) #dato RAW
    gyrX_coef = models.ForeignKey(DataProcessing,verbose_name="calibración giróscopo X",related_name='data_gyrX_coef',blank=True, null=True)
    
    gyrY_avg=models.SmallIntegerField('giroscopo (media) Y (RAW)', default=-32768) #dato RAW
    gyrY_std=models.SmallIntegerField('giroscopo (dsv_std) Y (RAW)', default=-1) #dato RAW
    gyrY_coef = models.ForeignKey(DataProcessing,verbose_name="calibración giróscopo Y",related_name='data_gyrY_coef',blank=True, null=True)
    
    gyrZ_avg=models.SmallIntegerField('giroscopo (media) Z (RAW)', default=-32768) #dato RAW
    gyrZ_std=models.SmallIntegerField('giroscopo (dsv_std) Z (RAW)', default=-1) #dato RAW
    gyrZ_coef = models.ForeignKey(DataProcessing,verbose_name="calibración giróscopo Z",related_name='data_gyrZ_coef',blank=True, null=True)
    

    #from master only:
    ref_air_temp = models.FloatField('temperatura de referencia [ºC]', blank=True, null=True) #
    ref_pressure = models.FloatField('presion de referencia [hPa]', blank=True, null=True) #
    ref_humidity_relative = models.FloatField('humedad relativa [%]', blank=True, null=True) #
    ref_wind_module = models.FloatField('intensidad del viento [m/s]', blank=True, null=True) #
    ref_wind_direction = models.FloatField('direccion del viento [ºDeg]', blank=True, null=True) #
    
    
    
    #data = models.ForeignKey(Device,verbose_name="dispositivo")
    
    
    
    
    ########PRE-CALCULATE DATA RACE############
    ranking = models.SmallIntegerField('Posición en la carrera]', blank=True, null=True) #
     
    velocity = models.FloatField('Velocidad [m/s]', blank=True, null=True) #
    direction = models.SmallIntegerField('Dirección [ºDeg]', blank=True, null=True) #
    
    
    
    class Meta:
        managed = True
        db_table = 'msr_devdataraw'
        verbose_name = 'medida de dispositivo'
        verbose_name_plural = 'medidas de dispositivos'
        
    def __str__(self):  
        return (str(self.device))
    
    def latitude(self,WGS84=False):
        if WGS84:
            self.geom.transform(4326)
        if self.geom:
            if self.geom.geom_type == 'Point':
                return self.geom.y
        return None
    latitude.allow_tags = True
    latitude.short_description = "latitud"

    def longitude(self,WGS84=False):
        if WGS84:
            self.geom.transform(4326)
        if self.geom:
            if self.geom.geom_type == 'Point':
                return self.geom.x
        return None
    longitude.allow_tags = True
    longitude.short_description = "longitud"
    
    def geom_type(self,):
        if not self.geom.empty:
            return self.geom.geom_type
        else:
            return None
    geom_type.allow_tags = True
    geom_type.short_description = "Tipo geometría"
        
    def geom_WKT(self):
        return self.geom.wkt
    geom_WKT.allow_tags = True
    geom_WKT.short_description = "Código WKT"
    
    def geom_KML(self):
        return self.geom.kml
    geom_KML.allow_tags = True
    geom_KML.short_description = "Código KML"
    
    def geom_JSN(self):
        return self.geom.json
    geom_JSN.allow_tags = True
    geom_JSN.short_description = "Código GeoJSON"
    
    def geom_JSN_WGS84(self):
        self.geom.transform(4326)
        return self.geom.json
    geom_JSN_WGS84.allow_tags = True
    geom_JSN_WGS84.short_description = "Código GeoJSON en WGS84"
    
    def set_geom(self,geom_wkt_hrx_wkb_geojson):
        self.geom = GEOSGeometry(geom_wkt_hrx_wkb_geojson)
        self.save()

    def get_unit_SI(param=None):
        variables = {}
        
        if param =='accX':
            if self.accX_coef:
                variables['accX'] = self.accX_coef.raw_to_SI(self.accX_avg)
            else:
                variables['accX'] = self.accX_avg
        elif param =='accY':
            if self.accY_coef:
                variables['accY'] = self.accY_coef.raw_to_SI(self.accY_avg)
            else:
                variables['accY'] = self.accY_avg
        elif param =='accZ':
            if self.accZ_coef:
                variables['accZ'] = self.accZ_coef.raw_to_SI(self.accZ_avg)
            else:
                variables['accZ'] = self.accZ_avg
        #####################3
        elif param =='gyrX':
            if self.gyrX_coef:
                variables['gyrX'] = self.gyrX_coef.raw_to_SI(self.gyrX_avg)
            else:
                variables['gyrX'] = self.gyrX_avg
        elif param =='gyrY':
            if self.gyrY_coef:
                variables['gyrY'] = self.gyrY_coef.raw_to_SI(self.gyrY_avg)
            else:
                variables['gyrY'] = self.gyrY_avg
        elif param =='gyrZ':
            if self.gyrZ_coef:
                variables['gyrZ'] = self.gyrZ_coef.raw_to_SI(self.gyrZ_avg)
            else:
                variables['gyrZ'] = self.gyrZ_avg
        ##########################
        elif param =='bearing':
            if self.bearing_coef:
                variables['bearing'] = self.bearing_coef.raw_to_SI(self.bearing_avg)
            else:
                variables['bearing'] = self.bearing_avg
        ###########################
        elif param =='voltage_batt':
            if self.voltage_batt_coef:
                variables['voltage_batt'] = self.voltage_batt_coef.raw_to_SI(self.voltage_batt_avg)
            else:
                variables['voltage_batt'] = self.voltage_batt_avg
        elif param =='amp_batt':
            if self.amp_batt_coef:
                variables['amp_batt'] = self.amp_batt_coef.raw_to_SI(self.amp_batt)
            else:
                variables['amp_batt'] = self.amp_batt_avg
        elif param =='pressure':
            if self.pressure_coef:
                variables['pressure'] = self.pressure_coef.raw_to_SI(self.pressure_avg)
            else:
                variables['pressure'] = self.pressure_avg
        elif param =='ligth':
            if self.ligth_coef:
                variables['ligth'] = self.ligth_coef.raw_to_SI(self.ligth_avg)
            else:
                variables['ligth'] = self.ligth_avg
        
        else:
            return None
