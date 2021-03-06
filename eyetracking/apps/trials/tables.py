from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings
import django_tables2 as tables
from .models import Trial


class TrialTable(tables.Table):
    image = tables.Column(verbose_name='Image', orderable=False)
    trial_name = tables.Column(empty_values=())
    level = tables.Column(verbose_name='Level')
    participant = tables.Column(verbose_name='Participant')
    duration = tables.Column(empty_values=(), orderable=False)
    percentage_samples = tables.Column(verbose_name='Samples')
    resolved = tables.Column(verbose_name='Solved')
    tr_class=tables.Column(visible=False, empty_values=())
    actions = tables.TemplateColumn(orderable=False, empty_values=(), template_name='trials/trial_actions.html', attrs={"td": {"nowrap":"nowrap"}})

    class Meta:
        model = Trial
        fields = ('image', 'trial_name', 'level', 'participant', 'duration', 'percentage_samples', 'resolved', 'tr_class')

    def render_image(self, value, record):
        return mark_safe('<img src="' + settings.MEDIA_URL + '/%s" />' % escape(value.resized_image))

    def render_trial_name(self, value, record):
        return mark_safe('''<a href=%s>%s</a>''' % (record.id, record.image.original_name))

    def render_participant(self, value, record):
        return value.first_name + ' ' + value.last_name

    def render_duration(self, record):
        return record.end_date - record.start_date

    def render_percentage_samples(self, value):
        return str(value) + ' %'

    def render_resolved(self, value):
        return mark_safe('''<span class="label label-success">Yes</span>''') if value else mark_safe('''<span class="label label-danger">No</span>''')

    def render_tr_class(self, value, record):
        if record.percentage_samples < 80.0 or record.resolved == False:
            return 'danger'
        else:
            return 'success'