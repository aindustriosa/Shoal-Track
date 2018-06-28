from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


from profiles.models import Contact
from profiles.models import Organization
from profiles.models import Monitor


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('image_tag','name','category','get_username')
    list_display_links = ('image_tag', 'name')
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('image_tag','fisrt_name','last_name','acronym','get_username')
    list_display_links = ('image_tag', 'fisrt_name')
    
    fields = (('user'),
              ('fisrt_name','last_name'),
              ('acronym'),
              ('email'),
              ('image_tag','image')
              )
    
    readonly_fields = ('image_tag',)
                       
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('image_tag','name','acronym','country','email')
    list_display_links = ('image_tag', 'name')

    fields = (('name','acronym'),
              ('country','telephone','email'),
              ('homepage'),
              ('image_tag','image')
              )
    
    readonly_fields = ('image_tag',)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ContactInline(admin.StackedInline):
    model = Contact
    fk_name = 'user'
    verbose_name_plural = 'contactos asociados'
    extra = 0 # how many rows to show
    #readonly_fields = ['resource_ptr']


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ContactInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
