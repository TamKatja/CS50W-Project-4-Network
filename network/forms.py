from django.forms import ModelForm

from .models import User

class UploadProfilePicture(ModelForm):
    class Meta:
        model = User
        fields = ["profile_picture"]