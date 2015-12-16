from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.conf import settings
from vanilla import CreateView, UpdateView, TemplateView
from apps.images.models import Image
from .forms import AOIForm
from .models import AOI


class AOIList(TemplateView):
    template_name = 'aoi/aoi_draw.html'

    def get_context_data(self, **kwargs):
        id_first_image = ''
        images = Image.objects.all()

        if (images):
            id_first_image = images[0].pk

        return {'images': images, 'id_first_image':id_first_image}


class AjaxableResponseMixin(object):

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            context,
            **response_kwargs
        )

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


class AOIGetInfoImage(JSONResponseMixin, TemplateView):

    def get_context_data(self, **kwargs):
        id = self.request.GET.get('image_id')
        model = get_object_or_404(Image, pk=id)
        return {'id':model.id, 'image':settings.MEDIA_URL+model.image.name, 'height':model.height, 'width':model.width}

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class AOIGetShapes(JSONResponseMixin, TemplateView):

    def get_context_data(self, **kwargs):
        image_id = self.request.GET.get('image_id')
        model = AOI.objects.filter(image=image_id)
        serialized_queryset = serializers.serialize('json', model)
        return serialized_queryset

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['safe'] = False
        return self.render_to_http_response(context, **response_kwargs)


class AOIDelete(JSONResponseMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        id =  self.kwargs['pk']
        AOI.objects.filter(id=id).delete()
        return {'success':True}

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class AOIChangeName(JSONResponseMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        id =  self.kwargs['pk']
        name = self.request.POST.get('name')
        AOI.objects.filter(id=id).update(name=name)
        return {'success':True}

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)