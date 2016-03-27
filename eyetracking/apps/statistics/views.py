from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from vanilla import TemplateView
from django_tables2 import SingleTableView
from ..trials.models import Trial, TrialData
from .tables import StatisticsTable, TrialDataTable
from .utils import Utils

class StatisticList(TemplateResponseMixin, TemplateView):
    template_name = 'statistics/statistic_list.html'

    def get_name(self, item):
        return item['name']

    def get_errors(self, item):
        return item['errors']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StatisticList, self).get_context_data(**kwargs)

        trials = Trial.objects.filter(percentage_samples__gte=79.99, resolved=True)

        data =[]
        for trial in trials:
            data_trial = {'participant_name':trial.participant.first_name + ' ' + trial.participant.last_name,
                          'image_name':trial.image.original_name, 'duration':trial.end_date - trial.start_date,
                          'errors':2, 'actions':trial.pk}

            data.append(data_trial)

        if self.request.GET.get('sort'):
            sort_value = self.request.GET.get('sort')
            if sort_value == 'name':
                data = sorted(data, key=self.get_name)
            elif sort_value == 'errors':
                data = sorted(data, key=self.get_errors)

        context['table'] = StatisticsTable(data)

        return context


class TrialDataList(SingleTableView):
    model = TrialData
    template_name = 'statistics/statistic_trialdata_list.html'
    table_class = TrialDataTable
    table_pagination = {'per_page': 50}


    def get_table_data(self):
        pk = self.kwargs.get('pk')
        data = TrialData.objects.filter(trial=pk)
        if self.request.GET.get('search'):
            value = self.request.GET.get('search')
            if value:
                data = data.filter(Q(avg_x=value) | Q(avg_y=value)
                                   | Q(left_pupil_size=value) | Q(right_pupil_size=value))
        return data

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TrialDataList, self).get_context_data(**kwargs)

        # Add in a QuerySet data trial
        pk = self.kwargs.get('pk')

        model = get_object_or_404(Trial, pk=pk)
        context['participant_name'] = model.participant.first_name + ' ' + model.participant.last_name
        context['image_name'] = model.image.original_name
        context['duration'] = model.end_date - model.start_date

        data_trial = Utils().data_trial(pk)
        context['raw_pupil'] = data_trial['raw_pupil']
        context['smooth_pupil'] = data_trial['smooth_pupil']
        context['fixed_pupil_distance'] = data_trial['fixed_pupil_distance']
        context['raw_distance'] = data_trial['raw_distance']
        context['smooth_distance'] = data_trial['smooth_distance']
        context['first_index_baseline'] = data_trial['first_index_baseline']
        context['last_index_baseline'] = data_trial['last_index_baseline']

        search = ''
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
        context['search'] = search

        return context