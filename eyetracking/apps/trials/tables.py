import django_tables2 as tables
#from django_tables2.utils import A  # alias for Accessor
from django.utils.safestring import mark_safe
from django.utils.html import escape
from eyetracking.settings import MEDIA_URL
from .models import Trial, TrialData


class TrialTable(tables.Table):
    participant = tables.Column(verbose_name='Participant')
    trial_name = tables.Column(empty_values=())
    image = tables.Column(verbose_name='Image', orderable=False)
    duration = tables.Column(empty_values=())
    samples = tables.Column(empty_values=())
    actions = tables.TemplateColumn(orderable=False, empty_values=(), template_name='trials/trial_actions.html')

    class Meta:
        model = Trial
        fields = ('image', 'trial_name', 'participant', 'duration', 'samples')

    def render_image(self, value, record):
        return mark_safe('<img src="' + MEDIA_URL + '/%s" />' % escape(value.resized_image))

    def render_trial_name(self, value, record):
        return mark_safe('''<a href=%s>%s</a>''' % (record.id, record.image.original_name))

    def render_participant(self, value, record):
        return value.first_name + ' ' + value.last_name

    def render_duration(self, record):
        return record.end_date - record.start_date

    def render_samples(self, record):
        return TrialData.percentage_samples(record.id)


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

