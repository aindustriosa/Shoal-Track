from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required


from django_tables2 import RequestConfig
from .tables import DeviceDataRawTable, DataProcessingTable,DataProcessingDeviceTable

from .models import Device
from .forms import DeviceForm

from telemetrydata.models import DeviceDataRaw,DataProcessing
from telemetrydata.forms import DataProcessingForm
# Create your views here.


def summary(request, device_slug=False):
    ''' informacin basica del dispositivo
    '''
    output =device_slug
    return HttpResponse(output)

def detail(request, device_slug=False):
    ''' inforaciondetallada: 
       campeonatos y posiicon
       carreras y posicion
    '''
    output =device_slug
    return HttpResponse(output)

@login_required
def edit(request, device_slug=False):
    ''' Editar un dispositivo
    '''
    try:
        device = Device.objects.filter(acronym=device_slug).get()
    except:
        return HttpResponse("No find Champioship entry.")
    
    if request.method == "POST":
        form_device = DeviceForm(request.POST, instance=device)
        if form_device.is_valid():
            post = form_device.save(commit=False)
            #post.author = request.user
            post.save()
            return redirect('device_detail', device_slug=device.acronym)
    else:
        form_device = DeviceForm(instance=device)
    
    #la lista de calibraciones:
    qCalibrations = DataProcessing.objects.filter(device=device).order_by('-timestamp')
    tableCalibrt = DataProcessingDeviceTable(qCalibrations)
    RequestConfig(request).configure(tableCalibrt)
        
    return render(request, 'device_edit.html', {'img': device.image_tag(),
                                                'acronym': device.acronym,
                                                'device': form_device,
                                                'tableCalibrt':tableCalibrt})


def calibration(request, device_slug=False):
    ''' muestra sus parametros y puede calibrar datos
    '''
    qDevice = Device.objects.filter(acronym=device_slug).get()
    qCalibrations = DataProcessing.objects.filter(device=qDevice).order_by('-timestamp')
    
    tableData = DataProcessingTable(qCalibrations)
    RequestConfig(request).configure(tableData)
    
    return render(request, 'calibration_data.html', {'table': tableData,
                                                     'device_name':qDevice.name})

def telemetry(request, device_slug=False):
    ''' muestra listado de telemetrias (con su carrera... si esta asociada)
    '''
    
    qDevice = Device.objects.filter(acronym=device_slug).get()
    
    qDatas = DeviceDataRaw.objects.filter(device=qDevice).order_by('-timestamp')
    
    
    tableData = DeviceDataRawTable(qDatas)
    RequestConfig(request).configure(tableData)
    
    return render(request, 'device_data.html', {'table': tableData,
                                                'device_name':qDevice.name})
    
