import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from images.models import Image
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class ImageTable(tables.Table):
    name = tables.LinkColumn('images:detail_image', args=[A('pk')])
    actions = tables.Column(orderable=False, empty_values=())

    class Meta:
        model = Image
        fields = ('name', 'resolution', 'size')

    def render_size(self, value):
        return '%s MB' % value

    def render_actions(self, record):
        link_edit = reverse("images:update_image", args=[record.pk])
        link_delete = reverse("images:delete_image", args=[record.pk])
        btn_edit = '<a class="btn btn-primary btn-sm tooltip-btn" data-toggle="tooltip" data-placement="top" data-original-title="Update" href=' + \
            link_edit + '><i class="glyphicon glyphicon-edit"></i></a>'
        btn_delete = '<a class="btn btn-danger btn-sm tooltip-btn delete-link" data-toggle="tooltip" data-placement="top" data-original-title="Delete" data-delete-url=' + \
            link_delete + '><i class="glyphicon glyphicon-trash"></i></a>'
        return mark_safe(btn_edit + ' ' + btn_delete)
