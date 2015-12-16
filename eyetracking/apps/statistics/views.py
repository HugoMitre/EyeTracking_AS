from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from vanilla import CreateView, DetailView, UpdateView, RedirectView, TemplateView
from .forms import StatisticForm
from .models import Statistic
from apps.images.models import Image


class StatisticList(TemplateView):
    template_name = 'statistics/statistic_list.html'

    def get_context_data(self, **kwargs):
        id_first_image = ''
        images = Image.objects.all()

        if (images):
            id_first_image = images[0].pk

        return {'images': images, 'id_first_image':id_first_image}


class StatisticCreate(SuccessMessageMixin, CreateView):
    model = Statistic
    form_class = StatisticForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('statistics:list')
    success_message = "%(name)s was created successfully"


class StatisticDetail(DetailView):
    model = Statistic


class StatisticUpdate(SuccessMessageMixin, UpdateView):
    model = Statistic
    form_class = StatisticForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('statistics:list')
    success_message = "%(name)s was updated successfully"


class StatisticDelete(RedirectView):
    model = Statistic

    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse_lazy('statistics:list')
        model = get_object_or_404(Statistic, pk=kwargs['pk'])
        name = model.name
        model.delete()
        messages.success(self.request, name + ' was deleted successfully')
        return super(StatisticDelete, self).get_redirect_url(*args, **kwargs)
