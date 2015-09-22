from django.conf.urls import url
from tracker import views


urlpatterns = [
        url(r'^$', views.home, name='home'),
        url(r'^create$', views.create, name='create_tracker'),
        url(r'^(?P<pk>\d+)/update$', views.create, name='update_tracker'),
        url(r'^detail', views.detail, name='detail_tracker'),
    ]
