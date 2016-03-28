from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_tables2 import SingleTableView
from ..trials.models import Trial, TrialData, TrialFeatures
from .tables import StatisticsTable, TrialDataTable
from .utils import Utils

class StatisticList(SingleTableView):
    model = TrialFeatures
    template_name = 'statistics/statistic_list.html'
    table_class = StatisticsTable
    table_pagination = False

    def get_table_data(self):
        data = TrialFeatures.objects.filter(trial__percentage_samples__gte=79.99, trial__resolved=1)
        if self.request.GET.get('search'):
            value = self.request.GET.get('search')
            if value:
                data = data.filter(Q(trial__participant__first_name=value) | Q(trial__participant__last_name=value)
                                   | Q(trial__image__original_name=value))
        return data

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StatisticList, self).get_context_data(**kwargs)

        search = ''
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
        context['search'] = search

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

        trial_data = Utils().get_signals(TrialData.objects.filter(trial=pk))
        context['raw_pupil'] = trial_data['raw_pupil']
        context['smooth_pupil'] = trial_data['smooth_pupil']
        context['fixed_pupil_distance'] = trial_data['fixed_pupil_distance']
        context['raw_distance'] = trial_data['raw_distance']
        context['smooth_distance'] = trial_data['smooth_distance']
        context['first_index_baseline'] = trial_data['first_index_baseline']
        context['last_index_baseline'] = trial_data['last_index_baseline']

        search = ''
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
        context['search'] = search

        return context