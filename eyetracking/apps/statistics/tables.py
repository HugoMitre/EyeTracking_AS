import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from .models import Statistic


class StatisticTable(tables.Table):
    name = tables.LinkColumn('statistics:detail', args=[A('pk')])
    actions = tables.TemplateColumn(orderable=False, empty_values=(), template_name='statistics/statistic_actions.html')

    class Meta:
        model = Statistic
        fields = ('name',)
