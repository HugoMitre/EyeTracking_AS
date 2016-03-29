from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.StatisticList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/data$', views.TrialDataList.as_view(), name='data'),
    url(r'^charts_levels$', views.ChartsLevels.as_view(), name='charts_levels'),
    url(r'^participant_levels$', views.ParticipantLevels.as_view(), name='participant_levels'),
]
