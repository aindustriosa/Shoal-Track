from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from model_utils import Choices
from django.utils import timezone
from django.template.defaultfilters import slugify

from profiles.models import Organization
from .race import Race


class Champion(models.Model):
    STATUS = Choices((0, 'propostal', 'propuesta'),
                                  (1, 'desing', 'diseño'),
                                  (2, 'open', 'abierta'),
                                  (3, 'briefing', 'instrucciones'),
                                  (4, 'waiting', 'esperando'),
                                  (5, 'launch', 'lanzamiento'),
                                  (6, 'start', 'comenzando'),
                                  (7, 'middle', 'en curso'),
                                  (8, 'ending', 'terminando'),
                                  (9, 'finished', 'finalizada'),
                                  (10,'deliberation','deliberacion'),
                                  (11,'awards', 'premios'),
                                  (12,'closed', 'cerrada')
                                 )
    
    name = models.CharField('nombre', max_length=50)
    slug = models.SlugField(unique=True)
    
    edicion = models.SmallIntegerField('numero de edición',default=1)
    description = models.CharField('descripción',max_length=255, blank=True, null=True)
    
    timestamp_start = models.DateTimeField(verbose_name="fecha de inicio",default=timezone.now)
    timestamp_finish = models.DateTimeField(verbose_name="fecha de finalización",blank=True, null=True)
    
    status = models.SmallIntegerField('estado del campeonato',choices=STATUS,default=STATUS.propostal)
    
    races = models.ManyToManyField(Race,blank=True,
                                   through='ListTraceRaces',
                                   verbose_name='lista de carreras')
    
    organization = models.ForeignKey(Organization,verbose_name="organizador")
    image=models.ImageField('imagen',upload_to='media/uploads/images/competition/',default = 'media/uploads/test_images/noimage.png',null=True, blank=True) # file will be saved to MEDIA_ROOT/uploads/2015/01/30
    
    class Meta:
        managed = True
        db_table = 'chp_champion'
        unique_together = ('name', 'edicion')
        verbose_name = 'campeonato'
        verbose_name_plural = 'campeonatos'
        
        
    def __str__(self):  
        return '{}ª {}'.format(self.edicion, self.name)
    
    def save(self, *args, **kwargs):
        if not self.pk: #si no existe, 
            text_slug = '{}-{}'.format(self.edicion, self.name)
            self.slug = slugify(text_slug)
        
        super(Champion, self).save(*args,**kwargs)
    
    
    def image_tag(self):
        try:
            return '<img src="{}" />'.format(self.image.url)
        except:
            return None
    image_tag.short_description = 'image'
    image_tag.allow_tags = True

    def get_status(self):
        return self.STATUS[self.status]
    get_status.allow_tags = True
    get_status.short_description = "Estado"
    






class ListTraceRaces(models.Model):
    champion = models.ForeignKey(Champion,verbose_name="competición")
    race = models.ForeignKey(Race,verbose_name="carrera asociada")
    
    is_enable=models.BooleanField('¿esta operativa?',default=True)
    
    order = models.SmallIntegerField('orden de posición',default=1)
    
    
    class Meta:
        managed = True
        db_table = 'chp_listrace'
        verbose_name = 'listado de carreras en campeonato'
        verbose_name_plural = 'listados de carreras en campeonatos'
    
    def __str__(self):  
        return (str(self.champion)+': '+str(self.order)+'ª prueba')
