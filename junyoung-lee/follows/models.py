from django.db import models

class Follow(models.Model):
    follow_user   = models.ForeignKey('user.User', related_name='followed', on_delete=models.CASCADE)
    followers     = models.ForeignKey('user.User', related_name='follower', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'follows'