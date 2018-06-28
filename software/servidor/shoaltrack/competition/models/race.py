from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from model_utils import Choices
from django.utils import timezone
from django.template.defaultfilters import slugify

from profiles.models import Organization
from devices.models import Device


class Race(models.Model):
    STATUS = Choices((0,'abort', 'abortada'),
                                  (1, 'propostal', 'propuesta'),
                                  (2, 'desing', 'diseño'),
                                  (3, 'open', 'abierta'),
                                  (4, 'briefing', 'instrucciones'),
                                  (5, 'waiting', 'esperando'),
                                  (6, 'launch', 'lanzamiento'),
                                  (7, 'start', 'comenzando'),
                                  (8, 'middle', 'en curso'),
                                  (9, 'ending', 'terminando'),
                                  (10,'finished', 'finalizada'),
                                  (11,'deliberation','deliberacion'),
                                  (12,'awards', 'premios'),
                                  (13,'closed', 'cerrada')
                                 )
    
    name = models.CharField('nombre', max_length=50)
    edicion = models.SmallIntegerField('numero de edición',default=1)
    slug = models.SlugField(unique=True)
    
    description = models.CharField('descripción',max_length=255, blank=True, null=True)
    
    timestamp_start = models.DateTimeField(verbose_name="fecha de inicio",default=timezone.now)
    timestamp_finish = models.DateTimeField(verbose_name="fecha de finalización",blank=True, null=True)
    
    status = models.SmallIntegerField('estado de la carrera',choices=STATUS,default=STATUS.propostal)
    
    track = models.ManyToManyField(Device,blank=True,
                                   through='TrackGeom',
                                   verbose_name='configuración del trazado')
    
    limit_area = models.GeometryField('limites de la zona de carrera',srid=32629,blank=True, null=True) #coordenadas UTM29N
    
    organization = models.ForeignKey(Organization,verbose_name="organizador")
    image=models.ImageField('imagen',upload_to='uploads/images/competition/',default = 'test_images/noimage.jpg',null=True, blank=True) # file will be saved to MEDIA_ROOT/uploads/2015/01/30
    
    class Meta:
        managed = True
        db_table = 'chp_race'
        verbose_name = 'carrera'
        verbose_name_plural = 'carreras'
        
        
    def __str__(self):  
        return (str(self.edicion)+'ª '+self.name)
    
    def save(self, *args, **kwargs):
        if not self.pk: #si no existe, 
            text_slug = '{}-{}'.format(self.edicion, self.name)
            self.slug = slugify(text_slug)
        
        super(Race, self).save(*args,**kwargs)
    
    def image_tag(self):
        try:
            return '<img src="%s" />' % self.image.url
        except:
            return None
    image_tag.short_description = 'image'
    image_tag.allow_tags = True

    def get_status(self):
        return self.STATUS[self.status]
    get_status.allow_tags = True
    get_status.short_description = "Estado"


    def get_geom(self):
        '''busca las medidas asociadas y calcula el boundin box de todas-> geometria
        '''
        pass
    get_geom.allow_tags = True
    get_geom.short_description = "Geometría"
    
    def get_geom_WKT(self):
        geom = self.get_geom()
        return geom.wkt
    get_geom_WKT.allow_tags = True
    get_geom_WKT.short_description = "Código WKT"
    
    def get_geom_KML(self):
        geom = self.get_geom()
        return geom.kml
    get_geom_KML.allow_tags = True
    get_geom_KML.short_description = "Código KML"
    
    def get_geom_JSN(self):
        geom = get_geom()
        return geom.json
    get_geom_JSN.allow_tags = True
    get_geom_JSN.short_description = "Código GeoJSON"
    
    def get_limits_JSN(self):
        return self.limit_area.json
    get_limits_JSN.allow_tags = True
    get_limits_JSN.short_description = "Límites GeoJSON"
    
    def get_limits_JSN_WGS84(self):
        self.limit_area.transform(4326)
        return self.limit_area.json
    get_limits_JSN_WGS84.allow_tags = True
    get_limits_JSN_WGS84.short_description = "Límites GeoJSON en WGS84"
    
    def get_geom_marks(self,):
        '''obtengo una lista de las geometrias que han de pasar los devices
        '''
        linear_marks=[]
        marks_tracks = TrackGeom.objects.filter(race=self).order_by('order').select_related("device")
        
        linear_start = []
        linear_end = []
        linear_inrace=[]
        for track in marks_tracks:
            if track.track_pass in [0,1]: #es de typo inicio
                linear_start.append([track.longitude(),track.latitude()])
                
            elif track.track_pass in [2,3]: #es de typo fin
                linear_end.append([track.longitude(),track.latitude()])
                
            else:
                temp = track.get_cross_line()
                if temp:
                    linear_inrace.append(temp)
                
        linear_marks.append(linear_start)
        for item in linear_inrace:
            linear_marks.append(item)
        linear_marks.append(linear_end)
         
        return linear_marks
        

class TrackGeom(models.Model):
    '''realcion de los dispositivos encargados de delimitar el trazado de una carrera
    '''
    MODE = Choices((0, 'startR', 'comienzo por derechas'),
                   (1, 'startL', 'comienzo por izquierdas'),
                   (2, 'endR', 'fin por derechas'),
                   (3, 'endL', 'fin por izquierdas'),
                   (4, 'near', 'cerca'),
                   (5, 'under', 'por debajo'),
                   (6, 'loiterR', 'giro a derechas'),
                   (7, 'loiterL', 'giro a izquierdas'),
                   (8, 'touch', 'tocar'),
                   (11, 'crossN', 'atravesar Norte'),
                   (12, 'crossNE', 'atravesar NoroEste'),
                   (13, 'crossE', 'atravesar Este'),
                   (14, 'crossSE', 'atravesar SurEste'),
                   (15, 'crossS', 'atravesar Sur'),
                   (16, 'crossSO', 'atravesar SurOeste'),
                   (17, 'crossO', 'atravesar Oeste'),
                   (18, 'crossNO', 'atravesar NorteOeste'),
                   (200, 'info', 'informacion')
                  )
    
    race = models.ForeignKey(Race,verbose_name="competicion")
    device = models.ForeignKey(Device,verbose_name="dispositivo asociado")
    
    timestamp_enable = models.DateTimeField(verbose_name="agregado desde",default=timezone.now)
    
    track_pass = models.SmallIntegerField('modo de paso',choices=MODE,default=MODE.touch)
    timestamp_disable = models.DateTimeField(verbose_name="retirado desde",blank=True, null=True)
    
    order = models.SmallIntegerField('número de orden',default=1)
    geom = models.GeometryField('geometria 2D inicial',srid=32629,blank=True, null=True) #coordenadas UTM29N
    
    
    class Meta:
        managed = True
        db_table = 'chp_trackgeom'
        verbose_name = 'marcador del trazado de la carrera'
        verbose_name_plural = 'marcadores del trazado de la carrera'
        
    def __str__(self):  
        return (str(self.race)+'-'+str(self.device))
    
    def get_type(self):
        return self.device.get_type()
    get_type.allow_tags = True
    get_type.short_description = "Tipo"
    
    def get_pass(self):
        return self.MODE[self.track_pass]
    get_pass.allow_tags = True
    get_pass.short_description = "Validación"
    
    def latitude(self):
        if self.geom.geom_type == 'Point':
            return self.geom.y
        else:
            return None
    latitude.allow_tags = True
    latitude.short_description = "latitud"

    def longitude(self):
        if self.geom.geom_type == 'Point':
            return self.geom.x
        else:
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
    
    def get_cross_line(self,):
        if self.track_pass == self.MODE.crossN:
            line=[[self.longitude(),self.latitude()]] #point start
            line.append([self.longitude(),self.latitude()+100]) #point end subo 100 metros
        
        elif self.track_pass == self.MODE.crossNE:
            line=[[self.longitude(),self.latitude()]] #point start
            line.append([self.longitude()+100,self.latitude()+100]) #point end subo 100 metros
            
        elif self.track_pass == self.MODE.crossE:
            line=[[self.longitude(),self.latitude()]] #point start
            line.append([self.longitude()+100,self.latitude()]) #point end 100 metros derecha
            
        elif self.track_pass == self.MODE.crossSE:
            line=[[self.longitude(),self.latitude()]] #point start
            line.append([self.longitude()+100,self.latitude()-100]) #point end subo 100 metros
        elif self.track_pass == self.MODE.crossS:
            line=[[self.longitude(),self.latitude()]] #point start
            line.append([self.longitude(),self.latitude()-100]) #point end subo 100 metros
            
        elif self.track_pass == self.MODE.crossSO:
            line=[[self.longitude(),self.latitude()]] #point start
            line.append([self.longitude()-100,self.latitude()-100]) #point end subo 100 metros
            
        elif self.track_pass == self.MODE.crossO:
            line=[[self.longitude(),self.latitude()]] #point start
            line.append([self.longitude()-100,self.latitude()]) #point end subo 100 metros
            
        elif self.track_pass == self.MODE.crossNO:
            line=[[self.longitude(),self.latitude()]] #point start
            line.append([self.longitude()-100,self.latitude()+100]) #point end subo 100 metros
            
        else:
            return None
            
