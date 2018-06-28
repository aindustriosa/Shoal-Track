import django_tables2 as tables
from .models import Device, TeamTrace
from telemetrydata.models import DeviceDataRaw, DataProcessing
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ButtonColum(tables.Column): 
    empty_values = list() 
    def render(self, value, record): 
        button ='<button onclick='
        button +='"return activity_popup('
        button +="'/shoaltrack/telemetry/"
        button +=record.device.acronym
        button +='/calibration/edit/'
        button +=str(record.pk)
        button += "')"
        button +='">Modificar</button>'
        
        return mark_safe(button)
'''
class ImageColumn(tables.Column):
    def render(self, value):
        return mark_safe('<img src="/media/%s" />' % escape(value))
'''

class DeviceDataRawTable(tables.Table):
    class Meta:
        model = DeviceDataRaw
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'} 

class DataProcessingTable(tables.Table):
    class Meta:
        model = DataProcessing
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'} 

class DataProcessingDeviceTable(tables.Table):
    editable = ButtonColum(orderable=False) # just add a field here
    
    class Meta:
        model = DataProcessing
        fields = ('pk','timestamp','type_param', 'type_equation', 'args')
        #fields = ('resource__name','resource__code', 'name_ATON', 'name_WMO','status_mode')
        
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'} 
      
    
    #def render_resource__image_tag(self, value):#reago la peticion de salida..
    #   return mark_safe(value)
