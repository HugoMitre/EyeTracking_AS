from django.shortcuts import render

# Create your views here.
def home(request):

    return render(request, 'home.html', {})


def create(request):

    return render(request, 'create.html', {})


def update(request, pk):

    return render(request, 'update.html', {})


def detail(request):

    return render(request, 'detail.html', {})