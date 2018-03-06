from django.db import models
from model_utils import Choices
from django.utils import timezone
import json

from devices.models import Device
from math import log, exp, pow, sqrt


class DataProcessing(models.Model):
    TYPEEQUATION  = Choices((0, 'none', 'ninguna'),
                            (1, 'linear', 'linear'),
                            (2, 'logaritmic', 'logaritmica'),
                            (3, 'exponential', 'exponencial'),
                            (4, 'power', 'potencia'),
                            (5, 'polinomic', 'polinomica'),
                            (6, 'mean', 'media móvil')
                           )
    
    TYPEPARAM  = Choices((0, 'longitude', 'longitud [UTM29N]'),
                         (1, 'latitude', 'latitud [UTM29N]'),
                         (2, 'accelerometer_x', 'acelerómetro en X [m/s2]'),
                         (3, 'accelerometer_y', 'acelerómetro en Y [m/s2]'),
                         (4, 'accelerometer_z', 'acelerómetro en Z [m/s2]'),
                         (5, 'gyroscope_x', 'gyroscopo en X [rad/s]'),
                         (6, 'gyroscope_y', 'gyroscopo en Y [rad/s]'),
                         (7, 'gyroscope_z', 'gyroscopo en Z [rad/s]'),
                         (8, 'magnetometer_x', 'magnetometro en X [uT]'),
                         (9, 'magnetometer_y', 'magnetometro en Y [uT]'),
                         (10, 'magnetometer_z', 'magnetometro en Z [uT]'),
                         (11, 'pressure', 'presion [Pa]'),
                         (12, 'temperature_int', 'temperatura interior [ºC]'),
                         (13, 'temperature_air', 'temperatura aire [ºC]'),
                         (14, 'temperature_water', 'temperatura agua [ºC]'),
                         (15, 'ilumination_fr', 'iluminación FrontRigth [Lux]'),
                         (16, 'ilumination_fl', 'iluminación FrontLeft [Lux]'),
                         (17, 'ilumination_br', 'iluminación BackRigth [Lux]'),
                         (18, 'ilumination_bl', 'iluminación BackLeft [Lux]'),
                         (19, 'voltage', 'voltaje [V]'),
                         (20,'amperes', 'amperios [A]'),
                         (21,'wind_mod', 'intensidad viento [m/s]'),
                         (22,'wind_dir', 'dirección viento [ºDeg]'),
                         (23,'humidity_relative', 'humedad relativa [%]')
                        )
    
    device = models.ForeignKey(Device,verbose_name="dispositivo")
    timestamp = models.DateTimeField(verbose_name="fecha de adquisición",default=timezone.now)
    
    type_equation = models.SmallIntegerField('tipo de ecuacion',choices=TYPEEQUATION,default=TYPEEQUATION.none)
    type_param = models.SmallIntegerField('tipo de parámetro',choices=TYPEPARAM,default=TYPEPARAM.longitude)
    
    args = models.CharField('constantes de la ecuación',max_length=200,blank=True, null=True) #guardo los argumentos en una estructrua json
    
    
    class Meta:
        managed = True
        db_table = 'msr_dataprocess'
        verbose_name = 'coeficientes de proceso del dato'
        verbose_name_plural = 'coeficientes de proceso de los datos'
        
    def __str__(self):  
        return (str(self.device))
    
    def get_type_equation(self):
        return self.TYPEEQUATION[self.type_equation]
    get_type_equation.allow_tags = True
    get_type_equation.short_description = "Tipo de ecuación"
    
    def get_type_param(self):
        return self.TYPEPARAM[self.type_param]
    get_type_param.allow_tags = True
    get_type_param.short_description = "Tipo de parámetro"
    
    def set_args(self, x):
        if x==None:
            x=[1,0]
        
        self.args = json.dumps(x)

    def get_args(self):
        return json.loads(self.args)
    
    def raw_to_SI(self, valueraw):
        coefs = self.get_args()
        
        if self.type_equation == self.TYPEEQUATION.linear:
            #ax+b
            return ((coefs[0]*valueraw) + coefs[1])
        
        elif self.type_equation == self.TYPEEQUATION.logaritmic:
            #log(x,base)+a
            return (log(valueraw,coefs[1]) + coefs[0])
        
        elif self.type_equation == self.TYPEEQUATION.exponential:
            #e(x)+a
            return valueraw
            #return (exp(valueraw) + coefs[0])
            
        else:
            return valueraw
