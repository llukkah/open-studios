from django import forms
from django.forms import inlineformset_factory
from django.forms.formsets import formset_factory
from django.forms.widgets import HiddenInput
from .models import *


class ImageForm(forms.Form):
    name = forms.CharField(max_length = 255)
    url = forms.URLField(label = "Image URL", max_length = 200)
    featured = forms.BooleanField(widget = forms.CheckboxInput, required = False)
    class Meta:
        parent_model = Exhibit
        model = Image
        fk_name = 'images'
        fields = ('name', 'url')

ImageFormSet = formset_factory(ImageForm, extra = 20, max_num = 10)
    # upload = forms.ClearableFileInput()


class ExhibitForm(forms.Form):
    artist_name = forms.CharField(max_length = 255, required = True)
    email = forms.EmailField(max_length = 254, required = True)
    website = forms.URLField(max_length = 200, required = False)
    bio = forms.CharField(widget = forms.Textarea, required = True)
    
    exhibit_name = forms.CharField(max_length = 255, required = True)
    description = forms.CharField(max_length = 500, widget = forms.Textarea, required=True)
    featured = forms.BooleanField().hidden_widget
    featured_date = forms.DateField().hidden_widget
    
    choices = []
    for tag in Tag.objects.all():
        choices.append((tag.tag_id, tag.name))
    tags = forms.MultipleChoiceField(choices = choices, required = False)
    
    description = forms.CharField(max_length = 500, widget = forms.Textarea, required=True)
    
    class Meta:
        parent_model = Exhibit
        model = Image
        form = ImageForm()
        fk_name = 'images'
        fields = ('name', 'url')
        min_num = 1
        max_num = 20


class CommentForm(forms.Form):
    comment = forms.CharField(max_length = 500, widget = forms.Textarea, required = False)
    author = forms.CharField(max_length = 255, required = False)
    
    class Meta:
        parent_model = Comment
        model = Exhibit
        fk_name = 'comments'
        fields = ('comment', 'author')

CommentFormSet = formset_factory(CommentForm, extra = 1)


class TagForm(forms.Form):
    name = forms.CharField(max_length = 255)
    
    class Meta:
        parent_model = Tag
        model = Exhibit
        fk_name = 'tags'
        fields = ('name')
        min_num = 1

TagFormSet = formset_factory(TagForm, extra = 1)