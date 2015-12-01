from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from vanilla import CreateView, UpdateView, RedirectView, TemplateView
from apps.images.models import Image
from .forms import AOIForm
from .models import AOI
import json


class AOIList(TemplateView):
    template_name = 'aoi/aoi_list.html'

    def get_context_data(self, **kwargs):
        first_image = ''
        id_first_image = ''
        images = Image.objects.all()

        if (images):
            first_image = settings.MEDIA_URL + images[0].image.name
            id_first_image = images[0].pk

        return {'photos': images, 'first_image': first_image, 'id_first_image':id_first_image}


class AjaxableResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response


class AOICreate(AjaxableResponseMixin, CreateView):
    model = AOI
    form_class = AOIForm
    success_url = ' '


class AOIUpdate(AjaxableResponseMixin, UpdateView):
    model = AOI
    form_class = AOIForm
    success_url = ' '


class AOIDelete(RedirectView):
    model = AOI

    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse_lazy('aoi:list')
        model = get_object_or_404(AOI, pk=kwargs['pk'])
        name = model.name
        model.delete()
        messages.success(self.request, name + ' was deleted successfully')
        return super(AOIDelete, self).get_redirect_url(*args, **kwargs)


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

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class AOIGetUrlImage(JSONResponseMixin, TemplateView):

    def get_context_data(self, **kwargs):
        id = self.request.GET.get('id')
        model = get_object_or_404(Image, pk=id)
        return {'urlPhoto': settings.MEDIA_URL+model.image.name}

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

