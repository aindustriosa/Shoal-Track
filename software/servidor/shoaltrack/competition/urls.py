from django.conf.urls import include,url


from . import views
'''
urlpatterns = [
    # ex: /champion/
    
    
    
    url(r'^$', views.summary, name='summary'),
    
    url(r'^results/champion/(?P<slug>[\w-]+)/$', views.champion_results, name='race_detail'),
    url(r'^results/race/(?P<slug>[\w-]+)/$', views.race_results, name='race_detail'),
    url(r'^results/device/(?P<code>[\w-]+)/$', views.node_results, name='node_detail'),
    
    url(r'^service/update/(?P<service>[\w-]+)/$', views.update_data, name='node_detail'),
    url(r'^service/lastdata/(?P<slug>[\w-]+)/(?P<amount>[0-9]{2})/$', views.last_data, name='last_data'),
    
    url(r'^(?P<slug>[\w-]+)/$', views.champion_detail, name='champion_detail'),
    
]
'''

urlpatterns = [
    url(r'^(?P<championship_slug>[\w-]+)/', include([
        url(r'^$',  views.summary, name='champion_summary'),
        url(r'^detail/$',  views.detail, name='champion_detail'),
        url(r'^devices/$', views.devices, name='champion_devices'),
        url(r'^teams/$', views.teams, name='champion_teams'),
        url(r'^adwars/$', views.adwars, name='champion_adwars'),
        url(r'^lastdata/(?P<amount>[0-9]{2})$', views.last_data, name='champion_lastNdata'),
        url(r'^lasttelemetry/$', views.last_telemetry, name='champion_lasttelemetry'),
    ])),
]
