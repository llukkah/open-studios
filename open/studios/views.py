from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .forms import *
import datetime

# Create your views here.
def main(request):
    featured = ''
    exhibits = images = []
    exhibits = Exhibit.objects.all().order_by('-exhibit_id')
    for exhibit in exhibits:
        if exhibit.is_featured():
            featured = exhibit
    print(featured)
    tags = []
    for tag in Tag.objects.all():
            tags.append(tag.tag_id)
    
    if len(exhibits) > 1:
        exhibits['upcoming'] = Rotation.upcoming()
    
    for image in featured.pics.all().order_by('-image_id'):
        if image.is_featured():
            images.append({
                'id' : image.image_id, 
                'url' : image.url,
                'name' : image.name})
    
    return render(request, 'main.html', context = {
        'featured' : featured, 
        'images' : images
        })


def about(request):
    return render(request, 'about.html')


def create_image(request):
    if request.method == 'GET':
        form = ImageForm()
        return render(request, 'image.html', context = {'form' : form})
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            Image.objects.update_or_create(name = name, url = url)
            return HttpResponseRedirect(reverse('add_image'))

def edit_image(request, exhibit_id):
    if request.method == 'GET':
        image = Image.objects.get(exhibit_id)
        form = ImageForm(initial = {
            'name' : image.name, 
            'url' : image.url, 
            'exhibit' : image.exhibit})
        return render(request, 'edit_image.html', context = {'iform' : form})
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
        image_formset = ImageFormSet()
        tag_formset = TagFormSet()
        
        tags = []
        for tag in Tag.objects.all():
            tags.append(tag.tag_id)
        
        return render(request, 'create_exhibit.html', context = {
            'form' : form, 
            'image_formset' : image_formset, 
            'tag_formset' : tag_formset, 
            'tags' : tags})
    
    if request.method == 'POST':
        form = ExhibitForm(request.POST)
        image_formset = ImageFormSet(request.POST)
        tag_formset = TagFormSet(request.POST)
        tags = images = []
        # pics = request.tag_formset.getlist('images')
        if image_formset.is_valid():
            for form in image_formset:
                itm = {'name' : form.cleaned_data['name'],
                        'url' : form.cleaned_data['url'], 
                        'featured' : form.cleaned_data['featured']}
                images.append(Image.ojects.create(name = itm.name, url = itm.url, featured = itm.featured)) 
            form.update(images = images)
        
        if tag_formset.is_valid():
            for form in tag_formset:
                tag = form.clean_data['name']
                tag.save()
                tags.append(tag)
            form.update(tags)
        
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
            if image.featured:
                print(image)
                art.append(image.image_id)
                
        
        form = ExhibitForm(initial = {
            'artist_name' : exhibit.artist_name, 
            'email' : exhibit.email, 
            'bio' : exhibit.bio,  
            'website' : exhibit.website, 
            'description' : exhibit.description, 
            'images' : art, 
            'tags' : tags})
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
        formset = CommentFormSet()
        featured = Exhibit()
        for exhibit in Exhibit.objects.all().order_by('exhibit_id'):
            if exhibit.is_featured():
                featured = exhibit
        
        images = []
        for image in featured.pics.all().order_by('image_id'):
            images.append({
                'id' : image.image_id, 
                'url' : image.url,
                'name' : image.name})
        
        comments = [{'author' : c.author, 'comment' : c.comment} for c in featured.responses.all().order_by('created')]
        
        return render(
            request = request, 
            template_name = 'featured.html', 
            context = { 
                    'exhibit': featured,
                    'images' : images, 
                    'form':formset,
                    'comments' : comments})
    
    if request.method == 'POST':    
        formset = CommentFormSet(request.POST)
        if formset.is_valid():
            comment = formset.cleaned_data
            comment.save()        
        return render(request = request, template_name = 'featured.html')


def upcoming(request):
    exhibits = Exhibit.objects.exclude(featured=True).exclude(revealed = True)
    
    art = []
    for exhibit in exhibits:
        count = 0
        for i in exhibit.pics.all():
            if count < 3:
                art.append({
                        'url' : i.url, 
                        'name' : i.name, 
                        'id' : i.image_id,
                        'collection' : exhibit.exhibit_id})
            count += 1
    return render(request = request, template_name = 'upcoming.html', context = {
                        'exhibits' : exhibits, 
                        'images' : art })
''' ****** possible additions for comments on each image ******
    art = comments = []
    for exhibit in exhibits:
        for i in exhibit.pics.all().order_by('-image_id'):
            if i.featured:
                art.append({
                        'url' : i.url, 
                        'name' : i.name, 
                        'id' : i.image_id})
    return render(request = request, template_name = 'upcoming.html', context = {
                            'exhibits' : exhibits, 
                            'images' : art,
                            'comments' : comments})
'''

def show_image(request, name):
    if request.method == 'GET':
        image = Image()
        for pic in Image.objects.all().order_by('image_id'):
            if pic.name == name:
                image = pic
        
        return render(request, 'image.html', context = {'image' : image})


def register(request):
    pass


def login(request):
    pass

def rotation(request):
    pass