from django import forms

from .models import DataProcessing

class DataProcessingForm(forms.ModelForm):
    
    class Meta:
        model = DataProcessing
        fields = ('timestamp', 'type_param','type_equation','args') 
        
 
