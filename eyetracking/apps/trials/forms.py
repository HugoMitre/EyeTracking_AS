from django import forms
from .models import Trial


class TrialForm(forms.ModelForm):
	file = forms.FileField()

	class Meta:
		model = Trial
		fields = ['file']
