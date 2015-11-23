from django import forms
from .models import Image


class PhotoForm(forms.ModelForm):

    original_name = forms.CharField(label='Name', max_length=255, error_messages={'required': 'Name is required.'})

    class Meta:
        model = Image
        fields = ('original_name',)