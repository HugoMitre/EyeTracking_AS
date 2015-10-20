from django.shortcuts import render
from django_tables2   import RequestConfig
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from images.models import Image
from images.tables import ImageTable
from images.forms import ImageForm


def index(request):

    table = ImageTable(Image.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    return render(request, 'images/index.html', {'table':table})


def add(request):

    if request.method == 'POST':
        form = ImageForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Images Added')
            return HttpResponseRedirect(reverse('images:index_images'))
    else:
        form = ImageForm()

    return render(request, 'images/add.html', {'form':form})


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

    return render(request, 'images/update.html', {'form':form})


def delete(request, pk):

    model = get_object_or_404(Image, pk=pk)
    model.delete()
    messages.success(request, 'Image Deleted')

    return HttpResponse('OK')
