from django import forms
from picastro.models import Post, PicastroUser


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = PicastroUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_no']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["image", "imageDescription", "imageCategory", "astroNameShort", "astroName",
                  "exposureTime", "moonPhase", "cloudCoverage", "bortle", "poster"]
