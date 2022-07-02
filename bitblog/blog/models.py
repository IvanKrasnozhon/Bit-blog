from django.db import models
import datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib import admin



class Profile(models.Model):
    user_img = models.ImageField(upload_to='img/user')
    posts = models.DecimalField(decimal_places = 0, max_digits = 20, default=0)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_id': self.pk})
    def save_model(self, request, obj, form, change):
        obj.profile = request.user.profile
        super().save_model(request, obj, form, change)

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    post_date = models.DateTimeField('post pub date', auto_now_add=True)
    post_img = models.ImageField(upload_to='img/post')
    post_info = models.CharField(max_length=300, default=None)
    def __str__(self):
        return self.profile.user.username
    def was_published_recently(self):
        return self.post_date >=(timezone.now() - datetime.timedelta(days = 7))
    def get_absolute_url(self):
        return reverse('show_post', kwargs={'post_id': self.pk})
    def post_comment_add(self):
        return reverse('add_comment', kwargs={'post_id': self.pk})

class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    comment_date = models.DateTimeField('post pub date', auto_now_add=True)
    comment_info = models.CharField(max_length=300, default=None)
    def __str__(self):
        data = self.profile.user.username + ': \n' + self.comment_info + '\n' + self.comment_date
        return data
