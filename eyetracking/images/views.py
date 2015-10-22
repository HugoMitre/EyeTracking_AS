from django.shortcuts import render
from django_tables2 import RequestConfig
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from images.models import Image, Photo
from images.tables import ImageTable
from images.forms import ImageForm
import os
from django.conf import settings
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse


def index(request):

    table = ImageTable(Image.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    return render(request, 'images/index.html', {'table': table})


def add(request):

    return render(request, 'images/add.html', {})


def update(request, pk):

    model = get_object_or_404(Image, pk=pk)

    if request.method == 'POST':
        form = ImageForm(data=request.POST, instance=model)

        if form.is_valid():
            form.save()
            messages.success(request, 'Image Updated')
            return HttpResponseRedirect(reverse('images:index_images'))
    else:
        form = ImageForm(None, instance=model)

    return render(request, 'images/update.html', {'form': form})


def delete(request, pk):

    model = get_object_or_404(Image, pk=pk)
    model.delete()
    messages.success(request, 'Image Deleted')

    return HttpResponse('OK')


@require_POST
def upload(request):

    image = upload_receive(request)
    size = image.size

    model = Photo(image=image, resized_image=image)
    basename = os.path.basename(model.image.path)
    model.original_name = os.path.basename(model.image.path)
    model.size = Photo.humansize(size)
    model.save()

    thumbnail_name = str(model.resized_image)

    file_dict = {
        'name': basename,
        'size': size,

        'url': settings.MEDIA_URL + thumbnail_name,
        'thumbnailUrl': settings.MEDIA_URL + thumbnail_name,

        'deleteUrl': reverse('images:upload_delete', kwargs={'pk': model.pk}),
        'deleteType': 'POST',
    }

    return UploadResponse(request, file_dict)


@require_POST
def upload_delete(request, pk):

    success = True
    try:
        model = Photo.objects.get(pk=pk)
        os.unlink(model.image.path)
        os.unlink(model.resized_image.path)
        model.delete()
    except Photo.DoesNotExist:
        success = False

    return JFUResponse(request, success)
