from django.db.models.fields import NullBooleanField
from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.forms import formset_factory
from .models import *
from .forms import *
import datetime




# ---------------------------------------------------------------------------------------------------
# ----------------------------------------------- Display -------------------------------------------
# ---------------------------------------------------------------------------------------------------
def main(request):
    featured = next_exhibit = ''
    images = []
    
    featured = get_featured()
    next_exhibit = coming_exhibit()
    
    today = datetime.date.today()
    time_featured = today - featured.featured_date
    
    if (time_featured.days > 1):
        featured.remove_featured()
        featured.save()
        next_exhibit.add_featured()
        next_exhibit.save()
        featured = next_exhibit

        if coming_exhibit() == '':
            next_exhibit = reset()

        else:
            next_exhibit = coming_exhibit()
    
    for image in featured.pics.all().order_by('-image_id'):
        if image.featured:
            images.append({
                'id' : image.image_id, 
                'url' : image.url,
                'name' : image.name
            })

    return render(request, 'main.html', context = {
                                            'featured' : featured,
                                            'next' : next_exhibit,
                                            'images' : images
                                        })


def show_image(request, name):
    if request.method == 'GET':
        image = Image()
        
        for pic in Image.objects.all().order_by('image_id'):
            if pic.name == name:
                image = pic
        
        return render(request, 'image.html', context = {'image' : image})


def featured(request):
    if request.method == 'GET':
        form = CommentForm()
        
        # featured = Exhibit()
        for exhibit in Exhibit.objects.all().order_by('exhibit_id'):
            if exhibit.featured:
                featured = exhibit
        
        images = []
        for image in featured.pics.all().order_by('image_id'):
            images.append({
                'id' : image.image_id, 
                'url' : image.url,
                'name' : image.name})
        
        comments = []
        if len(featured.responses.all()) > 0:
            for c in featured.responses.all().order_by('created'):
                comments.append({
                    'author' : c.author, 
                    'comment' : c.comment})
        
        return render(request = request, template_name = 'featured.html', context = { 
                    'exhibit': featured,
                    'images' : images, 
                    'form': form,
                    'comments' : comments})
    
    if request.method == 'POST':    
        form = CommentForm(data = request.POST)
        featured = Exhibit()
        for exhibit in Exhibit.objects.all().order_by('exhibit_id'):
            if exhibit.featured:
                featured = exhibit

        if form.is_valid():
            comment = form.cleaned_data['comment']
            author = form.cleaned_data['author']
            created = datetime.date.today()
            Comment.objects.create(
                                comment = comment, 
                                created = created, 
                                author = author, 
                                exhibit = featured)
            return HttpResponseRedirect(reverse('featured'))


def upcoming(request):
    if request.method == 'GET':
        exhibits = Exhibit.objects.exclude(featured = True).exclude(revealed = True)
        
        art = []
        for exhibit in exhibits:
            for i in exhibit.pics.all():
                if i.featured:
                    art.append({
                            'url' : i.url, 
                            'name' : i.name, 
                            'id' : i.image_id,
                            'collection' : exhibit.exhibit_id})
        
        return render(request = request, template_name = 'upcoming.html', context = {'exhibits' : exhibits, 'images' : art})


def about(request):
    profiles = [{
        'name' : 'Llukkah Delos Reyes', 
            'image' : '/static/media/images/llukkah.jpg', 
            'git' : 'https://www.github.com/llukkah',
            'linkedin' : 'https://www.linkedin.com/in/llukkahrey?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BPVPIS6RuS1mFA2Oz%2BiCvTA%3D%3D'
        }, 
        {'name' : 'Chris Linton',
            'image' : '/static/media/images/chris.jpg', 
            'git' : 'https://github.com/Kwyjib0',
            'linkedin' : 'https://www.linkedin.com/in/christopher-linton1?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3B90XwWnipSSGg%2Bj1Y%2BC%2BfEw%3D%3D'
        }, 
        {'name' : 'Lee Harvey',
            'image' : '/static/media/images/lee.jpg', 
            'git' : 'https://github.com/VirtDev337', 
            'linkedin' : 'https://www.linkedin.com/in/lee-harvey-jr?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BIvwSNWutSqaVtbFzP0%2BtHg%3D%3D'
        }, 
        {'name' : 'Jason Rolle',
            'image' : '/static/media/images/jason.jpg',
            'git' : 'https://github.com/JasonRolle1990',
            'linkedin' : 'https://www.linkedin.com/in/jasonrolle1990?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3Bculc7Op7S3esL9F80ZfMhw%3D%3D'
        }]

    links = [{'name': 'Facebook', 'icon': '/static/media/images/facebook.png', 'site': 'https://www.facebook.com'}, {'name': 'Instagram', 'icon': '/static/media/images/instagram.png', 'site': 'https://www.instagram.com/'}, {'name': 'Twitter', 'icon': '/static/media/images/twitter.png', 'site': 'https://twitter.com/'}
    ]
    return render(request, 'about.html', {'profiles' : profiles, 'links': links})




# ===================================================================================================
# ----------------------------------------- Create and Edit -----------------------------------------
# ===================================================================================================


# ---------------------------------------------- Images ---------------------------------------------
path = ''

# Create page
def create_image(request):
    action = 'create'
    if request.method == 'GET':
        form = ImageForm()
        return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})
    
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            featured = form.cleaned_data['featured']
            
            Image.objects.create(name = name, url = url, featured = featured)
            
            return HttpResponseRedirect(reverse(action))
        else:
            return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})


def create_edit_image(request, image_id):
    action = 'edit'
    if request.method == 'GET':
        image = Image.objects.get(image_id)
        form = ImageForm(data = {
            'name' : image.name, 
            'url' : image.url, 
            'featured' : image.featured})
        
        return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})
    
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            featured = form.cleaned_data['featured']
            Image.objects.update_or_create(name = name, url = url, featured = featured)
            return HttpResponseRedirect(reverse('create'))
        else:
            return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})


# Upcoming/edit page
def upcoming_create_image(request):
    action = 'upcoming'
    global path
    e_id = int(path.split("/")[-1])
    
    if request.method == 'GET':
        form = ImageForm()
        return render(request, 'cne_image.html', context = {'form' : form, 'action' : action, 'route' : path})
    
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            featured = form.cleaned_data['featured']
            
            Image.objects.create(name = name, url = url, featured = featured)
            
            return HttpResponseRedirect(reverse('edit', kwargs={'exhibit_id' : e_id}))
        else:
            return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})


def upcoming_edit_image(request, image_id):
    action = 'change'
    global path
    e_id = int(path.split("/")[-1])
    
    if request.method == 'GET':
        image = Image.objects.get(image_id)
        form = ImageForm(initial = {
            'name' : image.name, 
            'url' : image.url, 
            'featured' : image.featured,
            'route' : path})
        
        return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})

    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            featured = form.cleaned_data['featured']
            Image.objects.update_or_create(name = name, url = url, featured = featured)
            return HttpResponseRedirect(reverse('edit', kwargs={'exhibit_id' : e_id}))
        else:
            return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})


# --------------------------------------------- Exhibits --------------------------------------------


def create_exhibit(request):
    action = 'create'
    if request.method == 'GET':
        form = ExhibitForm()
        images = []
        for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
            images.append(image)
        
        tags = []
        for tag in Tag.objects.all():
            tags.append(tag.tag_id)
        
        context = {
            'form' : form, 
            'action' : action,
            'tags' : tags,
            'uri' : request.path,
            } 
        
        if len(images) > 0:
            context['images'] = images
        
        return render(request, 'exhibit.html', context )
    
    if request.method == 'POST':
        form = ExhibitForm(request.POST)
        tags = images = []
        images = []
        for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
            images.append(image)
        
        if form.is_valid():
            artist_name = form.cleaned_data['artist_name']
            email = form.cleaned_data['email']
            bio = form.cleaned_data['bio']
            website = form.cleaned_data['website']
            exhibit_name = form.cleaned_data['exhibit_name']
            description = form.cleaned_data['description']
            tags = form.cleaned_data['tags']
            
            Exhibit.objects.create(
                artist_name = artist_name,
                email = email, 
                bio = bio,
                website = website,
                exhibit_name = exhibit_name,
                description = description)
            
            exhibit = Exhibit.objects.all().order_by('-exhibit_id')
            
            exhibit[0].tags.set(tags)
            
            for image in images:
                exhibit[0].pics.add(image)
            
            return HttpResponseRedirect(reverse('upcoming'))
        else:
            return render(request, 'exhibit.html', context = {'form' : form, 'tags' : tags, 'images' : images} )


def edit_exhibit(request, exhibit_id):
    action = 'edit'
    global path
    path = request.get_full_path()
    
    if request.method == 'GET':
        
        exhibit = Exhibit.objects.get(pk = exhibit_id)
        
        tags = []
        for tag in exhibit.tags.all():
            tags.append(tag.tag_id)
        
        images = []
        for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
            images.append(image)
        
        form = ExhibitForm(initial = {
            'artist_name' : exhibit.artist_name, 
            'email' : exhibit.email, 
            'bio' : exhibit.bio,  
            'website' : exhibit.website, 
            'exhibit_name' : exhibit.exhibit_name,
            'description' : exhibit.description, 
            })
        
        return render(request, 'exhibit.html', context = {'form' : form, 'exhibit' : exhibit, 'action' : action, 'images' : images, 'route' : path})
    
    if request.method == 'POST':
        form = ExhibitForm(request.POST)
        
        if form.is_valid():
            if 'save' in request.POST:
                artist_name = form.cleaned_data['artist_name']
                email = form.cleaned_data['email']
                bio = form.cleaned_data['bio']
                website = form.cleaned_data['website']
                exhibit_name = form.cleaned_data['exhibit_name']
                description = form.cleaned_data['description']
                tags = form.cleaned_data['tags']
                
                exhibit = Exhibit.objects.filter(pk = exhibit_id)
                
                exhibit.update(
                    artist_name = artist_name,
                    email = email, 
                    bio = bio,
                    website = website,
                    exhibit_name = exhibit_name,
                    description = description)
                
                art = []
                for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
                    if image.featured:
                        art.append(image)
                
                exhibit = Exhibit.objects.get(pk = exhibit_id)
                
                exhibit.tags.set(tags)
                
                for image in art:
                    exhibit.pics.update_or_create(image)
                
            elif 'delete' in request.POST:
                exhibit = Exhibit.objects.get(pk = exhibit_id)
                
                for image in exhibit.pics.all():
                    image.delete()
                
                for cmnt in exhibit.responses.all():
                    cmnt.delete()
                
                exhibit.delete()
            path = ''
            return HttpResponseRedirect(reverse('upcoming'))
        else:
            exhibit = Exhibit.objects.get(pk = exhibit_id)
        
            tags = []
            for tag in exhibit.tags.all():
                tags.append(tag.tag_id)
            
            images = []
            for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
                images.append(image)
            
            return render(request, 'exhibit.html', context = {'form' : form, 'exhibit' : exhibit, 'images' : images, 'route' : path} )


# ===================================================================================================
# ------------------------------------------------- Logic -------------------------------------------
# ===================================================================================================


def get_featured():
    for exhibit in Exhibit.objects.all().order_by('-timestamp'):
        if exhibit.featured:
            featured = exhibit
    return featured


def coming_exhibit():

    if len(Exhibit.objects.filter(featured=False, revealed=False)) > 0:
        next_exhibit = Exhibit.objects.filter(featured=False, revealed=False).first()

    else:
        next_exhibit = ''

    return next_exhibit


def reset():
    exhibit = Exhibit.objects.all().order_by('featured_date').filter(featured = False, revealed = True).first()
    exhibit.revealed = False
    exhibit.save()

    return exhibit


# ===================================================================================================
# ------------------------------------------------- Users -------------------------------------------
# ===================================================================================================


def register(request):
    pass


def login(request):
    pass