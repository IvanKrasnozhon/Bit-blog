from django.urls import path
from matplotlib.pyplot import show
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('profile/<int:profile_id>/', profile, name='profile'),
    path('addpost', addPost, name = 'add_post'),
    path('login', LoginUser.as_view(), name = 'login'),
    path('logout', logout_user, name = 'logout'),
    path('register', RegisterUser.as_view(), name = 'register'),
    path('edit_profile', EditProfile, name='edit_profile'),
    path('post/<int:post_id>/',  showPost, name='show_post'),
    path('addcomment/<int:post_id>/',  addComment, name='add_comment'),
]