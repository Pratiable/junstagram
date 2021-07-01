from django.db import models

from user.models import User
from likes.models import Like

class Post(models.Model):
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    content    = models.CharField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes      = models.ManyToManyField(User, related_name='users', through='Like')

    class Meta:
        db_table = 'posts'

class Image(models.Model):
    post      = models.ForeignKey(Post, on_delete=models.CASCADE)
    url       = models.URLField(max_length=2000)

    class Meta:
        db_table = 'images'

class Comment(models.Model):
    post           = models.ForeignKey(Post, on_delete=models.CASCADE)
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    nested_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    content        = models.CharField(max_length=500)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'