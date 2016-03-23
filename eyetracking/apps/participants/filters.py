import django_filters as df
from .models import Participant

class ParticipantFilter(df.FilterSet):
    first_name = df.CharFilter(lookup_type='icontains')

    class Meta:
        model = Participant
        fields = ['first_name', 'last_name']