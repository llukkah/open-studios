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
        if coming_exhibit() != None:
            next_exhibit = coming_exhibit()
        else:
            reset()
    
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
        exhibits = Exhibit.objects.exclude(featured=True).exclude(revealed = True)
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




# ---------------------------------------------------------------------------------------------------
# ----------------------------------------- Create and Edit -----------------------------------------
# ---------------------------------------------------------------------------------------------------


def create_image(request):
    action = 'create'
    if request.method == 'GET':
        formset = ImageForm()
        return render(request, 'cne_image.html', context = {'form' : formset, 'action' : action})
    
    if request.method == 'POST':
        # items = []
        # cleaned = []
        # tmp = {}
        formset = ImageForm(request.POST)
        if formset.is_valid():
            # for form in formset:
            #     cleaned.append(form.cleaned_data)
                
            # for itm in cleaned:
            #     for key in itm:
            #         if 'featured' in key:
            #             tmp[key] = bool(itm[key])
            #         else:
            #             tmp[key] = itm[key]
            #     items.append(tmp)
            # print()
            # print(items)
            # print()
            # for item in items:
            #     print(item)
            #     if item['name'] == '':
            #         items.remove(item)
            #     Image.objects.create(name = item['name'], url = item['url'], featured = item['featured'])
            name = formset.cleaned_data['name']
            url = formset.cleaned_data['url']
            featured = formset.cleaned_data['featured']
            Image.objects.create(name = name, url = url, featured = featured)
            
            return HttpResponseRedirect(reverse('create'))
        else:
            return render(request, 'cne_image.html', context = {'form' : formset, 'action' : action})


def edit_image(request, exhibit_id):
    action = 'edit'
    if request.method == 'GET':
        image = Image.objects.get(exhibit_id)
        form = ImageForm(initial = {
            'name' : image.name, 
            'url' : image.url, 
            'featured' : image.featured})
        
        return render(request, 'edit_image.html', context = {'iform' : form, 'action' : action})
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

def create_tag(request):
    action = 'create'
    if request.method == 'GET':
        form = TagForm()
        return render(request, 'tag.html', context = {'form' : form, 'action' : action})
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Tag.objects.create(name = name)
            return HttpResponseRedirect(reverse('create'))
        else:
            return render(request, 'tag.html', context = {'form' : form, 'action' : action})

def edit_tag(request, tag_id):
    action = 'edit'
    if request.method == 'GET':
        tag = Tag.objects.get(pk = tag_id)
        form = TagFormSet(initial = {'name' : tag.name})
        return render(request, 'edit_tag.html', context = {'form' : form, 'action' : action, 'tag' : tag})
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
            return HttpResponseRedirect(reverse('create'))
        else:
            return render(request, 'tag.html', context = {'form' : form, 'action' : action})

def create_exhibit(request):
    action = 'create'
    if request.method == 'GET':
        form = ExhibitForm()
        # image_formset = ImageFormSet()
        # tag_formset = TagFormSet()
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
            # 'image_formset' : image_formset, 
            # 'tag_formset' : tag_formset
            } 
        
        if len(images) > 0:
            context['images'] = images
        
        return render(request, 'exhibit.html', context )
    
    if request.method == 'POST':
        form = ExhibitForm(request.POST)
        # image_formset = ImageFormSet(request.POST)
        # tag_formset = TagFormSet(request.POST)
        tags = images = []
        # pics = request.tag_formset.getlist('images')
        # if image_formset.is_valid():
        #     for form in image_formset:
        #         itm = {'name' : form.cleaned_data['name'],
        #                 'url' : form.cleaned_data['url'], 
        #                 'featured' : form.cleaned_data['featured']}
        #         images.append(Image.ojects.create(name = itm.name, url = itm.url, featured = itm.featured)) 
        #     form.update(images = images)
        
        # if tag_formset.is_valid():
        #     for form in tag_formset:
        #         tag = form.clean_data['name']
        #         tag.save()
        #         tags.append(tag)
        #     form.update(tags)
        
        if form.is_valid():
            artist_name = form.cleaned_data['artist_name']
            email = form.cleaned_data['email']
            bio = form.cleaned_data['bio']
            website = form.cleaned_data['website']
            exhibit_name = form.cleaned_data['exhibit_name']
            description = form.cleaned_data['description']
            tags = form.cleaned_data['tags']
            images = form.cleaned_data['images']
            # timestamp = datetime.date.today()

            Exhibit.objects.create(
                artist_name = artist_name,
                email = email, 
                bio = bio,
                website = website,
                exhibit_name = exhibit_name,
                description = description)
                # timestamp = datetime.date.today()

            exhibit = Exhibit.objects.all().order_by('-exhibit_id')

            exhibit[0].tags.set(tags)
            exhibit[0].images.set(images)
            return HttpResponseRedirect(reverse('upcoming'))
        else:
            return render(request, 'exhibit.html', context = {'form' : form, 'tags' : tags, 'images' : images} )


def edit_exhibit(request, exhibit_id):
    action = 'edit'
    if request.method == 'GET':
        
        exhibit = Exhibit.objects.get(pk = exhibit_id)
        
        tags = []
        for tag in exhibit.tags.all():
            tags.append(tag.tag_id)
            
        art = []
        for image in exhibit.pics.all().order_by('image_id'):
            if image.featured:
                art.append(image.image_id)
                
        
        form = ExhibitForm(initial = {
            'artist_name' : exhibit.artist_name, 
            'email' : exhibit.email, 
            'bio' : exhibit.bio,  
            'website' : exhibit.website, 
            'exhibit_name' : exhibit.exhibit_name,
            'description' : exhibit.description, 
            'images' : art, 
            'tags' : tags})
        
        return render(request, 'exhibit.html', context = {'form' : form, 'action' : action})
    
    if request.method == 'POST':
        form = ExhibitForm(request.POST)
        exhibit = Exhibit.objects.filter(pk = exhibit_id)
        
        tags = []
        for tag in exhibit.tags.all():
            tags.append(tag.tag_id)
            
        art = []
        for image in exhibit.pics.all().order_by('image_id'):
            if image.featured:
                art.append(image.image_id)
        if form.is_valid():
            if 'save' in request.POST:
                artist_name = form.cleaned_data['artist_name']
                email = form.cleaned_data['email']
                bio = form.cleaned_data['bio']
                website = form.cleaned_data['website']
                exhibit_name = form.cleaned_data['exhibit_name']
                description = form.cleaned_data['description']
                tags = form.cleaned_data['tags']
                images = form.cleaned_data['images']
                # timestamp = datetime.date.today()
                
                exhibit.update(
                    artist_name = artist_name,
                    email = email, bio = bio,
                    website = website,
                    exhibit_name = exhibit_name,
                    description = description)
                    # removed timestamp = timestamp  
                exhibit[0].tags.set(tags)
                exhibit[0].images.set(images)
            elif 'delete' in request.POST:
                exhibit.delete()
            return HttpResponseRedirect(reverse('upcoming'))
        else:
            return render(request, 'exhibit.html', context = {'form' : form} )


# ---------------------------------------------------------------------------------------------------
# ------------------------------------------------- Logic -------------------------------------------
# ---------------------------------------------------------------------------------------------------

def get_featured():
    for exhibit in Exhibit.objects.all().order_by('timestamp'):
        if exhibit.featured:
            featured = exhibit
    return featured

def coming_exhibit():
    # exhibits = []
    if len(Exhibit.objects.all()) > 1:
        for exhibit in Exhibit.objects.all().order_by('-timestamp'):
            if not exhibit.revealed and not exhibit.featured:
                next_exhibit = exhibit            
        return next_exhibit

    else:
        next_exhibit = None
        return next_exhibit

            # exhibits.append({
            #     'name' : e.exhibit_name, 
            #     'created' : e.timestamp, 
            #     'id' : e.exhibit_id,
            #     'featured' : e.featured,
            #     'featured_date' : e.featured_date,
            #     'revealed' : e.revealed})
    # return exhibits[0]


def reset():
    cnt = 0
    for exhibit in Exhibit.objects.all().order_by('exhibit_id'):
        if cnt == 0:
            exhibit.add_featured()
        else:
            exhibit.remove_featured()
            exhibit.revealed = False
        cnt += 1


def register(request):
    pass

def login(request):
    pass

def rotation(request):
    pass