from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from vanilla import CreateView, DetailView, UpdateView, RedirectView
from django_tables2 import SingleTableView
from .forms import ParticipantForm
from .models import Participant
from .tables import ParticipantTable
from .filters import ParticipantFilter
from .utils import PagedFilteredTableView


class ParticipantList(SingleTableView):
    #PagedFilteredTableView
    model = Participant
    table_class = ParticipantTable
    table_pagination = {'per_page': 10}
    #filter_class = ParticipantFilter

    total = Participant().get_total()
    male, female = Participant().count_gender(total)
    mean = Participant().mean()
    sd = Participant().sd()


class ParticipantCreate(SuccessMessageMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('participants:list')
    success_message = "%(first_name)s %(last_name)s was created successfully"


class ParticipantDetail(DetailView):
    model = Participant


class ParticipantUpdate(SuccessMessageMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('participants:list')
    success_message = "%(first_name)s %(last_name)s was updated successfully"


class ParticipantDelete(RedirectView):
    model = Participant

    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse_lazy('participants:list')
        self.permanent = True
        model = get_object_or_404(Participant, pk=kwargs['pk'])
        name = model.first_name + ' ' + model.last_name
        model.delete()
        messages.success(self.request, name + ' was deleted successfully')
        return super(ParticipantDelete, self).get_redirect_url(*args, **kwargs)
