from django.db import models

# Create your models here.

class Tag(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

class Image(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 255)
    url = models.URLField(max_length = 200)
    # upload = models.ImageField(upload_to = "upload/", blank = True, max_length=255)
    # description = models.CharField()
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    id = models.AutoField(primary_key = True)
    comment = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

class Exhibit(models.Model):
    id = models.AutoField(primary_key = True)
    exhibit_name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    timestamp = models.DateField(auto_now = False, auto_now_add = False)
    tags = models.ManyToManyField(Tag)
    # images = models.ManyToOneRel(Image,to = models.URLField, field_name = 'url' )
    comment = models.ManyToOneRel(Comment, to = models.CharField, field_name = 'comment')
    # potentially will be moved to User model
    artist_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 254)
    website = models.URLField(max_length = 200)
    bio = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.exhibit_name

class Rotation(models.Model):
    id = models.AutoField(primary_key = True)
    # current = models.ForeignKey(Exhibit, on_delete = models.CASCADE)
    # upcoming = models.ForeignKey(Exhibit, on_delete = models.CASCADE)
    delay = models.TimeField(auto_now = False, auto_now_add = False)
    
    def __str__(self):
        return self.current.name


#*****Potential Post MVP*****

# class User(models.Model):

# class Security(models.Model):