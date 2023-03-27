from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["image", "imageDescription", "astroNameShort","astroName", "imageIsSaved",
        "award", "exposureTime","moonPhase", "cloudCoverage","bortle", "starCamp","leadingLight"]



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)