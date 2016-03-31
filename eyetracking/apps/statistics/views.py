from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django_tables2 import SingleTableView
from vanilla import TemplateView
from ..trials.models import Trial, TrialData, TrialFeatures
from ..participants.models import Participant
from .tables import StatisticsTable, TrialDataTable
from .utils import Utils

class StatisticList(SingleTableView):
    model = TrialFeatures
    template_name = 'statistics/statistic_list.html'
    table_class = StatisticsTable
    table_pagination = False

    def get_table_data(self):
        data = TrialFeatures.objects.filter(trial__percentage_samples__gte=79.99, trial__resolved=1).order_by('trial__participant__first_name')

        if self.request.GET.get('search'):
            value = self.request.GET.get('search')
            if value:
                data = data.filter(Q(trial__participant__first_name__contains=value) | Q(trial__participant__last_name__contains=value)
                                   | Q(trial__image__original_name__contains=value))

        level = 1
        if self.request.GET.get('level'):
            level = self.request.GET.get('level')

        data = data.filter(trial__level=level)

        return data

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StatisticList, self).get_context_data(**kwargs)

        search = ''
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
        context['search'] = search

        level = 1
        if self.request.GET.get('level'):
            level = self.request.GET.get('level')
        context['level'] = level

        context['totals'] = TrialFeatures().get_totals(level, '', search)

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
        context['first_index_solved'] = trial_data['first_index_solved']

        search = ''
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
        context['search'] = search

        return context


class ChartsLevels(TemplateView):
    template_name = 'statistics/statistic_charts_levels.html'

    def get_context_data(self, **kwargs):
        context = super(ChartsLevels, self).get_context_data(**kwargs)

        features = {1:'', 2:'', 3:''}
        for i in range(3):
            level = i+1
            features_level = TrialFeatures().get_totals(level, '', '')
            features[level]= features_level

        context['features'] = features

        context['participants'] = Participant.objects.all().order_by('first_name', 'last_name')

        return context


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


class ParticipantLevels(JSONResponseMixin, TemplateView):

    def get_context_data(self, **kwargs):

        features = {1:'', 2:'', 3:''}

        participant_id = ''

        if self.request.GET.get('participant'):
            participant_id = self.request.GET.get('participant')

        for i in range(3):
            level = i+1
            features_level = TrialFeatures().get_totals(level, participant_id, '')
            features[level] = features_level

        return features

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)