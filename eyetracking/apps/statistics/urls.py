from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.StatisticList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/data$', views.TrialDataList.as_view(), name='data'),
]
