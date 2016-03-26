import os
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from django.db.models import Q
from vanilla import CreateView, DetailView, RedirectView
from django_tables2 import SingleTableView
from ..statistics.utils import Utils
from .forms import TrialForm
from .models import Trial, TrialData
from .tables import TrialTable, TrialDataTable


class TrialList(SingleTableView):
    model = Trial
    table_class = TrialTable
    table_pagination = {'per_page': 10}

    def get_table_data(self):
        data = Trial.objects.all()
        if self.request.GET.get('search'):
            value = self.request.GET.get('search')
            data = data.filter(Q(image__original_name__contains=value) | Q(participant__first_name__contains=value)
                               | Q(participant__last_name__contains=value) | Q(percentage_samples__contains=value))
        return data


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

        # Add in a QuerySet duration
        context['duration'] = context['object'].end_date - context['object'].start_date
        return context


class TrialDelete(RedirectView):
    model = Trial

    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse_lazy('trials:list')
        model = get_object_or_404(Trial, pk=kwargs['pk'])
        try:
            with transaction.atomic():
                # Delete eye data
                TrialData.objects.filter(trial=model.pk).delete()

                # Delete trial
                model.delete()

                # Delete file
                os.unlink(model.file.path)

                messages.success(self.request, 'Trial was deleted successfully')
        except IntegrityError:
            messages.error(self.request, 'The request was unsuccessful')

        return super(TrialDelete, self).get_redirect_url(*args, **kwargs)


class TrialDataList(SingleTableView):
    model = TrialData
    table_class = TrialDataTable
    table_pagination = {'per_page': 50}

    def get_table_data(self):
        pk = self.kwargs.get('pk')
        data = TrialData.objects.filter(trial=pk)
        if self.request.GET.get('search'):
            value = self.request.GET.get('search')
            data = data.filter(Q(avg_x=value) | Q(avg_y=value)
                               | Q(left_pupil_size=value) | Q(right_pupil_size=value))
        return data

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TrialDataList, self).get_context_data(**kwargs)

        # Add in a QuerySet data trial
        pk = self.kwargs.get('pk')

        data_trial = Utils().data_trial(pk)
        context['raw'] = data_trial['raw']
        context['pupil'] = data_trial['pupil']
        context['first_index_baseline'] = data_trial['first_index_baseline']
        context['last_index_baseline'] = data_trial['last_index_baseline']

        return context
