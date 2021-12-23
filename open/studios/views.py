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

# The code is a request for the featured exhibit teaser and the next exhibit to be featured.
def main(request):
    # The code starts by initializing the featured variable to an empty string.
    featured = next_exhibit = ''
    images = []
    
    # The main function first calls get_featured(), which returns a dictionary containing information about all of the exhibits currently on display at this gallery.
    featured = get_featured()
    next_exhibit = coming_exhibit()
    
    # It then uses today as the current date and time to calculate how long ago they were last displayed for public viewing (time_featured) using datetime's .today() method.
    today = datetime.date.today()
    time_featured = today - featured.featured_date
    
    #If time_featured is greater than one day ago, then it removes any previously-displayed exhibits from featured with remove_featured().
    if (time_featured.days > 1):
        # After removing any previously-displayed exhibits from featured, save()s them back into their original state before displaying them again later on in this loop.
        featured.remove_featured()
        featured.save()
        next_exhibit.add_featured()
        next_exhibit.save()
        featured = next_exhibit

        # After saving all of these features back into their original state again, featured becomes whatever exhibit comes next in this loop--in other words, what will be displayed next when we run through this loop again later on down below where we have reset() being called instead of adding new features to showcase every time around our loop.
        if coming_exhibit() == '':
            next_exhibit = reset()

        else:
            next_exhibit = coming_exhibit()
    # Next, it gets all of the images from featured's pics attribute and orders them by their image ID (the -image_id part).
    for image in featured.pics.all().order_by('-image_id'):
        # Then it checks if each image has been featured before; if so, then it appends its name to a list called images.
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


# The code attempts to show an image for a given name.
def show_image(request, name):
    if request.method == 'GET':
        image = Image()
        
        # It iterates through all of the images in the database, and then checks if each image has a name that matches the given name.
        for pic in Image.objects.all().order_by('image_id'):
            if pic.name == name:
                image = pic
        # If so, it returns the template displaying the image.
        return render(request, 'image.html', context = {'image' : image})


# The code is a request for the featured exhibit.
def featured(request):
    if request.method == 'GET':
        # The code starts by creating a CommentForm class instance,which returns a dictionary containing all of the fields on our form. 
        form = CommentForm()
        
        # For each Exhibit object, we order them by exhibit_id and check to see if they are featured. If so, we create an instance of that Exhibit with its own images and comments lists.
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
        # The code starts by defining a variable called form, which is the object that is used to store data from the comment form. 
        form = CommentForm(initial = request.POST)
        
        # Next, it defines a variable called featured which will hold the featured exhibit that is currently being displayed on the homepage.
        featured = Exhibit()
        for exhibit in Exhibit.objects.all().order_by('exhibit_id'):
            if exhibit.featured:
                featured = exhibit

        if form.is_valid():
            # Next it assigns the cleaned data to variables that match the attributes in a Comment object.
            comment = form.cleaned_data['comment']
            author = form.cleaned_data['author']
            created = datetime.date.today()
            # Then it creates a new Comment instance with its own set of fields.
            Comment.objects.create(
                                comment = comment, 
                                created = created, 
                                author = author, 
                                exhibit = featured)
            
            # Finally after creating these instances they return an HTTP response redirecting back to "featured" if everything went well with creating this new Comment instance.
            return HttpResponseRedirect(reverse('featured'))


# The code is a request for the upcoming page of exhibits.
def upcoming(request):
    if request.method == 'GET':
        # then it will use the Exhibit.objects.exclude() method to find all of the exhibits that are not featured or revealed.
        exhibits = Exhibit.objects.exclude(featured = True).exclude(revealed = True)
        
        art = []
        # Next, for each exhibit in 'exhibits', we iterate through its images using the pics attribute and check if they are featured.
        for exhibit in exhibits:
            for i in exhibit.pics.all():
                if i.featured:
                    # If they are, then we add their url, name, id number (the image_id), and collection information to our list of upcoming exhibits.
                    art.append({
                            'url' : i.url, 
                            'name' : i.name, 
                            'id' : i.image_id,
                            'collection' : exhibit.exhibit_id})
        # Finally the template is displayed to the user listing the exhibits that will be featured in time.
        return render(request = request, template_name = 'upcoming.html', context = {'exhibits' : exhibits, 'images' : art})


# The code is information for the about page.
def about(request):
    # The code starts by defining a list of profiles.
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
            'linkedin' : 'https://www.linkedin.com/in/lee-harvey-jr?lipi=urn%3Ali%3Apage%3Ad_flcreateagship3_profile_view_base_contact_details%3BIvwSNWutSqaVtbFzP0%2BtHg%3D%3D'
        }, 
        {'name' : 'Jason Rolle',
            'image' : '/static/media/images/jason.jpg',
            'git' : 'https://github.com/JasonRolle1990',
            'linkedin' : 'https://www.linkedin.com/in/jasonrolle1990?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3Bculc7Op7S3esL9F80ZfMhw%3D%3D'
        }]

    # The code then defines a list of links.
    links = [{'name': 'Facebook', 'icon': '/static/media/images/facebook.png', 'site': 'https://www.facebook.com'}, {'name': 'Instagram', 'icon': '/static/media/images/instagram.png', 'site': 'https://www.instagram.com/'}, {'name': 'Twitter', 'icon': '/static/media/images/twitter.png', 'site': 'https://twitter.com/'}
    ]
    
    # Then the template about.html is returned with the listed information to be presented.
    return render(request, 'about.html', {'profiles' : profiles, 'links': links})




# ===================================================================================================
# ----------------------------------------- Create and Edit -----------------------------------------
# ===================================================================================================


# ---------------------------------------------- Images ---------------------------------------------
path = ''

# This function is used to create an image in a new exhibit.
def create_image(request):
    # The first line of code defines what type of action this function will perform, to be passed to the cne_image template (create and edit image) for defining what is displayed to the user.
    action = 'create'
    if request.method == 'GET':
        # The code starts by defining a variable called form, which is the object that is used to store data from the image form.
        form = ImageForm()
        
        # Then form and action are passed to the template to be displayed.
        return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})
    
    if request.method == 'POST':
        # The code starts by defining a variable called form, which is the object that is storing data from the image form.
        form = ImageForm(request.POST)
        if form.is_valid():
            
            # Next it assigns the cleaned data to variables that match the attributes in a Image object.
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            featured = form.cleaned_data['featured']
            
            # Then it creates a new Image instance with its own set of fields.
            Image.objects.create(name = name, url = url, featured = featured)
            
            # Finally it returns to the create exhibit page.
            return HttpResponseRedirect(reverse(action))
        else:
            # Should the form not be valid, returns the user to the create image page with the entered information for editing.
            return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})


def create_edit_image(request, image_id):
    # The first line of code defines what type of action this function will perform, to be passed to the cne_image template (create and edit image) for defining what is displayed to the user.
    action = 'edit'
    
    # Next it accessed the global variable path that has the dynamic uri for the exhibit being edited.
    global path
    
    # Then we check the global variable path for upcoming to define the page that the user will be redirected to depending on how this funcion was accessed.
    if 'upcoming' in path:
        # We parse the path for the exhibit_id to be assigned to e_id for use in the reverse redirect.
        e_id = int(path.split("/")[-1])
        
        # We assign the page url name to the page variable for the reverse redirect.
        page = 'edit'
    else:
        page = 'create'
    
    if request.method == 'GET':
        # The code starts by getting the image with the ID of "image_id" from the database and saving it to a variable called "image".
        image = Image.objects.get(pk = image_id)
        
        # Next, we create an instance of ImageForm using initial parameters that will be passed into render().
        form = ImageForm(initial = {
            'image_id' : image.image_id,
            'name' : image.name, 
            'url' : image.url, 
            'featured' : image.featured})
        
        # Finally, we return a response to the client with our newly created form in HTML format.
        return render(request, 'cne_image.html', context = {'form' : form, 'action' : action, 'image' : image})
    
    if request.method == 'POST':
        # The code starts by defining a variable called form, which is the object that is storing data from the image form.
        form = ImageForm(request.POST)
        
        # The code checks if the form has been validated or not.
        if form.is_valid():
            
            if 'save' in request.POST:
                # If it has, then some data from the form are cleaned up and saved in an instance of Image called image.
                name = form.cleaned_data['name']
                url = form.cleaned_data['url']
                featured = form.cleaned_data['featured']
                
                image = Image.objects.filter(image_id = image_id)
                image.objects.update(name = name, url = url, featured = featured)
                
                
                path = ''
                if page == 'edit':
                    # If the action is edit, then the return call will utilize the page variable and necessary keyword arguments.
                    return HttpResponseRedirect(reverse(page, kwargs = {'exhibit_id' : e_id}))
                else:
                    # If the action is not edit, the the return call will utilize the page variable.
                    return HttpResponseRedirect(reverse(page))
            elif 'delete' in request.POST:
                # We retrieve the instance of the Image object that is defined by "image_id".
                image = Image.objects.get(pk = image_id)
                
                # Next we delete this Image instance.
                image.delete()
                
                # Then we clear the path global variable.
                path = ''
                if page == 'edit':
                    # If the action is edit, then the return call will utilize the page variable and necessary keyword arguments.
                    return HttpResponseRedirect(reverse(page, kwargs = {'exhibit_id' : e_id}))
                else:
                    # If the action is not edit, the the return call will utilize the page variable.
                    return HttpResponseRedirect(reverse(page))
        else:
            # Assign the image object with "image_id" to image in order to provide the template with access to the object for editing.
            image = Image.objects.get(pk = image_id)
            
            # Should the form not be valid, returns the user to the create image page with the entered information for editing.
            return render(request, 'cne_image.html', context = {'form' : form, 'action' : action, 'image' : image})


# This function is used to create an image in a new exhibit.
def upcoming_create_image(request):
    # The first line of code defines what type of action this function will perform, to be passed to the cne_image template (create and edit image) for defining what is displayed to the user.
    action = 'upcoming'
    
    if request.method == 'GET':
        # The code starts by defining a variable called form, which is the object that is used to store data from the image form.
        form = ImageForm()
        
        # Then form and action are passed to the template to be displayed.
        return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})
    
    if request.method == 'POST':
        # The code starts by defining a variable called form, which is the object that is storing data from the image form.
        form = ImageForm(request.POST)
        if form.is_valid():
            
            # Next it assigns the cleaned data to variables that match the attributes in a Image object.
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            featured = form.cleaned_data['featured']
            
            # Then it creates a new Image instance with its own set of fields.
            Image.objects.create(name = name, url = url, featured = featured)
            
            # Next it accessed the global variable path that has the dynamic uri for the exhibit being edited.
            global path
            
            # We parse the path for the exhibit_id to be assigned to e_id for use in the reverse redirect.
            e_id = int(path.split("/")[-1])
            
            # Then we clear the path global variable.
            path = ''
            
            # Finally we return the user to the edit exhibit template where they had accessed the add image button.
            return HttpResponseRedirect(reverse('edit', kwargs={'exhibit_id' : e_id}))
        else:
            # Should the form not be valid, returns the user to the create image page with the entered information for editing.
            return render(request, 'cne_image.html', context = {'form' : form, 'action' : action})


# --------------------------------------------- Exhibits --------------------------------------------


# This code is used to create an Exhibit instance.
def create_exhibit(request):
    action = 'create'
    if request.method == 'GET':
        # The code starts by creating a form object. 
        form = ExhibitForm()
        
        # Next, the code iterates over Image instances with the exhibit_name set to None. This is to display any images that are not associated with an exhibit.
        images = []
        for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
            images.append(image)
        
        # The next line iterates through all of the tags in Tag objects and appends them to an array called tags.
        tags = []
        for tag in Tag.objects.all():
            tags.append(tag.tag_id)
        
        # Next, there is a dictionary that contains information about what actions are being performed (create), which tags are being used (tags), as well as some context variables such as form and action.
        context = {
            'form' : form, 
            'action' : action,
            'tags' : tags,
            'uri' : request.path,
            } 
        
        # Then there is an evaluation to determine if the images list has any entries.
        if len(images) > 0:
            # If there are entries, then the image key value pair is added to context.
            context['images'] = images
        
        # Render the exhibit template with the context values assigned previously.
        return render(request, 'exhibit.html', context )
    
    if request.method == 'POST':
        # The code starts by defining a variable called form, which is the object that is storing data from the exhibit form.
        form = ExhibitForm(request.POST)
        tags = images = []
        images = []
        
        #Next, the code iterates over Image instances with the exhibit_name set to None. This is to retrieve a list of any images that are not associated with an exhibit in order to assign them to the instantiation of this exhibit.
        for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
            images.append(image)
        
        # The code checks if the form has been validated or not.
        if form.is_valid():
            # Next it assigns the cleaned data to variables that match the attributes in a Exhibit object.
            artist_name = form.cleaned_data['artist_name']
            email = form.cleaned_data['email']
            bio = form.cleaned_data['bio']
            website = form.cleaned_data['website']
            exhibit_name = form.cleaned_data['exhibit_name']
            description = form.cleaned_data['description']
            tags = form.cleaned_data['tags']
            
            # Then it creates a new Image instance with its own set of fields.
            Exhibit.objects.create(
                artist_name = artist_name,
                email = email, 
                bio = bio,
                website = website,
                exhibit_name = exhibit_name,
                description = description)
            
            # Next a list of Exhibit instances are returned in reverse.  This allows for the latest addition to be at the beginning of the list.
            exhibit = Exhibit.objects.all().order_by('-exhibit_id')
            
            # Next the tags are associated with the exhibit.
            exhibit[0].tags.set(tags)
            
            # Then iterate over the images checking for the featured attribute.  Any Image instances with the featured attribute enabled, the number of current featured images is checked to ensure no more than four are assigned this attribute.
            for image in images:
                if image.featured:
                    if len(exhibit[0].pics.filter('featured')) <= 3:
                        exhibit[0].pics.add(image)
                    else:
                        # If there are already four featured images, change the featured attribute and add the image to the exhibit.
                        image.featured = False
                        exhibit[0].pics.add(image)
                else:
                    # Assign any images without the featured attribute to the newest exhibit.
                    exhibit[0].pics.add(image)
            
            # Finally it returns to the upcoming exhibit page.
            return HttpResponseRedirect(reverse('upcoming'))
        else:
            # Should the form not be valid, returns the user to the create exhibit page with the entered information for editing.
            return render(request, 'exhibit.html', context = {'form' : form, 'tags' : tags, 'images' : images} )


# This code is used to edit an Exhibit instance.
def edit_exhibit(request, exhibit_id):
    # The first line of code defines what type of action this function will perform, to be passed to the exhibit template for defining what is displayed to the user.
    action = 'edit'
    
    # Next it accessed the global variable path that has the dynamic uri for the exhibit being edited.
    global path
    
    # Then we assign the global variable path with the dynamically created edit exhibit uri.
    path = request.get_full_path()
    
    if request.method == 'GET':
        # The code starts by getting the Exhibit with the ID of "exhibit_id" from the database and saving it to a variable called "exhibit".
        exhibit = Exhibit.objects.get(pk = exhibit_id)
        
        # The next line iterates through all of the tags in Tag objects associated with this Exhibit instance and appends them to an array called tags.
        tags = []
        for tag in exhibit.tags.all():
            tags.append(tag.tag_id)
        
        images = []
        #Next, the code iterates over Image instances with the exhibit_name set to None. This is to display any images that are not associated with an exhibit.
        for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
            images.append(image)
        
        # Next, we create an instance of ExhibitForm using initial parameters that will be passed into render().
        form = ExhibitForm(initial = {
            'artist_name' : exhibit.artist_name, 
            'email' : exhibit.email, 
            'bio' : exhibit.bio,  
            'website' : exhibit.website, 
            'exhibit_name' : exhibit.exhibit_name,
            'description' : exhibit.description, 
            'tags' : tags})
        
        # Finally, we return a response to the client with our newly created form in HTML format.
        return render(request, 'exhibit.html', context = {'form' : form, 'exhibit' : exhibit, 'action' : action, 'images' : images})
    
    if request.method == 'POST':
        # The code starts by defining a variable called form, which is the object that is storing data from the exhibit form.
        form = ExhibitForm(request.POST)
        
        # The code checks if the form has been validated or not.
        if form.is_valid():
            if 'save' in request.POST:
                # If it has, then some data from the form are cleaned up and saved in an instance of Exhibit called exhibit.
                artist_name = form.cleaned_data['artist_name']
                email = form.cleaned_data['email']
                bio = form.cleaned_data['bio']
                website = form.cleaned_data['website']
                exhibit_name = form.cleaned_data['exhibit_name']
                description = form.cleaned_data['description']
                tags = form.cleaned_data['tags']
                
                # Next the Exhibit queryset specified by "exhibit_id" is assignedd to exhibit.
                exhibit = Exhibit.objects.filter(pk = exhibit_id)
                
                # Then the instance of Exhibit is populated with the edited attribute values.
                exhibit.update(
                    artist_name = artist_name,
                    email = email, 
                    bio = bio,
                    website = website,
                    exhibit_name = exhibit_name,
                    description = description)
                
                art = []
                # Next, the code iterates over Image instances with the exhibit_name set to None. This is to assemble any images that are not associated with an exhibit.
                for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
                    art.append(image)
                
                # Next the Exhibit instance specified by "exhibit_id" is assignedd to exhibit.
                exhibit = Exhibit.objects.get(pk = exhibit_id)
                
                # The next line iterates through all of the tags in Tag objects associated with this Exhibit instance and appends them to an array called tags.
                for tag in exhibit.tags.all():
                    tags.append(tag.tag_id)
                
                # Next the tags are associated with the exhibit.
                exhibit.tags.set(tags)
                
                # Then iterate over the images checking for the featured attribute.  Any Image instances with the featured attribute enabled, the number of current featured images is checked to ensure no more than four are assigned this attribute.
                for image in art:
                    if image.featured:
                        if len(exhibit.pics.filter('featured')) <= 3:
                            exhibit.pics.add(image)
                        else:
                            # If there are already four featured images, change the featured attribute and add the image to the exhibit.
                            image.featured = False
                            exhibit.pics.add(image)
                    else:
                        # Assign any images without the featured attribute to the newest exhibit.
                        exhibit.pics.add(image)
                
            elif 'delete' in request.POST:
                # Next the Exhibit instance specified by "exhibit_id" is assignedd to exhibit.
                exhibit = Exhibit.objects.get(pk = exhibit_id)
                
                # Next we delete the Image instances that are associated with the current exhibit.
                for image in exhibit.pics.all():
                    image.delete()
                
                # Next we delete the Comment instances that are associated with the current exhibit.
                for cmnt in exhibit.responses.all():
                    cmnt.delete()
                
                # Then we can finally delete the exhibit.
                exhibit.delete()
            # Then we clear the path global variable.
            path = ''
            
            # Finally we return the client to the upcoming template.
            return HttpResponseRedirect(reverse('upcoming'))
        else:
            # Next the Exhibit instance specified by "exhibit_id" is assignedd to exhibit.
            exhibit = Exhibit.objects.get(pk = exhibit_id)
        
            tags = []
            for tag in exhibit.tags.all():
                tags.append(tag.tag_id)
            
            images = []
            
            # Next, the code iterates over Image instances with the exhibit_name set to None. This is to assemble any images that are not associated with an exhibit.
            for image in Image.objects.filter(exhibit_name = None).order_by('image_id'):
                images.append(image)
            
            # Should the form not be valid, returns the user to the create exhibit page with the entered information for editing.
            return render(request, 'exhibit.html', context = {'form' : form, 'exhibit' : exhibit, 'images' : images} )


# ===================================================================================================
# ------------------------------------------------- Logic -------------------------------------------
# ===================================================================================================


# The code returns the featured exhibit at the end of its execution.
def get_featured():
    # The code starts by getting all the exhibits in the database. It then loops through each of them and orders them by their timestamp.
    for exhibit in Exhibit.objects.all().order_by('-timestamp'):
        if exhibit.featured:
            # If an exhibit is featured, it will store that feature into a variable called "featured".
            featured = exhibit
    return featured


# The code is a function that compiles the next featured Exhibit object.
def coming_exhibit():
    # The code starts by checking if there are any exhibits that have been featured and revealed.
    if len(Exhibit.objects.filter(featured=False, revealed=False)) > 0:
        
        # If so, the first exhibit not featured or revealed is selected and returned.
        next_exhibit = Exhibit.objects.filter(featured=False, revealed=False).first()
    else:
        
        # Otherwise, it returns an empty string.
        next_exhibit = ''
    return next_exhibit


# The code attempts to return an object that was previously saved and has been set back to its original state.
def reset():
    # The code starts by creating a variable called exhibit and, goes on to create an instance of the Exhibit class, which is the object that will be used for all operations in this function, by ordering all objects from the Exhibit class according to their featured_date attribute and filters them so that only one object is returned - the first object in the list.
    exhibit = Exhibit.objects.all().order_by('featured_date').filter(featured = False, revealed = True).first()
    
    # This first object has its featured property set to False and its revealed property set to False.
    exhibit.revealed = False
    
    # Then, it saves this single object back into memory using save().
    exhibit.save()
    
    # Finally the exhibit object is returned to the calling function.
    return exhibit


# ===================================================================================================
# ------------------------------------------------- Users -------------------------------------------
# ===================================================================================================


def register(request):
    pass


def login(request):
    pass
