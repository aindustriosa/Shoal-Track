from django.db import models

class Organization(models.Model):
    #por la ProfilesBase: 
    #acronym
    #description
    #image
    
    name = models.CharField('nombre', max_length=60)
    acronym = models.CharField('acrónimo',unique=True, max_length=20) 
    
    country = models.CharField('país', max_length=30, blank=True, null=True)
    telephone = models.CharField('teléfono',max_length=30, blank=True, null=True)
    email = models.EmailField('correo-e', blank=True, null=True)
    
    homepage = models.URLField('página web',blank=True, null=True) # la url de la organizacion
    
    image=models.ImageField('imagen',upload_to='media/uploads/images/profiles/',default = 'media/uploads/test_images/noimage.png',null=True, blank=True) # file will be saved to MEDIA_ROOT/uploads/2015/01/30
    
    class Meta:
        managed = True
        db_table = 'prf_organization'
        verbose_name = 'organización'
        verbose_name_plural = 'organizaciones'
    
    def __str__(self):
        return self.name  
    
    def image_tag(self,resolution=None):
        try:
            img_html = '<img src="%s" />' % self.image.url
        except:
            img_html = None
        
        if resolution =='low':
            img_html = img_html.replace('.png','-low.png')
       
        return img_html
    image_tag.short_description = 'image'
    image_tag.allow_tags = True
    
