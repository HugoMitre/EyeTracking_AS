from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from vanilla import CreateView, DetailView, UpdateView, RedirectView
from django_tables2 import SingleTableView
from .forms import StatisticForm
from .models import Statistic
from .tables import StatisticTable


class StatisticList(SingleTableView):
    model = Statistic
    table_class = StatisticTable
    table_pagination = {'per_page': 10}


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
