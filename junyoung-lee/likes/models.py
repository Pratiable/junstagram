from django.db import models

class Like(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey('postings.Post', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'