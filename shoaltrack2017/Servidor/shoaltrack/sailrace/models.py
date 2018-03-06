from django.contrib.gis.db import models

from django.utils import timezone

class Device(models.Model):
    name = models.CharField('nombre',unique=True, max_length=80)
    acronym = models.CharField('acrónimo', unique=True, max_length=30)
    
    code = models.SmallIntegerField('código reagata',unique=True)
    
    
    image=models.ImageField('imagen',upload_to='uploads/images/ships/',null=True, blank=True) # file will
    
    
    homepage = models.URLField('página web',blank=True, null=True) # la url de la organizacion
    
    hull_type = models.ForeignKey('HullType',verbose_name="tipo de casco")
    
    team = models.ManyToManyField('Team',verbose_name="equipo")
    
    owner = models.ForeignKey('Organization',verbose_name="colegio")
    
    class Meta:
        managed = True
        db_table = 'device'
        verbose_name = 'dispositivo'
        verbose_name_plural = 'dispositivos'

    def __str__(self):  
        return self.name
    
    
    
class HullType(models.Model):
    name = models.CharField('nombre',unique=True, max_length=80)
    acronym = models.CharField('acrónimo', unique=True, max_length=30)
    
    icon=models.ImageField('imagen',upload_to='uploads/images/icons/',null=True, blank=True) # file will
     
    #boya,monohull, catamarna


class MeasurementNone(models.Model):
    resource = models.ForeignKey(Ship,verbose_name="asociado al dispositivo") #
    
    timestamp = models.DateTimeField(default=timezone.now) #cuando se creo la medida
    
    millisecons = models.BigIntegerField('tiempo desde inicio de hardware (milissec)', default=-1) #cuando se creo la medida
    
    temp_int_raw = models.SmallIntegerField('temperatura interna (decigrados)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    temp_air_raw = models.SmallIntegerField('temperatura aire (decigrados)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    temp_water_raw = models.SmallIntegerField('temperatura agua (decigrados)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    
    press_air_raw = models.SmallIntegerField('presión aire (hectopascal)', default=-1) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    
    accX_raw = models.SmallIntegerField('accelerómetro X (RAW)', default=-1) #
    accY_raw = models.SmallIntegerField('accelerómetro Y (RAW)', default=-1) #
    accZ_raw = models.SmallIntegerField('accelerómetro Z (RAW)', default=-1) #
    
    gyrX_raw = models.SmallIntegerField('giróscopo X (RAW)', default=-1) #
    gyrY_raw = models.SmallIntegerField('giróscopo Y (RAW)', default=-1) #
    gyrZ_raw = models.SmallIntegerField('giróscopo Z (RAW)', default=-1) #
    
    magX_raw = models.SmallIntegerField('magnetómetro X (RAW)', default=-1) #
    magY_raw = models.SmallIntegerField('magnetómetro Y (RAW)', default=-1) #
    magZ_raw = models.SmallIntegerField('magnetómetro Z (RAW)', default=-1) #
    
    power_volt = models.SmallIntegerField('voltaje solar (RAW)', default=-1) #(0,1024)
    power_amp  = models.SmallIntegerField('amperios solar (RAW)', default=-1) #(0,1024)
    
    ldr_fr_raw = models.SmallIntegerField('luz incidente FrontRigth (RAW)', default=-1) #
    ldr_fl_raw = models.SmallIntegerField('luz incidente FrontLeft (RAW)', default=-1) #
    ldr_br_raw = models.SmallIntegerField('luz incidente BackRigth (RAW)', default=-1) #
    ldr_bl_raw = models.SmallIntegerField('luz incidente BackLeft (RAW)', default=-1) #
    
    
    #to instert facilmente datos gps:
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    

class MeasurementBase(models.Model):
    resource = models.ForeignKey(Ship,verbose_name="asociado al dispositivo") #
    
    timestamp = models.DateTimeField(default=timezone.now) #cuando se creo la medida
    
    millisecons = models.BigIntegerField('tiempo desde inicio de hardware (milissec)', default=-1) #cuando se creo la medida
    
    #vaisala
    #temperatura aire, humedad, vel_viento, dir_viento, presion aire, lluvia
    
    
    temp_int_raw = models.SmallIntegerField('temperatura interna (decigrados)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    temp_air_raw = models.SmallIntegerField('temperatura aire (decigrados)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    temp_water_raw = models.SmallIntegerField('temperatura agua (decigrados)', default=-999) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    
    press_air_raw = models.SmallIntegerField('presión aire (hectopascal)', default=-1) #-32768 to 32767 (-327.68ºC to 327.67ºC)
    
    ldr_fr_raw = models.SmallIntegerField('luz incidente FrontRigth (RAW)', default=-1) #
    ldr_fl_raw = models.SmallIntegerField('luz incidente FrontLeft (RAW)', default=-1) #
    ldr_br_raw = models.SmallIntegerField('luz incidente BackRigth (RAW)', default=-1) #
    ldr_bl_raw = models.SmallIntegerField('luz incidente BackLeft (RAW)', default=-1) #
    
    
    #to instert facilmente datos gps:
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    
