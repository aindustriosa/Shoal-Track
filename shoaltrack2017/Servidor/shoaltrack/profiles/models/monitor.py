from django.db import models
from model_utils import Choices
from django.contrib.auth.models import User

class Monitor(models.Model):
    TYPE = Choices((0, 'emergency', 'emergencias'),
                   (1, 'notification', 'notificaciones'),
                   (2, 'acquiredata', 'adquisicion de datos'),
                   (3, 'searchref', 'buscador referencias')
                  )
    name = models.CharField('nombre', max_length=60)
    
    category = models.SmallIntegerField('categoría de monitoreo',choices=TYPE,default=TYPE.acquiredata)
    
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="acceso de usuario",
                             blank=True, null=True) # 
    
    image=models.ImageField('imagen',upload_to='media/uploads/images/profiles/',default = 'media/uploads/test_images/noimage.png',null=True, blank=True)
    
    class Meta:
        managed = True
        db_table = 'prf_monitor'
        verbose_name = 'monitor'
        verbose_name_plural = 'monitores'
    
    
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
    
    def get_username(self):
        if user:
            return self.user.username
        else:
            return None
    get_username.short_description = 'nombre usuario'
    get_username.allow_tags = True
    
