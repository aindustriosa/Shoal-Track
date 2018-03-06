from django.db import models
from model_utils import Choices
from django.utils import timezone

from profiles.models import Organization, Contact


class Device(models.Model):
    TYPE = Choices(
                   (0, 'monohull', 'monocasco'),
                   (1, 'catamaran', 'bicasco'),
                   (2, 'swath', 'casco sumergido'),
                   (3, 'planing', 'planeador'),
                   (4, 'hydrofoil', 'hidrofoil'),
                   (5, 'air_lift', 'hovercraft'),
                   (6, 'trimaran', 'tricasco'),
                   (7, 'underwater', 'submarino'),
                   (100, 'virtualpoint', 'punto virtual'),
                   (101, 'racebuoy', 'boya señalizacion'),
                   (102, 'fixedgateway', 'puesto de control'),
                   (103, 'fixedbuoy', 'boya de señalización fija'),
                  )
    
    name = models.CharField('nombre', max_length=50)
    category = models.SmallIntegerField('categoría del casco',choices=TYPE,default=TYPE.monohull)
    acronym = models.CharField('acrónimo',unique=True, max_length=20) 
    
    description = models.CharField('descripción',max_length=255, blank=True, null=True)
    
    image=models.ImageField('imagen',upload_to='media/uploads/images/devices/',default = 'media/uploads/test_images/noimage.png',null=True, blank=True)
    
    #propiedades
    weight = models.FloatField('masa [Kg]', blank=True, null=True) #en Kg
    length = models.FloatField('eslora [m]', blank=True, null=True) #eslora (largo)
    sleeve = models.FloatField('manga [m]', blank=True, null=True) #manga ancho
    draft  = models.FloatField('calado [m]', blank=True, null=True) #calado
    model3d= models.FileField('modelo 3d',upload_to='uploads/models/devices/',null=True, blank=True)
    
    
    #actividad
    timestamp_created = models.DateTimeField(verbose_name="fecha creación",default=timezone.now)
    is_enable=models.BooleanField('¿esta operativo?',default=True)
    
    #gestion de sus usuarios:
    owner = models.ForeignKey(Organization,verbose_name="fabricante")
    team = models.ManyToManyField(Contact,blank=True,
                                  through='TeamTrace',
                                  verbose_name='configuración de equipo')
    
    
    class Meta:
        managed = True
        db_table = 'dev_node'
        verbose_name = 'dispositivo'
        verbose_name_plural = 'dispositivos'
        
    def __str__(self):  
        return (self.name +' ['+self.acronym+']')
    
    def image_tag(self):
        try:
            return '<img src="%s" />' % self.image.url
        except:
            return None
    image_tag.short_description = 'image'
    image_tag.allow_tags = True
    
    def get_type(self):
        return self.TYPE[self.category]
    get_type.allow_tags = True
    get_type.short_description = "Tipo"
    
 
class TeamTrace(models.Model):
    TYPE = Choices((0, 'owner', 'dueño'),
                   (1, 'financial', 'financiero'),
                   (2, 'electric', 'eléctrico'),
                   (3, 'mechanical', 'mecánico'),
                   (4, 'coordination', 'coordinador'),
                   (5, 'program', 'programador'),
                   (6, 'desing', 'diseñador'),
                   (7, 'consultant', 'asesor'),
                   (8, 'technical', 'técnico')
                  )
    device = models.ForeignKey(Device,verbose_name="dispositivo")
    contact = models.ForeignKey(Contact,verbose_name="perfil contacto")
    
    timestamp_enable = models.DateTimeField(verbose_name="agregado desde",default=timezone.now)
    rol = models.SmallIntegerField('rol funcional',choices=TYPE,default=TYPE.technical)
    timestamp_disable = models.DateTimeField(verbose_name="retirado desde",blank=True, null=True)
    
    
    
    
    class Meta:
        managed = True
        db_table = 'team_trace'
        verbose_name = 'trazabilidad del equipo'
        verbose_name_plural = 'trazabilidad de equipos'
        
    def get_rol(self):
        return self.TYPE[self.rol]
    get_rol.allow_tags = True
    get_rol.short_description = "Tipo"
