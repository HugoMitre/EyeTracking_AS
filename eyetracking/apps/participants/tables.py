import django_tables2 as tables
from django.utils.safestring import mark_safe
from .models import Participant


class ParticipantTable(tables.Table):
    id = tables.Column(sortable=True)
    first_name = tables.Column()
    actions = tables.TemplateColumn(orderable=False, empty_values=(), template_name='participants/participant_actions.html')

    class Meta:
        model = Participant
        fields = ('id', 'first_name', 'gender', 'age')

    def render_first_name(self, value, record):
        return mark_safe('''<a href=%s>%s</a>''' % (record.id, value + ' ' + record.last_name))