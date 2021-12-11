from django.db import models
import datetime

# Create your models here.
class Tag(models.Model):
    tag_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

class Image(models.Model):
    image_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 255)
    url = models.URLField(max_length = 200)
    featured = models.BooleanField(default = False)
    # upload = models.ImageField(upload_to = "upload/", blank = True, max_length=255)
    # description = models.CharField()
    
    class Meta:
        verbose_name_plural = 'Images'
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    comment_id = models.AutoField(primary_key = True)
    comment = models.TextField()
    author = models.CharField(max_length = 255, default="")
    
    class Meta:
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return self.comment

class Exhibit(models.Model):
    exhibit_id = models.AutoField(primary_key = True)
    exhibit_name = models.CharField(max_length = 255)
    description = models.TextField()
    timestamp = models.DateField(auto_now = True, auto_now_add = False)
    featured_date = models.DateField(auto_now = False, null = True)
    featured = models.BooleanField(default = False)
    revealed = models.BooleanField(default = False)
    
    # Linked classes
    tags = models.ManyToManyField(Tag)
    images = models.ForeignKey(Image, default = int, related_name = "gallery",  on_delete = models.SET_DEFAULT)
    comments = models.ForeignKey(Comment, default = 1, related_name = "response", on_delete = models.SET_DEFAULT)
    
    # potentially will be moved to User model
    artist_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 254)
    website = models.URLField(max_length = 200)
    bio = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Exhibits'
    
    def __str__(self):
        return self.exhibit_name
    
    def is_featured(self):
        return self.featured
    
    def add_featured(self):
        self.featured = True
        self.featured_date = datetime.datetime.now()
    
    def remove_featured(self):
        self.featured = False
        self.revealed = True


class Rotation(models.Model):
    rotation_id = models.AutoField(primary_key = True)
    current = models.ForeignKey(Exhibit, related_name='exhibit', default = 1, on_delete = models.CASCADE)
    # upcoming = models.OneToOneField(Exhibit, on_delete = models.CASCADE, related_name = 'timestamp',)
    delay = models.TimeField(auto_now = False, auto_now_add = False)
    
    class Meta:
        verbose_name_plural = 'Rotations'
    
    def __str__(self):
        return self.current.exhibit_name
    
    def upcoming():
        exhibits = []
        for e in Exhibit.objects.all().order_by('timestamp'):
            if not e.revealed and not e.is_featured():
                exhibits.append({'name' : e.exhibit_name, 'created' : e.timestamp, 'id' : e.exhibit_id})
        return exhibits[0]


#*****Potential Post MVP*****

# class User(models.Model):

# class Security(models.Model):