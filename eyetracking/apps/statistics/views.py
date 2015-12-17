from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from vanilla import CreateView, DetailView, UpdateView, RedirectView, TemplateView
from.features import point_inside_polygon, get_data_shapes
from apps.images.models import Image
from apps.tracker.models import TrackerData
from apps.aoi.models import AOI


class StatisticList(TemplateView):
    template_name = 'statistics/statistic_list.html'

    def get_context_data(self, **kwargs):
        id_first_image = ''
        images = Image.objects.all()

        if (images):
            id_first_image = images[0].pk

        return {'images': images, 'id_first_image':id_first_image}


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def render_to_http_response(self, context, **response_kwargs):

        return HttpResponse(self.get_data(context), content_type='application/json')

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class StatisticFeature(JSONResponseMixin, TemplateView):

    def get_context_data(self, **kwargs):
        image_id = self.request.GET.get('image_id')

        # Check if exists image
        image = get_object_or_404(Image, pk=image_id)

        # Get all aoi related to image
        aoi = AOI.objects.filter(image=image.id)

        # Obtain data points for aoi
        shapes = get_data_shapes(aoi)

        # Get fixation data
        fixations = TrackerData.objects.values('avg_x', 'avg_y')

        # Calculate features
        for fixation in fixations:
            x = fixation['avg_x']
            y = fixation['avg_y']

            #Check if the fixation point is inside an aoi
            for shape in shapes:
                inside = point_inside_polygon(x, y, shape['points'])

                if inside:
                    shape['visit_count']+=1

        return {'shapes':shapes}

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)