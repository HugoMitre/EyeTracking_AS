from django import forms
from .models import Trial


class TrialUploadForm(forms.ModelForm):
	file = forms.FileField()

	class Meta:
		model = Trial
		fields = ['file']

class TrialUpdateForm(forms.ModelForm):
	resolved = forms.BooleanField(label='Solved', required=False)
	LEVELS = (
        (1, 'Level 1'),
        (2, 'Level 2'),
		(3, 'Level 3'),
    )
	level = forms.ChoiceField(LEVELS)

	class Meta:
		model = Trial
		fields = ['resolved', 'level', 'errors', 'comments']