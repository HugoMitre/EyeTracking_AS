from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from vanilla import CreateView, DetailView, UpdateView, RedirectView
from django_tables2 import SingleTableView
from .forms import AOIForm
from .models import AOI
from .tables import AOITable


class AOIList(SingleTableView):
    model = AOI
    table_class = AOITable
    table_pagination = {'per_page': 10}


class AOICreate(SuccessMessageMixin, CreateView):
    model = AOI
    form_class = AOIForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('aoi:list')
    success_message = "%(name)s was created successfully"


class AOIDetail(DetailView):
    model = AOI


class AOIUpdate(SuccessMessageMixin, UpdateView):
    model = AOI
    form_class = AOIForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('aoi:list')
    success_message = "%(name)s was updated successfully"


class AOIDelete(RedirectView):
    model = AOI

    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse_lazy('aoi:list')
        model = get_object_or_404(AOI, pk=kwargs['pk'])
        name = model.name
        model.delete()
        messages.success(self.request, name + ' was deleted successfully')
        return super(AOIDelete, self).get_redirect_url(*args, **kwargs)
