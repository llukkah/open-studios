from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .forms import *
import datetime

# Create your views here.
def home(request):
    return render(request, 'home.html')

def add_image(request):
    if request.method == 'GET':
        form = ImageForm()
        return render(request, 'image.html', context = {'iform' : form})
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            Image.objects.update_or_create(name = name,url = url)
            return HttpResponseRedirect(reverse('add_image'))

def create_exhibit(request):
    if request.method == 'GET':
        form = ExhibitForm()
        return render(request, 'create_exhibit.html', context = {'eform' : form})
    if request.method == 'POST':
        form = ExhibitForm(request.POST)
        if form.is_valid():
            artist_name = form.cleaned_data['artist_name']
            email = form.cleaned_data['email']
            bio = form.cleaned_data['bio']
            website = form.cleaned_data['website']
            exhibit_name = form.cleaned_data['exhibit_name']
            description = form.cleaned_data['description']
            tags = form.cleaned_data['tags']
            images = form.cleaned_data['images']
            timestamp = datetime.datetime.now()
            Exhibit.objects.create(artist_name = artist_name, email = email, bio = bio, website = website, exhibit_name = exhibit_name, description = description, timestamp = timestamp)
            exhibit = Exhibit.objects.all().order_by('-id')
            exhibit[0].tags.set(tags)
            exhibit[0].images.set(images)
        return HttpResponseRedirect(reverse('home'))