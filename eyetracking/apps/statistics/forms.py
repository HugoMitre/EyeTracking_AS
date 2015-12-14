from django import forms
from .models import Statistic


class StatisticForm(forms.ModelForm):
	
	name = forms.CharField(widget=forms.TextInput(attrs={'autofocus':''}))

