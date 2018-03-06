from django.conf.urls import include,url


from . import views 


urlpatterns = [
    url(r'^(?P<device_slug>[\w-]+)/', include([
        url(r'^$',  views.summary, name='device_summary'),
        url(r'^detail/$',  views.detail, name='device_detail'),
        url(r'^edit/$',  views.edit, name='device_edit'),
        url(r'^calibration/$', views.calibration, name='device_calibration'),
        url(r'^telemetry/$', views.telemetry, name='device_telemetry'),
    ])),
]
