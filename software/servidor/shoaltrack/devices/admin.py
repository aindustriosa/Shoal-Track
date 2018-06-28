from django.contrib import admin


from devices.models import Device, TeamTrace



class TeamTraceInline(admin.TabularInline):
    model = TeamTrace
    fk_name = 'device'
    extra = 0 # how many rows to show


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('image_tag','name','get_type','owner','is_enable')
    list_display_links = ('image_tag', 'name')
    
    fields = (('name','category','acronym'),
              ('owner'),
              ('description'),
              ('image_tag','image'),
              ('weight','length','sleeve','draft'),
              ('model3d'),
              ('timestamp_created','is_enable'),
              )
    
    readonly_fields = ('image_tag',)
    
    inlines = [TeamTraceInline,]


@admin.register(TeamTrace)
class TeamTraceAdmin(admin.ModelAdmin):
    list_display = ('device','contact','get_rol','timestamp_enable','timestamp_disable')
    list_display_links = ('device', 'contact')
