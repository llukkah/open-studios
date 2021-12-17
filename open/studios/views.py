from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.forms import formset_factory
from .models import *
from .forms import *
import datetime

# Create your views here.
def main(request):
    featured = next_exhibit = ''
    images = []
    for exhibit in Exhibit.objects.all().order_by('timestamp'):
        if exhibit.is_featured():
            featured = exhibit
        if len(Exhibit.objects.all()) > 1:
            if not exhibit.revealed and not exhibit.is_featured():
                next_exhibit = exhibit
    
    for image in featured.pics.all().order_by('-image_id'):
        if image.is_featured():
            images.append({'id' : image.image_id, 
                            'url' : image.url,
                            'name' : image.name})
    
    return render(request, 'main.html', context = {'featured' : featured,
                                                    'next' : next_exhibit,
                                                    'images' : images})


def about(request):
    profiles = [{'name' : 'Llukkah', 
                    'image' : 'llukkah.jpeg', 
                    'git' : 'https://www.github.com/llukkah',
                    'linkedin' : 'https://www.linkedin.com/in/llukkahrey?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BPVPIS6RuS1mFA2Oz%2BiCvTA%3D%3D'}, 
                {'name' : 'Christopher',
                    'image' : 'chris.jpeg', 
                    'git' : 'https://github.com/Kwyjib0',
                    'linkedin' : 'https://www.linkedin.com/in/christopher-linton1?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3B90XwWnipSSGg%2Bj1Y%2BC%2BfEw%3D%3D'}, 
                {'name' : 'Lee',
                    'image' : 'lee.jpeg', 
                    'git' : 'https://github.com/VirtDev337', 
                    'linkedin' : 'https://www.linkedin.com/in/lee-harvey-jr?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BIvwSNWutSqaVtbFzP0%2BtHg%3D%3D'}, 
                {'name' : 'Jason',
                    'image' : 'jason.jpeg',
                    'git' : 'https://github.com/JasonRolle1990',
                    'linkedin' : 'https://www.linkedin.com/in/jasonrolle1990?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3Bculc7Op7S3esL9F80ZfMhw%3D%3D'}]
    return render(request, 'about.html', {'profiles': profiles})


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
            return HttpResponseRedirect(reverse('create'))

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
            return HttpResponseRedirect(reverse('create'))

def create_tag(request):
    if request.method == 'GET':
        form = TagForm()
        return render(request, 'tag.html', context = {'form' : form})
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Tag.objects.create(name = name)
            return HttpResponseRedirect(reverse('create'))

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
        return HttpResponseRedirect(reverse('create'))

def create_exhibit(request):
    action = 'create'
    if request.method == 'GET':
        form = ExhibitForm()
        image_formset = ImageFormSet()
        tag_formset = TagFormSet()
        
        tags = []
        for tag in Tag.objects.all():
            tags.append(tag.tag_id)
        
        return render(request, 'exhibit.html', context = {
            'form' : form, 
            'action' : action,
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
            'description' : exhibit.description, 
            'images' : art, 
            'tags' : tags})
        
        return render(request, 'exhibit.html', context = {'form' : form, 'action' : action})
    
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

# def edit(request, post_id):
#     if request.method == 'GET':
#         # get Post object by its post_id
#         post = Post.objects.get(pk = post_id)
#         # get a list of tag_id from ManyRelatedManager object
#         tags = []
#         for tag in post.tags.all():
#             tags.append(tag.tag_id)
#         # pre-populate form with values of the post
#         form = EditorForm(initial = { 'title': post.title, 'body': post.body, 'tags': tags, 'img_link': post.img_link })
#         return render(request = request, template_name = 'edit.html', context = { 'form': form, 'id': post_id })
#     if request.method == 'POST':    
#         # capture POST data as EditorForm instance
#         form = EditorForm(request.POST)
#         # validate form
#         if form.is_valid():
#             # if form was submitted by clicking Save
#             if 'save' in request.POST:
#                 # get cleaned data from form
#                 title = form.cleaned_data['title']
#                 img_link = form.cleaned_data['img_link']
#                 body = form.cleaned_data['body']
#                 tags = form.cleaned_data['tags']
#                 # filter QuerySet object by post_id
#                 posts = Post.objects.filter(pk = post_id)
#                 # update QuerySet object with cleaned title, body, img_link
#                 posts.update(title = title, body = body, img_link = img_link)
#                 # set cleaned tags to ManyRelatedManager object
#                 posts[0].tags.set(tags)
#             # if form was submitted by clicking Delete
#             elif 'delete' in request.POST:
#                 # filter QuerySet object by post_id and delete it
#                 Post.objects.filter(pk = post_id).delete()
#         # redirect to 'blog/'
#         return HttpResponseRedirect(reverse('blog'))

def featured(request):
    if request.method == 'GET':
        form = CommentForm()
        # featured = Exhibit()
        for exhibit in Exhibit.objects.all().order_by('exhibit_id'):
            if exhibit.is_featured():
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
                comments.append({'author' : c.author, 'comment' : c.comment})

        return render(request = request, template_name = 'featured.html', context = { 
                    'exhibit': featured,
                    'images' : images, 
                    'form': form,
                    'comments' : comments})
    
    if request.method == 'POST':    
        form = CommentForm(data=request.POST)
        featured = Exhibit()
        for exhibit in Exhibit.objects.all().order_by('exhibit_id'):
            if exhibit.is_featured():
                featured = exhibit
       
        if form.is_valid():
            comment = form.cleaned_data['comment']
            author = form.cleaned_data['author']
            created = datetime.datetime.now()
            Comment.objects.create(comment=comment, created=created, author=author, exhibit=featured)
            return HttpResponseRedirect(reverse('featured'))


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