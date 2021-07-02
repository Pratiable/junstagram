# Generated by Django 3.2.4 on 2021-07-02 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
        ('user', '__first__'),
        ('postings', '0002_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='likes', through='likes.Like', to='user.User'),
        ),
    ]
