from django import forms
from .models import *

class ExhibitForm(forms.Form):
    artist_name = forms.CharField(max_length=255, required = True)
    email = forms.EmailField(max_length=254)
    website = forms.URLField(max_length=200, required = False)
    bio = forms.CharField(widget=forms.Textarea, required=True)
    
    exhibit_name = forms.CharField(max_length=255, required = True)
    choices = []
    for tag in Tag.objects.all():
        choices.append((tag.id, tag.name))
    tags = forms.MultipleChoiceField()
    description = forms.CharField(widget=forms.Textarea, required=True)
    
    art = []
    for image in Image.objects.all():
        art.append((image.id, image.name, image.url))
    images = forms.MultipleChoiceField()

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, required=True)

class ImageForm(forms.Form):
    name = forms.CharField(max_length=255)
    url = forms.URLField(label = "Image URL", max_length = 200)
    # upload = forms.ClearableFileInput()

# ***** BLOG FORM *****
# class EditorForm(forms.Form):
#     title = forms.CharField(max_length=255, required=True)
#     img_link = forms.URLField(required=True)
#     body = forms.CharField(widget=forms.Textarea, required=True)
#     choices = []
#     for tag in Tag.objects.all():
#         choices.append((tag.tag_id, tag.name))
#     tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices, required=True)