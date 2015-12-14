from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.AOIList.as_view(), name='list'),
    url(r'^new/$', views.AOICreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/update/$', views.AOIUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.AOIDelete.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/change_name/$', views.AOIChangeName.as_view(), name='change_name'),
    url(r'^image/$', views.AOIGetInfoImage.as_view(), name='image'),
    url(r'^shapes/$', views.AOIGetShapes.as_view(), name='shapes'),
]
