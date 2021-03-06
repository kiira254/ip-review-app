from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Project, Rating

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
    email = forms.EmailField(max_length=200, help_text = 'Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ['user']

class ProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    exclude = ['poster','postername', 'pub_date']

class RatingForm(forms.ModelForm):
  class Meta:
    model = Rating
    exclude = ['average','project','postername','pub_date']
