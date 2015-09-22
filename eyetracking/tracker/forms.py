from django import forms

class TrackerForm(forms.ModelForm):
    ip = forms.GenericIPAddressField()
    port = forms.IntegerField()
    OPTIONS = (
            (30, "30fps"),
            (60, "60fps"),
            )
    frame_rate = forms.ChoiceField(choices=OPTIONS)