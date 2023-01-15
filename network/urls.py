from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.get_profile, name="profile"),
    path("following", views.following, name="following"),

    # API Routes
    path("post/edit/<int:post_id>", views.edit_post, name = "edit_post"),
    path("profile/post/edit/<int:post_id>", views.edit_post, name = "edit_post"),
    path("post/like/<int:post_id>", views.like_post, name = "like_post"),
    path("following/post/like/<int:post_id>", views.like_post, name = "like_post")
]