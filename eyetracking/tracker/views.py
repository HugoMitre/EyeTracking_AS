from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from tracker.forms import *
from pytribe import *
import time

# Create your views here.


def home(request):

    return render(request, 'home.html', {})


def create(request):

    if request.method == 'POST':
        form = TrackerForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Eye Tracker Settings Created')
            return HttpResponseRedirect(reverse('tracker:detail'))
    else:
        form = TrackerForm()

    return render(request, 'create.html', {'form': form})


def update(request):

    model = get_object_or_404(Tracker, pk=1)

    if request.method == 'POST':
        form = TrackerForm(data=request.POST, instance=model)

        if form.is_valid():
            form.save()
            messages.success(request, 'Eye Tracker Settings Updated')
            return HttpResponseRedirect(reverse('tracker:detail_tracker'))
    else:
        form = TrackerForm(None, instance=model)

    return render(request, 'update.html', {'form': form})


def detail(request):

    try:
        model = Tracker.objects.get(pk=1)
    except ObjectDoesNotExist:
        messages.warning(request, "Doesn't exist any eye tracker added.")
        return HttpResponseRedirect(reverse('tracker:create_tracker'))

    return render(request, 'detail.html', {'model': model})


def record(request):

    form = RecordForm()
    tracker_state = 1

    try:
        model = Tracker.objects.get(pk=1)
        eyetribe = EyeTribe(model.ip, model.port, True)
        time.sleep(.01)
        tracker_state = eyetribe._tracker.get_trackerstate()
        eyetribe.close()

        if request.method == 'POST':
            seconds = request.POST['time']

            eyetribe = EyeTribe(model.ip, model.port, False)
            eyetribe.start_recording()
            time.sleep(int(seconds))
            eyetribe.stop_recording()
            eyetribe.close()
            messages.success(request, 'Completed')

            return HttpResponseRedirect(reverse('tracker:record_tracker'))

    except Exception as e:
        #messages.error(request, str(e))
        pass

    return render(request, 'record.html', {'form': form, 'tracker_state': tracker_state})
