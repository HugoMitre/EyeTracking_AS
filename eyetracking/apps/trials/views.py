import os
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from django.db.models import Q
from vanilla import CreateView, DetailView, UpdateView, RedirectView
from django_tables2 import SingleTableView
from .forms import TrialUploadForm, TrialUpdateForm
from .models import Trial, TrialData
from .tables import TrialTable


class TrialList(SingleTableView):
    model = Trial
    table_class = TrialTable
    table_pagination = {'per_page': 5}

    def get_table_data(self):
        data = Trial.objects.all()
        if self.request.GET.get('search'):
            value = self.request.GET.get('search')
            if value:
                data = data.filter(Q(image__original_name__contains=value) | Q(participant__first_name__contains=value)
                                   | Q(participant__last_name__contains=value) | Q(percentage_samples__contains=value))
        return data

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TrialList, self).get_context_data(**kwargs)

        search = ''
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
        context['search'] = search

        trial = Trial()
        total = trial.get_total()
        if total > 0:
            percentage_valid = trial.get_percentage_valid(total)
            context['percentage_valid'] = percentage_valid

            solved = trial.get_solved()
            context['solved'] = solved
            context['unsolved'] = total - solved

        return context


class TrialCreate(SuccessMessageMixin, CreateView):
    model = Trial
    form_class = TrialUploadForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('trials:list')
    success_message = "Trial was created successfully"
    error_message = "Invalid file"

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)

        if (self.object.id is None):
            messages.error(self.request, self.error_message)
        else:
            messages.success(self.request, success_message)
        return response


class TrialDetail(DetailView):
    model = Trial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TrialDetail, self).get_context_data(**kwargs)

        # Add in a QuerySet duration
        context['duration'] = context['object'].end_date - context['object'].start_date
        return context


class TrialUpdate(SuccessMessageMixin, UpdateView):
    model = Trial
    form_class = TrialUpdateForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('trials:list')
    success_message = "Trial was updated successfully"


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