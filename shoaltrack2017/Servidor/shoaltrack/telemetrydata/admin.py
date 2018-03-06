from django.contrib import admin


from telemetrydata.models import DeviceDataRaw, DataProcessing



@admin.register(DeviceDataRaw)
class DeviceDataRawAdmin(admin.ModelAdmin):
    list_display = ('timestamp','device','millisecons','latitude','longitude')
    list_display_links = ('timestamp', 'device')
    
    fields = (('device','timestamp','millisecons'),
              ('geom','geom_JSN','geom_JSN_WGS84'),
              ('latitude_raw','longitude_raw'),
              ('accX_raw','accX_coef'),
              ('accY_raw','accY_coef'),
              ('accZ_raw','accZ_coef'),
              ('gyrX_raw','gyrX_coef'),
              ('gyrY_raw','gyrY_coef'),
              ('gyrZ_raw','gyrZ_coef'),
              ('magX_raw','magX_coef'),
              ('magY_raw','magY_coef'),
              ('magZ_raw','magZ_coef'),
              ('press_air_raw','press_air_coef'),
              ('temp_int_raw','temp_int_coef'),
              ('temp_air_raw','temp_air_coef'),
              ('temp_water_raw','temp_water_coef'),
              ('ldr_fl_raw','ldr_fr_coef'),
              ('ldr_fr_raw','ldr_fl_coef'),
              ('ldr_bl_raw','ldr_br_coef'),
              ('ldr_br_raw','ldr_bl_coef'),
              ('power_volt','power_volt_coef'),
              ('power_amp','power_amp_coef')
              )
    
    readonly_fields = ('geom_JSN','geom_JSN_WGS84')


@admin.register(DataProcessing)
class DataProcessingAdmin(admin.ModelAdmin):
    list_display = ('timestamp','device','type_param','type_equation','args')
    list_display_links = ('timestamp', 'device')
