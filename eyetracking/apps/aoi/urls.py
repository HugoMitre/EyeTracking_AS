from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.AOIList.as_view(), name='list'),
    url(r'^new/$', views.AOICreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.AOIDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.AOIUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.AOIDelete.as_view(), name='delete'),
    url(r'^image/$', views.AOIGetUrlImage.as_view(), name='image'),
]
