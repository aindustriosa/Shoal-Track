from devices.models import Device,TeamTrace
from profiles.models import Organization, Contact



def parse_championship_device(qDevice):
    '''dado u na consulta Query, obtengo un diccionario con las
    propiedades del dispositivo
    '''
    output ={}
    output['img']=qDevice.image_tag()
    output['acro']=qDevice.acronym
    output['name']=qDevice.name
    output['cat']=qDevice.get_type()
    output['descript']=qDevice.description
    output['weight']=qDevice.weight
    output['length']=qDevice.length
    output['sleeve']=qDevice.sleeve
    output['draft']=qDevice.draft
    
    #su dueño
    output['owner_img']=qDevice.owner.image_tag('low')
    output['owner_name']=qDevice.owner.name
    
    #listado de componenees
    output['team1']=[]
    output['team2']=[]
    output['team3']=[]
    output['team4']=[]
    count = 1
    for team_unit in qDevice.team.all():
        qRelation =TeamTrace.objects.filter(device=qDevice,
                                                                   contact=team_unit).get()
        
        item = {'img':team_unit.image_tag(),
                     'name':team_unit.get_idName(),
                     'rol':qRelation.get_rol()}
        if count > 15:
            output['team4'].append(item)
        elif count > 10:
            output['team3'].append(item)
        elif count > 5:
            output['team2'].append(item)
        else:
            output['team1'].append(item)
        count +=1
    
    return output
    
def parse_championship_team(qDevice):
    '''dado u na consulta Query, obtengo un diccionario con las
    propiedades del dispositivo
    '''
    output ={}
    output['img']=qDevice.owner.image_tag()
    output['acro']=qDevice.owner.acronym
    output['name']=qDevice.owner.name
    output['country']=qDevice.owner.country
    output['telephone']=qDevice.owner.telephone
    output['email']=qDevice.owner.email
    output['web']=qDevice.owner.homepage
   
    
    #sus integrantes
    
    #listado de componenees
    output['team1']=[]
    output['team2']=[]
    output['team3']=[]
    output['team4']=[]
    count = 1
    for team_unit in qDevice.team.all():
        qRelation =TeamTrace.objects.filter(device=qDevice,
                                            contact=team_unit).get()
        
        item = {'img':team_unit.image_tag(),
                 'name':str(team_unit),
                 'email':team_unit.email,
                 'rol':qRelation.get_rol(),
                 'enable':qRelation.timestamp_enable,
                 'disable':qRelation.timestamp_disable}
        if count > 15:
            output['team4'].append(item)
        elif count > 10:
            output['team3'].append(item)
        elif count > 5:
            output['team2'].append(item)
        else:
            output['team1'].append(item)
        count +=1
    
    return output
