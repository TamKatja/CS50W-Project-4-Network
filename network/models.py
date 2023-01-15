import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_picture = models.ImageField(default="profile_pictures/default.png", upload_to="profile_pictures")
    following = models.ManyToManyField("self", related_name="followers", blank=True, null=True, symmetrical=False)

    def __str__(self):
        return self.username


class Post(models.Model):
    content = models.TextField() 
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_edited = models.DateTimeField(default=datetime.datetime.now())
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="likes", blank=True, null=True)

    class Meta:
        ordering = ["-timestamp_created"]

    def like_count(self):
        return self.liked_by.count()

    def __str__(self):
        return f"{self.author} posted: {self.content}"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "timestamp_created": self.timestamp_created.strftime("%d %b %Y, %H:%M %p"),
            "timestamp_edited": self.timestamp_edited.strftime("%d %b %Y, %H:%M %p"),
            "author": self.author.username,
            "liked_by": [user.username for user in self.liked_by.all()],
            "like_count": self.like_count()
        }