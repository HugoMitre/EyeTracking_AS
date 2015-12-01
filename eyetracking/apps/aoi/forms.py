from django import forms
from .models import AOI


class AOIForm(forms.ModelForm):
	
    class Meta:
        model = AOI
        fields = [ 'image', 'name', 'top', 'left', 'height', 'width', 'type']
