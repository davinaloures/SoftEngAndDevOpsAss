from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


#creating table post
class Post(models.Model):
    #creating fields in table
    title=models.CharField( max_length=100) #maximum number of characters for title set to 100
    category=models.CharField(max_length=100, default='N/A')
    status=models.CharField(max_length=100, default='Active')
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now) #passing function as default value
    author=models.ForeignKey(User, on_delete=models.CASCADE) #if a user is deleted, then post is also deleted

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})