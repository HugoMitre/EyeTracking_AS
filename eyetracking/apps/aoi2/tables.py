import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from .models import AOI


class AOITable(tables.Table):
    name = tables.LinkColumn('aoi:detail', args=[A('pk')])
    actions = tables.TemplateColumn(orderable=False, empty_values=(), template_name='aoi/aoi_actions.html')

    class Meta:
        model = AOI
        fields = ('name',)
