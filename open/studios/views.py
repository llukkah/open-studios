from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .forms import *
import datetime

# Create your views here.
def main(request):
    featured = ''
    exhibits = images = carousel = []
    exhibits = Exhibit.objects.all().order_by('-exhibit_id')
    for exhibit in exhibits:
        if exhibit.is_featured():
            featured = exhibit
    tags = []
    if len(exhibits) > 1:
        exhibits['upcoming'] = Rotation.upcoming()
    
    images = Image.objects.all().order_by('-exhibit')
    for image in images:
        print(image)
        if image.exhibit == featured.exhibit_name:
            carousel.append(image)
    print(carousel)
    
    return render(request, 'main.html', context = {'featured' : featured, 'images' : carousel, 'exhibits' : exhibits})


def about(request):
    return render(request, 'about.html')

def create_image(request):
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

def edit_image(request, exhibit_id):
    if request.method == 'GET':
        image = Image.objects.get(exhibit_id)
        form = ImageForm(initial = {'name' : image.name, 'url' : image.url, 'exhibit' : image.exhibit})
        return render(request, 'image.html', context = {'iform' : form})
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            Image.objects.update_or_create(name = name, url = url)
            return HttpResponseRedirect(reverse('add_image'))

def create_tag(request):
    if request.method == 'GET':
        form = TagForm()
        return render(request, 'tag.html', context = {'form' : form})
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Tag.objects.create(name = name)
            return HttpResponseRedirect(reverse('tag'))

def edit_tag(request, tag_id):
    print(request.get_full_url())
    if request.method == 'GET':
        tag = Tag.objects.get(pk = tag_id)
        form = TagForm(initial = {'name' : tag.name})
        return render(request, 'edit_tag.html', context = {'form' : form})
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            if 'save' in request.POST:
                name = form.cleaned_data['name']
                tags = Tag.objects.filter(pk = tag_id)
                tags.update(name = name)
                tags.save()
            elif 'delete' in request.POST:
                Tag.objects.filter(pk = tag_id).delete()
        return HttpResponseRedirect(reverse('upcoming'))

def create_exhibit(request):
    if request.method == 'GET':
        form = ExhibitForm()
        tags = []
        for tag in Tag.objects.all():
            tags.append(tag.tag_id)
        art = []
        for image in Image.objects.all():
            art.append(image.id)
        print(art)
        return render(request, 'create_exhibit.html', context = {'form' : form})
    
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

            Exhibit.objects.create(
            artist_name = artist_name,
            email = email, 
            bio = bio,
            website = website,
            exhibit_name = exhibit_name,
            description = description,
            timestamp = timestamp)

            exhibit = Exhibit.objects.all().order_by('-exhibit_id')

            exhibit[0].tags.set(tags)
            exhibit[0].images.set(images)
        return HttpResponseRedirect(reverse('home'))


def edit_exhibit(request, exhibit_id):
    if request.method == 'GET':
        exhibit = Exhibit.objects.get(pk = exhibit_id)
        tags = []
        for tag in exhibit.tags.all():
            tags.append(tag.tag_id)
        art = []
        for image in exhibit.images.objects.all():
            art.append(image.id)
        print(art)
        form = ExhibitForm(initial = {'artist_name' : exhibit.artist_name, 'email' : exhibit.email, 'bio' : exhibit.bio, 'website' : exhibit.website, 'description' : exhibit.description, 'images' : art, 'tags' : tags})
        return render(request, 'edit_exhibit.html', context = {'form' : form})
    
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
            
            Exhibit.objects.create(
                artist_name = artist_name,
                email = email, bio = bio,
                website = website,
                exhibit_name = exhibit_name,
                description = description,
                timestamp = timestamp)
            
            exhibit = Exhibit.objects.all().order_by('-exhibit_id')
            
            exhibit[0].tags.set(tags)
            exhibit[0].images.set(images)
        
        return HttpResponseRedirect(reverse('upcoming'))


def featured(request):
    if request.method == 'GET':
        form = CommentForm()
        exhibit = Exhibit.objects.filter(featured=True)
        return render(request=request, template_name='featured.html', context={ 'exhibit': exhibit, 'form':form })
    if request.method == 'POST':    
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']        
        return render(request=request, template_name='featured.html')


def upcoming(request):
    exhibits = Exhibit.objects.exclude( revealed=True)
    art = [{'url' : i.url, 'name' : i.name, 'id' : i.id} for i in Image.objects.all().order_by('-exhibit')]
    return render(request = request, template_name = 'upcoming.html', context = {'exhibits' : exhibits, 'images' : art})


def register(request):
    pass


def login(request):
    pass

def rotation(request):
    pass