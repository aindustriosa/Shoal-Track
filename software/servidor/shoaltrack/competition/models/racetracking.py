from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from model_utils import Choices
from django.utils import timezone

from .race import Race,TrackGeom
from profiles.models import Organization
from devices.models import Device

from random import randint

class Penalty(models.Model):
    TYPE = Choices((0, 'second_start', 'segundos a la salida'),
                   (1, 'second_end', 'segundos al final'),
                   (2, 'position_end', 'posiciones al final'),
                   (3, 'position_start', 'posicones a la salida'),
                   (4, 'drivethrough', 'paso por boxes'),
                   (5, 'stopandgo', 'parada'),
                   (6, 'descalified', 'descalificado')
                  )
    
    name = models.CharField('nombre',unique=True, max_length=50)
    description = models.CharField('descripción',max_length=255, blank=True, null=True)
    unit_type = models.SmallIntegerField('tipo de penalización',choices=TYPE,default=TYPE.second_end)
    
    
    class Meta:
        managed = True
        db_table = 'chp_penalty'
        verbose_name = 'penalización'
        verbose_name_plural = 'penalizaciones'
    
    def get_type(self):
        return self.TYPE[self.unit_type]
    get_type.allow_tags = True
    get_type.short_description = "Tipo"

class RaceCategory(models.Model):
    name  = models.CharField('nombre', max_length=50)
    code  = models.CharField('codigo',unique=True, max_length=10)
    description = models.CharField('descripción',max_length=255, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'chp_category'
        verbose_name = 'categoría del participante'
        verbose_name_plural = 'categorías de participantes'
        
    def __str__(self):  
        return str(self.name)
    
    
class RaceTracking(models.Model):
    COLOR = Choices((0, 'clearblue', 'azul_claro'),
                    (1, 'darkblue', 'azul_oscuro'),
                    (2, 'cleargreen', 'verde_claro'),
                    (3, 'darkgreen', 'verde_oscuro'),
                    (4, 'pink', 'rosa'),
                    (5, 'red', 'rojo'),
                    (6, 'clearorange', 'naranja_claro'),
                    (7, 'darkorange', 'naranja_oscuro'),
                    (8, 'violet', 'violeta'),
                    (9, 'purple', 'morado'),
                    (10,'yellow', 'amarillo'),
                    (11,'white', 'blanco')
                   )
    
    device = models.ForeignKey(Device,verbose_name="participante")
    race   = models.ForeignKey(Race,verbose_name="carrera")
    
    code  = models.CharField('nombre', max_length=50)
    color = models.SmallIntegerField('codigo de color',choices=COLOR,default=COLOR.red)
    category = models.ForeignKey(RaceCategory,verbose_name="categoría",blank=True, null=True)
    
    points  = models.FloatField('puntuacion',null=True)
    
    penalty = models.ManyToManyField(Penalty,blank=True,
                                     through='PenaltyTracking',
                                     verbose_name='listado de penalizaciones')
    
    geo_track = models.ManyToManyField(TrackGeom,blank=True,
                                     through='RaceTrackingNode',
                                     verbose_name='listado de tracking')
    
    timestamp_integrate = models.DateTimeField(verbose_name="fecha de inicio",default=timezone.now)
    
    timestamp_exit = models.DateTimeField(verbose_name="fecha de salida",blank=True, null=True)
    
    observations = models.CharField('observaciones',max_length=255, blank=True, null=True)
    
    
    class Meta:
        managed = True
        db_table = 'chp_racetrack'
        unique_together = ('device', 'race','code')
        verbose_name = 'monitorización de la carrera'
        verbose_name_plural = 'monitorización de las carreras'
        
        
    def __str__(self):  
        return (str(self.race)+'-'+str(self.device)+'-'+self.code)
    
    

    def get_color(self):
        return self.COLOR[self.color]
    get_color.allow_tags = True
    get_color.short_description = "Color"
    
    def get_color_html(self):
        if self.color == self.COLOR.clearblue:
            return '#3d9ae2'
        
        elif self.color == self.COLOR.darkblue:
            return '#1868a3'
        
        elif self.color == self.COLOR.cleargreen:
            return '#b2df8a'
        
        elif self.color == self.COLOR.darkgreen:
            return '#33a02c'
        
        elif self.color == self.COLOR.pink:
            return '#e78ac3'
        
        elif self.color == self.COLOR.red:
            return '#e31a1c'
        
        elif self.color == self.COLOR.clearorange:
            return '#fdbf6f'
        
        elif self.color == self.COLOR.darkorange:
            return '#ff7f00'
        
        elif self.color == self.COLOR.violet:
            return '#cab2d6'
        
        elif self.color == self.COLOR.purple:
            return '#6a3d9a'
        
        elif self.color == self.COLOR.yellow:
            return '#ffff99'
        
        else:
            return '#ffffff'
    
    def get_points(self):
        if self.points:
            return self.points
        else:
            return randint(0, 9)


class RaceTrackingNode(models.Model):
    trackgeom    = models.ForeignKey(TrackGeom,verbose_name="Marcador de referencia")
    racetracking = models.ForeignKey(RaceTracking,verbose_name="Tracking de dispositivo")
    
    timestamp_pass = models.DateTimeField(verbose_name="tiempo de control",default=timezone.now)
    
    class Meta:
        managed = True
        db_table = 'chp_trackingnode'
        verbose_name = 'validacion de marcadores en la carrera'
        verbose_name_plural = 'validaciones de marcadores en las carreras'
    

class PenaltyTracking(models.Model):
    racetracking = models.ForeignKey(RaceTracking,verbose_name="referencia de monitoreo")
    penalty = models.ForeignKey(Penalty,verbose_name="referencia de penalización")
    units = models.SmallIntegerField('unidades de penalización',default=1)
    
    timestamp_pass = models.DateTimeField(verbose_name="tiempo de control",default=timezone.now)
    
    description = models.CharField('descripción',max_length=255, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'chp_trackingpenalty'
        verbose_name = 'monitorización de la penalización en la carrera'
        verbose_name_plural = 'monitorización de las penalizaciones en las carreras'
    
