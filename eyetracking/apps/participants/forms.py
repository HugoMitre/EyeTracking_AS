from django import forms
from .models import Participant


class ParticipantForm(forms.ModelForm):

    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'autofocus':''}))

    age = forms.IntegerField(min_value=1, widget=forms.TextInput(),
                             error_messages={'invalid': 'Enter a valid value',
                                             'min_value':'Value must be greater than or equal 1'})

    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'age', 'gender']
