from django import forms

from .models import Device

class DeviceForm(forms.ModelForm):
    description = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}) )

    class Meta:
        model = Device
        fields = ('name', 'category','acronym','description',
                      'image','weight','length','sleeve','draft') 
        
