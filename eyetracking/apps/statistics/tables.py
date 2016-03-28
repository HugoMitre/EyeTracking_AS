import itertools
import django_tables2 as tables
from ..trials.models import TrialData, TrialFeatures

class StatisticsTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='No.', sortable=False)
    trial_name = tables.Column(verbose_name='Trial Name', empty_values=(), order_by=("trial.image.original_name"))
    participant = tables.Column(empty_values=(), order_by=("trial.participant.first_name", "trial.participant.last_name"))
    duration = tables.Column(empty_values=(), sortable=False)
    errors = tables.Column(empty_values=(), order_by=("trial.errors"))
    apcps = tables.Column(verbose_name='APCPS')
    mpd = tables.Column(verbose_name='MPD')
    mpdc = tables.Column(verbose_name='MPDC')
    actions = tables.TemplateColumn(orderable=False, template_name='statistics/statistic_actions.html', attrs={"td": {"nowrap":"nowrap"}})

    class Meta:
        model = TrialFeatures
        fields = ('row_number', 'trial_name', 'participant', 'duration', 'errors', 'apcps', 'mpd', 'mpdc')

    def __init__(self, *args, **kwargs):
        super(StatisticsTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return next(self.counter) + 1

    def render_trial_name(self, record):
        return record.trial.image.original_name

    def render_participant(self, record):
        return record.trial.participant.first_name + ' ' + record.trial.participant.last_name

    def render_duration(self, record):
        return record.trial.end_date - record.trial.start_date

    def render_errors(self, record):
        return record.trial.errors


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
