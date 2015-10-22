from django.conf.urls import url
from django.views.generic import DetailView
from images import views
from images.models import Image


urlpatterns = [
    url(r'^$', views.index, name='index_images'),
    url(r'^add$', views.add, name='add_images'),
    url(r'^(?P<pk>\d+)/update$', views.update, name='update_image'),
    url(r'^(?P<pk>\d+)/detail$', DetailView.as_view(model=Image, template_name="images/detail.html"), name="detail_image"),
    url(r'^(?P<pk>\d+)/delete$', views.delete, name='delete_image'),
    url(r'^upload$', views.upload, name='upload_image'),
    url(r'^(?P<pk>\d+)/upload_delete$', views.upload_delete, name='upload_delete'),
]
