import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from .models import Photo
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape
from eyetracking.settings import MEDIA_URL

class PhotoTable(tables.Table):

    resized_image = tables.Column(orderable=False)
    original_name = tables.LinkColumn('images:detail_image', args=[A('pk')])
    width = tables.Column()
    actions = tables.Column(orderable=False, empty_values=())
    size = tables.Column(orderable=False)

    class Meta:
        model = Photo
        fields = ('resized_image', 'original_name', 'size', 'width')

    def render_resized_image(self, value, record):
        link_detail = reverse("images:detail_image", args=[record.pk])
        return mark_safe('<a href="' + link_detail + '" ><img src="' + MEDIA_URL + '/%s" /> </a>' % escape(value))

    def render_width(self, record):
        return '%s x %s' % (record.width, record.height)

    def render_actions(self, record):
        link_edit = reverse("images:update_image", args=[record.pk])
        link_delete = reverse("images:delete_image", args=[record.pk])
        btn_edit = '<a class="btn btn-primary btn-sm tooltip-btn" data-toggle="tooltip" data-placement="top" data-original-title="Update" href=' + \
            link_edit + '><i class="glyphicon glyphicon-edit"></i></a>'
        btn_delete = '<a class="btn btn-danger btn-sm tooltip-btn delete-link" data-toggle="tooltip" data-placement="top" data-original-title="Delete" data-delete-url=' + \
            link_delete + '><i class="glyphicon glyphicon-trash"></i></a>'
        return mark_safe(btn_edit + ' ' + btn_delete)

