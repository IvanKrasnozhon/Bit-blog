from django.db import models
import datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib import admin



class Profile(models.Model):
    user_img = models.ImageField(upload_to='img/user')
    posts = models.DecimalField(max_digits=5, decimal_places = 0, default=0)
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
    def __str__(self):
        return self.profile.user.username
    def was_published_recently(self):
        return self.post_date >=(timezone.now() - datetime.timedelta(days = 7))