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
    comment = models.TextField()
    
    def __str__(self):
        return self.comment

class Exhibit(models.Model):
    id = models.AutoField(primary_key = True)
    exhibit_name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    timestamp = models.DateField(auto_now = True, auto_now_add = False)
    tags = models.ManyToManyField(Tag)
    images = models.ForeignKey(Image, default = 1, on_delete = models.CASCADE)
    comment = models.ForeignKey(Comment, default = 1, on_delete = models.DO_NOTHING)
    # potentially will be moved to User model
    artist_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 254)
    website = models.URLField(max_length = 200)
    bio = models.CharField(max_length = 255)
    featured = models.BooleanField(default = False)
    
    def __str__(self):
        return self.exhibit_name
    
    def is_featured(self):
        return self.featured


class Rotation(models.Model):
    id = models.AutoField(primary_key = True)
    current = models.ForeignKey(Exhibit, related_name='exhibit', default = 1, on_delete = models.CASCADE)
    # upcoming = models.OneToOneField(Exhibit, on_delete = models.CASCADE, related_name = 'timestamp',)
    delay = models.TimeField(auto_now = False, auto_now_add = False)
    
    def __str__(self):
        return self.current.name
    
    # def upcoming(self):
    #     exhibits = [ e.]


#*****Potential Post MVP*****

# class User(models.Model):

# class Security(models.Model):