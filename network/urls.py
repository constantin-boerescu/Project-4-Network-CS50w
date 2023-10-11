
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<int:user_id>", views.user_profile, name="user_profile"),
    path("togglefollow/<int:user_id>/<str:action>", views.togglefollow, name="togglefollow"),
    path("following_page", views.following_page, name="following_page"),
    path('like_post/<int:post_id>', views.like_post, name='like_post'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),

    
]
