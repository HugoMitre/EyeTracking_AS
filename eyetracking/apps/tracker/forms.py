from django import forms
from .models import Tracker


class TrackerForm(forms.ModelForm):

    class Meta:
        model = Tracker
        exclude = ()


class RecordForm(forms.Form):

    time = forms.IntegerField()
