from django import forms
from .models import Trial


class TrialUploadForm(forms.ModelForm):
	file = forms.FileField()

	class Meta:
		model = Trial
		fields = ['file']

class TrialUpdateForm(forms.ModelForm):

	class Meta:
		model = Trial
		fields = ['comments']