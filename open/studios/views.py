from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .forms import *

# Create your views here.
def home(request):
    return render(request, 'base.html')

def clean_n_add(request, form):
    if form.is_valid(form):
        pass

def create_exhibit(request):
    if request.method == 'GET':
        eform = ExhibitForm()
        iform = ImageForm()
        return render(request, 'create_exhibit.html', context = {'eform' : eform, 'iform' : iform})
    if request.method == 'POST':
        eform = ExhibitForm(request.POST)
        iform = ImageForm(request.POST)
        clean_n_add(iform)
        if eform.is_valid():
            artist_name = eform.cleaned_data['artist_name']
            email = eform.cleaned_data['email']
            bio = eform.cleaned_data['bio']
            website = eform.cleaned_data['website']
            exhibit_name = eform.cleaned_data['exhibit_name']
            description = eform.cleaned_data['description']
            tags = eform.cleaned_data['tags']
            images = eform.cleaned_data['images']
            timestamp = eform.cleaned_data['timestamp']
            Exhibit.objects.create(artist_name=artist_name,email=email,bio=bio, website=website, exhibit_name=exhibit_name, description=description, timestamp=timestamp)
            exhibit = Exhibit.objects.all().order_by('-id')
            exhibit[0].tags.set(tags)
            exhibit[0].images.set(images)
        return HttpResponseRedirect(reverse('home'))