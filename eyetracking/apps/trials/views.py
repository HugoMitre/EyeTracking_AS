import os
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from vanilla import CreateView, DetailView, RedirectView
from django_tables2 import SingleTableView
from .forms import TrialForm
from .models import Trial, TrialData
from .tables import TrialTable, TrialDataTable


class TrialList(SingleTableView):
    model = Trial
    table_class = TrialTable
    table_pagination = {'per_page': 10}


class TrialCreate(SuccessMessageMixin, CreateView):
    model = Trial
    form_class = TrialForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('trials:list')
    success_message = "Trial was created successfully"


class TrialDetail(DetailView):
    model = Trial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TrialDetail, self).get_context_data(**kwargs)

        # Add in a QuerySet duration and samples
        context['duration'] = context['object'].end_date - context['object'].start_date
        context['samples'] = TrialData.percentage_samples(context['object'].id)
        return context


class TrialDelete(RedirectView):
    model = Trial

    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse_lazy('trials:list')
        model = get_object_or_404(Trial, pk=kwargs['pk'])
        try:
            with transaction.atomic():
                TrialData.objects.filter(trial=model.pk).delete()
                model.delete()
                os.unlink(model.file.path)
                messages.success(self.request, 'Trial was deleted successfully')
        except IntegrityError:
            messages.error(self.request, 'The request was unsuccessful')

        return super(TrialDelete, self).get_redirect_url(*args, **kwargs)


class TrialDataList(SingleTableView):
    model = TrialData
    table_class = TrialDataTable
    table_pagination = {'per_page': 100}