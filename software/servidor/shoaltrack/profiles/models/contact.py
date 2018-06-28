from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    """
    Clase Usuarios donde se gestionan los usuarios y permisos del sistema
    se enlaza con la de user propia de django por medio de la referencia de nombre de usuario...
    se enlaza como user.contact (tambien acesible directamente por herencia)
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="acceso de usuario",
                             blank=True, null=True) # 
    
    # username
    # fisrt_name
    # last_name
    # email
    # password
    # is_staff (admin site)
    # is active # para ver si es posible usarlo como lognin en PLACTOM
    # is superuser
    # lastlogin
    # date join
    # permisos: grupo
    #           usuario
    
    fisrt_name = models.CharField('nombre', max_length=50)
    last_name = models.CharField('apellidos', max_length=60)
    
    acronym = models.CharField('apodo',unique=True, max_length=20) 
    email=models.EmailField('correo-e',blank=True, null=True)
    
    image=models.ImageField('imagen',upload_to='media/uploads/images/profiles/',default = 'media/uploads/test_images/noimage.png',null=True, blank=True) # file will be saved to MEDIA_ROOT/uploads/2015/01/30
    
    
    
    class Meta:
        managed = True
        db_table = 'prf_contact'
        verbose_name = 'contacto'
        verbose_name_plural = 'contactos'
        
    def __str__(self):
        return self.fisrt_name +' '+self.last_name  
        
    
    def image_tag(self):
        try:
            return '<img src="%s" />' % self.image.url
        except:
            return None
    image_tag.short_description = 'image'
    image_tag.allow_tags = True
        
    def get_idName(self):
        return self.fisrt_name[0] +'.  '+self.last_name      

    def get_username(self):
        if self.user:
            return self.user.username
        else:
            return '--'
    get_username.short_description = 'nombre usuario'
    get_username.allow_tags = True
    
    def get_email(self):
        if user:
            return [self.user.email,self.email]
        else:
            return [self.email]
    
 
