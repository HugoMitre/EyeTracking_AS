import itertools
import django_tables2 as tables


class StatisticsTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='No.', sortable=False)
    image_name = tables.Column()
    participant_name = tables.Column()
    duration = tables.Column()
    errors = tables.Column()
    apcps = tables.Column(verbose_name='APCPS')
    mpd = tables.Column(verbose_name='MPD')
    mpdc = tables.Column(verbose_name='MPDC')
    lp = tables.Column(verbose_name='Latency to Peak')
    pd = tables.Column(verbose_name='Peak Dilation')
    #pdc = tables.Column(verbose_name='Peak Dilation Change')
    actions = tables.TemplateColumn(orderable=False, template_name='statistics/statistic_actions.html', attrs={"td": {"nowrap":"nowrap"}})

    class Meta:
        attrs = {"class": "table-responsive"}

    def __init__(self, *args, **kwargs):
        super(StatisticsTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return next(self.counter) + 1