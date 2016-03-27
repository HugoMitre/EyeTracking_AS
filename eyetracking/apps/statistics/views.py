from django.views.generic.base import TemplateResponseMixin
from vanilla import TemplateView
from ..trials.models import Trial
from .tables import StatisticsTable


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