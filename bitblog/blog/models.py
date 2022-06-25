from django.db import models
import datetime
from django.utils import timezone


class Post(models.Model):
    post_date = models.DateTimeField('post pub date')
    user_img = models.ImageField(upload_to='img/user')
    user_name = models.CharField('Username who published post', max_length=30)
    post_img = models.ImageField(upload_to='img/post')
    likes = models.DecimalField(max_digits=5, decimal_places = 0)
    comments = models.DecimalField(max_digits=5, decimal_places = 0)
    def __str__(self):
        return self.user_name
    def was_published_recently(self):
        return self.post_date >=(timezone.now() - datetime.timedelta(days = 7))


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_img = models.ImageField(upload_to='img/user')
    user_name = models.CharField('Username who published post', max_length=30)
    author_comment_text = models.TextField('Comment text', max_length=300)
    def __str__(self):
        return self.author_comment_text

class Profile(models.Model):
    user_img = models.ImageField(upload_to='img/user')
    user_name = models.CharField('Username', max_length=30)
    posts = models.DecimalField(max_digits=5, decimal_places = 0)
    subscribers = models.DecimalField(max_digits=5, decimal_places = 0)
    subscriptions = models.DecimalField(max_digits=5, decimal_places = 0)
    def __str__(self):
        return self.user_name
