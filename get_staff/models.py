from django.db import models

# Create your models here.
class Post_g(models.Model):

    title = models.CharField(max_length=30)
    content = models.TextField(default='content')



