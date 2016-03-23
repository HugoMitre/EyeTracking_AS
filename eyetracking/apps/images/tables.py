import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from .models import Image
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape
from eyetracking.settings import MEDIA_URL

class PhotoTable(tables.Table):
    id = tables.Column(orderable=True)
    resized_image = tables.Column(orderable=False)
    original_name = tables.LinkColumn('images:detail_image', args=[A('pk')])
    width = tables.Column()
    actions = tables.TemplateColumn(orderable=False, empty_values=(), template_name='images/actions.html')
    size = tables.Column(orderable=False)

    class Meta:
        model = Image
        fields = ('id', 'resized_image', 'original_name', 'size', 'width')

    def render_resized_image(self, value, record):
        link_detail = reverse("images:detail_image", args=[record.pk])
        return mark_safe('<a href="' + link_detail + '" ><img src="' + MEDIA_URL + '/%s" /> </a>' % escape(value))

    def render_width(self, record):
        return '%s x %s' % (record.width, record.height)


