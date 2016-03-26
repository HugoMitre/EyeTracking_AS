from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings
import django_tables2 as tables
from .models import Trial, TrialData


class TrialTable(tables.Table):
    image = tables.Column(verbose_name='Image', orderable=False)
    trial_name = tables.Column(empty_values=())
    participant = tables.Column(verbose_name='Participant')
    duration = tables.Column(empty_values=())
    percentage_samples = tables.Column(verbose_name='Samples')
    actions = tables.TemplateColumn(orderable=False, empty_values=(), template_name='trials/trial_actions.html')

    class Meta:
        model = Trial
        fields = ('image', 'trial_name', 'participant', 'duration', 'percentage_samples')

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


class TrialDataTable(tables.Table):

    timestamp = tables.DateTimeColumn(verbose_name='Timestamp')
    avg_x = tables.Column(verbose_name='Average X')
    avg_y = tables.Column(verbose_name='Average Y')
    left_pupil_size = tables.Column(verbose_name='Left pupil size')
    right_pupil_size = tables.Column(verbose_name='Right pupil size')
    distance = tables.Column(verbose_name='Distance')

    class Meta:
        model = TrialData
        fields = ('timestamp', 'avg_x', 'avg_y', 'left_pupil_size', 'right_pupil_size', 'distance')
