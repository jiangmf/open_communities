from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    about = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/')

class Community(models.Model):
    name = models.CharField(max_length=32)
    about = models.TextField(blank=True)

class Post(models.Model):
    POST = 'post'
    MEDIA = 'media'
    LINK = 'link'
    TYPE_CHOICES = [
        (POST, 'Post'),
        (MEDIA, 'Media'),
        (LINK, 'Link'),
    ]

    type = models.CharField(
        max_length=5,
        choices=TYPE_CHOICES,
        default=POST,
    )
    
    author = models.ForeignKey('User', models.CASCADE, null=True)
    community = models.ForeignKey('Community', models.CASCADE)
    votes = models.ManyToManyField('User', through='PostVote', related_name='post_votes')

    link = models.URLField()
    media = models.FileField(upload_to='uploads/')
    content = models.TextField()


class PostVote(models.Model):
    class Meta:
        unique_together = ['user', 'post']

    user = models.ForeignKey('User', models.CASCADE)
    post = models.ForeignKey('Post', models.CASCADE)
    upvote = models.BooleanField()


class Comment(models.Model):
    author = models.ForeignKey('User', models.CASCADE)
    post = models.ForeignKey('Post', models.CASCADE)
    votes = models.ManyToManyField('User', through='CommentVote', related_name='comment_votes')

    parent = models.ForeignKey('Comment', models.CASCADE, null=True)

class CommentVote(models.Model):
    class Meta:
        unique_together = ['user', 'comment']

    user = models.ForeignKey('User', models.CASCADE)
    comment = models.ForeignKey('Comment', models.CASCADE)
    upvote = models.BooleanField()
