from django.contrib import admin


from competition.models import Race, TrackGeom
from competition.models import Champion, ListTraceRaces

from competition.models import RaceTracking, RaceTrackingNode,Penalty,PenaltyTracking,RaceCategory


class TrackGeomInline(admin.TabularInline):
    model = TrackGeom
    fk_name = 'race'
    extra = 0 # how many rows to show

class ListTraceRacesInline(admin.TabularInline):
    model = ListTraceRaces
    fk_name = 'champion'
    extra = 0 # how many rows to show
    
class RaceTrackingNodeInline(admin.TabularInline):
    model = RaceTrackingNode
    fk_name = 'racetracking'
    extra = 0 # how many rows to show
    
class PenaltyTrackingInline(admin.TabularInline):
    model = PenaltyTracking
    fk_name = 'racetracking'
    extra = 0 # how many rows to show

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('image_tag','name','edicion','get_status','organization')
    list_display_links = ('image_tag', 'name')
    
    fields = (('name','edicion','organization','status'),
              ('slug'),
              ('description'),
              ('timestamp_start','timestamp_finish'),
              ('image_tag','image'),
              ('limit_area','get_limits_JSN','get_limits_JSN_WGS84')
              )
    
    readonly_fields = ('image_tag','get_limits_JSN','get_limits_JSN_WGS84')
    
    
    inlines = [TrackGeomInline,]


@admin.register(Champion)
class ChampionAdmin(admin.ModelAdmin):
    list_display = ('image_tag','name','edicion','get_status','organization')
    list_display_links = ('image_tag', 'name')
    
    fields = (('name','edicion','organization','status'),
              ('slug'),
              ('description'),
              ('timestamp_start','timestamp_finish'),
              ('image_tag','image')
              )
    
    readonly_fields = ('image_tag',)
    
    inlines = [ListTraceRacesInline,]


@admin.register(RaceTracking)
class RaceTrackingAdmin(admin.ModelAdmin):
    list_display = ('device','code','race','timestamp_integrate')
    list_display_links = ('device', 'code')
    
    fields = (('device','race'),
              ('code','color','category'),
              ('timestamp_integrate'),
              ('observations')
              )
    
    
    inlines = [PenaltyTrackingInline,RaceTrackingNodeInline]

@admin.register(TrackGeom)
class TrackGeomAdmin(admin.ModelAdmin):
    list_display = ('race','device','get_type','get_pass','order')
    list_display_links = ('race', 'device')
    fields = (('race','device'),
              ('track_pass','order'),
              ('timestamp_enable','timestamp_disable'),
              ('geom','geom_JSN','geom_JSN_WGS84')
              )
    
    readonly_fields = ('geom_JSN','geom_JSN_WGS84')

@admin.register(ListTraceRaces)
class ListTraceRacesAdmin(admin.ModelAdmin):
    list_display = ('champion','race','order','is_enable')
    list_display_links = ('champion','race')

@admin.register(RaceTrackingNode)
class RaceTrackingNodeAdmin(admin.ModelAdmin):
    list_display = ('trackgeom','racetracking','timestamp_pass')
    list_display_links = ('trackgeom','racetracking')


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('name','get_type','description')
    list_display_links = ('name',)
    
@admin.register(RaceCategory)
class RaceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','code','description')
    list_display_links = ('name','code')
