from django.contrib.gis import admin


from telemetrydata.models import DeviceDataRaw, DataProcessing



@admin.register(DeviceDataRaw)
class DeviceDataRawAdmin(admin.OSMGeoAdmin):
    list_display = ('timestamp','device','gps_itow','latitude','longitude')
    list_display_links = ('timestamp', 'device')
    
    fields = (('device','timestamp','timestamp_rcv'),
              ('nextHop','rssi'),
              ('geom','geom_JSN','geom_JSN_WGS84'),
              ('gps_precision','gps_itow','gps_heading'),
              ('gps_latitude','gps_longitude'),
              ('bearing_avg','bearing_std','bearing_coef'),
              ('voltage_batt_avg','voltage_batt_std','voltage_batt_coef'),
              ('amp_batt_avg','amp_batt_std','amp_batt_coef'), 
              ('pressure_avg','pressure_std','pressure_coef'), 
              ('ligth_avg','ligth_std','ligth_coef'), 
              ('accX_avg','accX_std','accX_coef'), 
              ('accY_avg','accY_std','accY_coef'), 
              ('accZ_avg','accZ_std','accZ_coef'), 
              ('gyrX_avg','gyrX_std','gyrX_coef'), 
              ('gyrY_avg','gyrY_std','gyrY_coef'), 
              ('gyrZ_avg','gyrZ_std','gyrZ_coef'), 
              ('ref_air_temp','ref_pressure','ref_humidity_relative'),
              ('ref_wind_module','ref_wind_direction'),
              ('ranking','velocity','direction')
              )
    
    readonly_fields = ('geom_JSN','geom_JSN_WGS84')


@admin.register(DataProcessing)
class DataProcessingAdmin(admin.ModelAdmin):
    list_display = ('timestamp','device','type_param','type_equation','args')
    list_display_links = ('timestamp', 'device')
