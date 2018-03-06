from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import random

from devices.models import Device
from telemetrydata.models import DeviceDataRaw,DataProcessing
from telemetrydata.forms import DataProcessingForm

from telemetrydata.equations import graph_linear



# Create your views here.

@login_required
def new(request, device_acro=False):
    try:
        device = Device.objects.filter(acronym=device_acro).get()
    except:
        return HttpResponse("No find Device to calibrate.")
    
    
    output =device_acro
    return HttpResponse(device_acro)

@login_required
def edit(request, device_acro,pk):
    ''' Editar una calibracion
    '''
    try:
        calibration = DataProcessing.objects.filter(pk=pk).get()
        device = Device.objects.filter(acronym=device_acro).get()
    except:
        return HttpResponse("No find Calibration to edit.")
    
    #añado identificaodre
    
    if request.method == "POST":
        form_calibrate = DataProcessingForm(request.POST, instance=calibration)
        if form_calibrate.is_valid():
            form_calibrate.save()
            return redirect('calibration_edit', device_acro=device.acronym, pk=calibration.pk)
    else:
        form_calibrate = DataProcessingForm(instance=calibration)
        
        
    #genero la direccion de la grafica:
    
    graphic = '/shoaltrack/telemetry/'+device.acronym+'/calibration/graph/'+str(calibration.pk)+'/plotgraph.png'
    
        
    return render(request, 'calibration_edit.html', {'calibration': form_calibrate,
                                                     'device':device,
                                                     'graphic':graphic})

@login_required
def plotgraph(request, device_acro,pk):
    ''' mostrar la grafica de una calibracion
    '''
    try:
        calibration = DataProcessing.objects.filter(pk=pk).get()
        device = Device.objects.filter(acronym=device_acro).get()
    except:
        return HttpResponse("No find Calibration to edit.")
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    
    x,y = graph_linear(constants=calibration.get_args())
    
    ax.plot(x, y,)
    
    verbose_param = calibration.get_type_param()
    verbose_param
    
    ax.set_xlabel("Raw data")
    ax.set_ylabel("Calibrated Data "+verbose_param.split(' ')[-1])
    ax.grid(True)
    
    title = '{} calibration for parameter {} and device {}'.format(calibration.get_type_equation(),
                                           calibration.get_type_param(),
                                           calibration.device.name)
    ax.set_title(title)

    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

