from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=50)
    nickname     = models.CharField(max_length=50)
    email        = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    password     = models.CharField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    followers    = models.ManyToManyField(
        'self',
        through        = 'Follow',
        through_fields = ('followee', 'follower'),
        symmetrical    = False,
        related_name   = 'following'
    )
    
    class Meta:
        db_table = 'users'

class Follow(models.Model):
    followee   = models.ForeignKey(
        User, 
        related_name = 'followee',
        on_delete    = models.CASCADE
        )
    follower     = models.ForeignKey(
        User, 
        related_name = 'follower',
        on_delete    = models.CASCADE
        )
    
    class Meta:
        db_table = 'follows'