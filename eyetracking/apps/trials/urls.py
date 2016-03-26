from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.TrialList.as_view(), name='list'),
    url(r'^upload/$', views.TrialCreate.as_view(), name='upload'),
    url(r'^(?P<pk>\d+)/$', views.TrialDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update', views.TrialUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/data$', views.TrialDataList.as_view(), name='data'),
    url(r'^(?P<pk>\d+)/delete/$', views.TrialDelete.as_view(), name='delete'),
]
