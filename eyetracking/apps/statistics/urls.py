from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.StatisticList.as_view(), name='list'),
    url(r'^feature$', views.StatisticFeature.as_view(), name='feature'),
]
