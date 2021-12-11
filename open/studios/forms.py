from django import forms
from django.forms.formsets import formset_factory
from .models import *


class ExhibitForm(forms.Form):
    artist_name = forms.CharField(max_length = 255, required = True)
    email = forms.EmailField(max_length = 254, required = True)
    website = forms.URLField(max_length = 200, required = False)
    bio = forms.CharField(widget = forms.Textarea, required = True)
    
    exhibit_name = forms.CharField(max_length = 255, required = True)
    description = forms.CharField(widget = forms.Textarea, required=True)
    
    choices = []
    for tag in Tag.objects.all():
        choices.append((tag.tag_id, tag.name))
    tags = forms.MultipleChoiceField()
    description = forms.CharField(widget = forms.Textarea, required=True)


class CommentForm(forms.Form):
    comment = forms.CharField(widget = forms.Textarea)
    author = forms.CharField()
    
    class Meta:
        parent_model = Comment
        model = Exhibit
        fk_name = 'comments'
        fields = ('comment', 'author')

CommentFormSet = formset_factory(CommentForm, extra = 1)

class ImageForm(forms.Form):
    name = forms.CharField(max_length = 255)
    url = forms.URLField(label = "Image URL", max_length = 200)
    
    class Meta:
        parent_model = Image
        model = Exhibit
        fk_name = 'images'
        fields = ('name', 'url')
        min_num = 1
        max_num = 20

ImageFormSet = formset_factory(ImageForm, extra = 10)
    # upload = forms.ClearableFileInput()

class TagForm(forms.Form):
    name = forms.CharField(max_length = 255)
    
    class Meta:
        parent_model = Tag
        model = Exhibit
        fk_name = 'tags'
        fields = ('name')
        min_num = 1

TagFormSet = formset_factory(TagForm, extra = 1)

