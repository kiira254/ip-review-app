from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
import datetime as dt
from .models import Image, Profile, Like, Comments
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .forms import LetterForm, ImageForm,SignupForm,ProfileForm, CommentForm
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    name = "Sign Up"
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('username')
            send_mail(
            'Welcome to Mini-Insta.',
            f'Hello {name},\n '
            'Welcome to Mini-Insta.',
            'nkamotho69@gmail.com',
            [email],
            fail_silently=False,
            )
        return redirect('post')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form, 'name':name})

@login_required(login_url='/accounts/login/')
