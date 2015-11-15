from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ParticipantList.as_view(), name='list'),
    url(r'^new/$', views.ParticipantCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.ParticipantDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.ParticipantUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.ParticipantDelete.as_view(), name='delete'),
]
