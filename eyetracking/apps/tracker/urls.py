from django.conf.urls import url
from apps.tracker import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create$', views.create, name='create_tracker'),
    url(r'^update$', views.update, name='update_tracker'),
    url(r'^detail$', views.detail, name='detail_tracker'),
    url(r'^record$', views.record, name='record_tracker'),
]
