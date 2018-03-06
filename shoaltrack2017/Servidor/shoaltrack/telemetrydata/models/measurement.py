from django.contrib.gis.db import models
from model_utils import Choices
from django.utils import timezone
from decimal import Decimal

from devices.models import Device
from .dataprocessing import DataProcessing

class DeviceDataRaw(models.Model):
    
    device = models.ForeignKey(Device,verbose_name="dispositivo")
    timestamp = models.DateTimeField(verbose_name="fecha de adquisición",default=timezone.now)
    
    geom = models.GeometryField('punto de adquisición',srid=32629,blank=True, null=True) #coordenadas corregidas UTM29N
    
    millisecons = models.BigIntegerField('tiempo desde inicio de hardware (milissec)', default=-1) #cuando se creo la medida
    
    ########MEASURE DATA RAW############
    #to instert facilmente datos gps:
    latitude_raw = models.FloatField('Latitud GPS UTM29N (RAW)',default=-500.0)  #
    longitude_raw = models.FloatField('Longitud GPS UTM29N (RAW)',default=-500.0) #
    timestamp_gps = models.DateTimeField(verbose_name="fecha del GPS",blank=True, null=True)
    
    accX_raw = models.SmallIntegerField('accelerómetro X (RAW)', default=-1) #dato RAW
    accX_coef = models.ForeignKey(DataProcessing,verbose_name="calibración accelerómetro X",related_name='data_accX_coef',blank=True, null=True)
    accY_raw = models.SmallIntegerField('accelerómetro Y (RAW)', default=-1) #
    accY_coef = models.ForeignKey(DataProcessing,verbose_name="calibración accelerómetro Y",related_name='data_accY_coef',blank=True, null=True)
    accZ_raw = models.SmallIntegerField('accelerómetro Z (RAW)', default=-1) #
    accZ_coef = models.ForeignKey(DataProcessing,verbose_name="calibración accelerómetro Z",related_name='data_accZ_coef',blank=True, null=True)
    
    gyrX_raw = models.SmallIntegerField('giróscopo X (RAW)', default=-1) #
    gyrX_coef = models.ForeignKey(DataProcessing,verbose_name="calibración giróscopo X",related_name='data_gyrX_coef',blank=True, null=True)
    gyrY_raw = models.SmallIntegerField('giróscopo Y (RAW)', default=-1) #
    gyrY_coef = models.ForeignKey(DataProcessing,verbose_name="calibración giróscopo Y",related_name='data_gyrY_coef',blank=True, null=True)
    gyrZ_raw = models.SmallIntegerField('giróscopo Z (RAW)', default=-1) #
    gyrZ_coef = models.ForeignKey(DataProcessing,verbose_name="calibración giróscopo Z",related_name='data_gyrZ_coef',blank=True, null=True)
    
    magX_raw = models.SmallIntegerField('magnetómetro X (RAW)', default=-1) #
    magX_coef = models.ForeignKey(DataProcessing,verbose_name="calibración magnetómetro X",related_name='data_magX_coef',blank=True, null=True)
    magY_raw = models.SmallIntegerField('magnetómetro Y (RAW)', default=-1) #
    magY_coef = models.ForeignKey(DataProcessing,verbose_name="calibración magnetómetro Y",related_name='data_magY_coef',blank=True, null=True)
    magZ_raw = models.SmallIntegerField('magnetómetro Z (RAW)', default=-1) #
    magZ_coef = models.ForeignKey(DataProcessing,verbose_name="calibración magnetómetro Z",related_name='data_magZ_coef',blank=True, null=True)
    
    press_air_raw = models.SmallIntegerField('presión aire (RAW)', default=-1) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    press_air_coef = models.ForeignKey(DataProcessing,verbose_name="calibración presión aire",related_name='data_press_coef',blank=True, null=True)
    
    temp_int_raw = models.SmallIntegerField('temperatura interna (RAW)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    temp_int_coef = models.ForeignKey(DataProcessing,verbose_name="calibración temperatura interna",related_name='data_temp_int_coef',blank=True, null=True)
    temp_air_raw = models.SmallIntegerField('temperatura aire (RAW)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    temp_air_coef = models.ForeignKey(DataProcessing,verbose_name="calibración temperatura aire",related_name='data_temp_air_coef',blank=True, null=True)
    temp_water_raw = models.SmallIntegerField('temperatura agua (RAW)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    temp_water_coef = models.ForeignKey(DataProcessing,verbose_name="calibración temperatura agua",related_name='data_temp_water_coef',blank=True, null=True)
    
    ldr_fr_raw = models.SmallIntegerField('luz incidente FrontRigth (RAW)', default=-1) #
    ldr_fr_coef = models.ForeignKey(DataProcessing,verbose_name="calibración iluminación FrontRigth",related_name='data_ldr_fr_coef',blank=True, null=True)
    ldr_fl_raw = models.SmallIntegerField('luz incidente FrontLeft (RAW)', default=-1) #
    ldr_fl_coef = models.ForeignKey(DataProcessing,verbose_name="calibración iluminación FrontLeft",related_name='data_ldr_fl_coef',blank=True, null=True)
    ldr_br_raw = models.SmallIntegerField('luz incidente BackRigth (RAW)', default=-1) #
    ldr_br_coef = models.ForeignKey(DataProcessing,verbose_name="calibración iluminación BackRigth",related_name='data_ldr_br_coef',blank=True, null=True)
    ldr_bl_raw = models.SmallIntegerField('luz incidente BackLeft (RAW)', default=-1) #
    ldr_bl_coef = models.ForeignKey(DataProcessing,verbose_name="calibración iluminación BackLeft",related_name='data_ldr_bl_coef',blank=True, null=True)
    
    power_volt = models.SmallIntegerField('voltaje solar (RAW)', default=-999) #(0,1024)
    power_volt_coef = models.ForeignKey(DataProcessing,verbose_name="calibración Voltaje",related_name='data_power_volt_coef',blank=True, null=True)
    power_amp  = models.SmallIntegerField('amperios solar (RAW)', default=-999) #(0,1024)
    power_amp_coef = models.ForeignKey(DataProcessing,verbose_name="calibración Amperios",related_name='data_power_amp_coef',blank=True, null=True)
    
    
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
                variables['accX'] = self.accX_coef.raw_to_SI(self.accX_raw)
            else:
                variables['accX'] = self.accX_raw
        elif param =='accY':
            if self.accY_coef:
                variables['accY'] = self.accY_coef.raw_to_SI(self.accY_raw)
            else:
                variables['accY'] = self.accY_raw
        elif param =='accZ':
            if self.accZ_coef:
                variables['accZ'] = self.accZ_coef.raw_to_SI(self.accZ_raw)
            else:
                variables['accZ'] = self.accY_raw
        #####################3
        elif param =='gyrX':
            if self.gyrX_coef:
                variables['gyrX'] = self.gyrX_coef.raw_to_SI(self.gyrX_raw)
            else:
                variables['gyrX'] = self.gyrX_raw
        elif param =='gyrY':
            if self.gyrY_coef:
                variables['gyrY'] = self.gyrY_coef.raw_to_SI(self.gyrY_raw)
            else:
                variables['gyrY'] = self.gyrY_raw
        elif param =='gyrZ':
            if self.gyrZ_coef:
                variables['gyrZ'] = self.gyrZ_coef.raw_to_SI(self.gyrZ_raw)
            else:
                variables['gyrZ'] = self.gyrZ_raw
        ##########################
        elif param =='magX':
            if self.magX_coef:
                variables['magX'] = self.magX_coef.raw_to_SI(self.magX_raw)
            else:
                variables['magX'] = self.magX_raw
        elif param =='magY':
            if self.magY_coef:
                variables['magY'] = self.magY_coef.raw_to_SI(self.magY_raw)
            else:
                variables['magY'] = self.magY_raw
        elif param =='magZ':
            if self.magZ_coef:
                variables['magZ'] = self.magZ_coef.raw_to_SI(self.magZ_raw)
            else:
                variables['magZ'] = self.magZ_raw
        ##########################
        elif param =='press_air':
            if self.press_air_coef:
                variables['press_air'] = self.press_air_coef.raw_to_SI(self.press_air_raw)
            else:
                variables['press_air'] = self.press_air_raw
        #####################3
        elif param =='temp_int':
            if self.temp_int_coef:
                variables['temp_int'] = self.temp_int_coef.raw_to_SI(self.temp_int_raw)
            else:
                variables['temp_int'] = self.temp_int_raw
        elif param =='temp_air':
            if self.temp_air_coef:
                variables['temp_air'] = self.temp_air_coef.raw_to_SI(self.temp_air_raw)
            else:
                variables['temp_air'] = self.temp_air_raw
        elif param =='temp_water':
            if self.temp_water_coef:
                variables['temp_water'] = self.temp_water_coef.raw_to_SI(self.temp_water_raw)
            else:
                variables['temp_water'] = self.temp_water_raw
        
        else:
            return None
