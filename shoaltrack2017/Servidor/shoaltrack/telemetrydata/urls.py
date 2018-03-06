from django.conf.urls import include,url


from . import views 


urlpatterns = [
    url(r'^(?P<device_acro>[\w-]+)/', include([
        url(r'^calibration/new$',  views.new, name='calibration_new'),
        url(r'^calibration/edit/(?P<pk>\d+)/$',  views.edit, name='calibration_edit'),
        url(r'^calibration/graph/(?P<pk>\d+)/plotgraph.png$',  views.plotgraph, name='calibration_graph'),
    ])),
]
 
