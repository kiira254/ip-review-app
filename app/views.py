from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
import datetime as dt
from .models import Profile
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,ProfileForm
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
def profile(request, id):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)
  user = request.user
  projects = Project.objects.filter(poster=frank).order_by('-pub_date')
  projectcount=projects.count()
  return render(request, 'profile/profile.html',{'profile':profile,'user':user,'projectcount':projectcount,'projects':projects})

@login_required(login_url='/accounts/login/')
def newprofile(request):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)
  
  
  if request.method == 'POST':
    instance = get_object_or_404(Profile, user=user)
    form = ProfileForm(request.POST, request.FILES,instance=instance)
    if form.is_valid():
      form.save()
    return redirect('profile', user)

  else:
    
    form = ProfileForm()

  return render(request, 'profile/newprofile.html',{'form':form,'profile':profile})

def home(request):
    
    
    return render(request, 'index.html')


@login_required(login_url='/accounts/login/')
def search(request):
  user = request.user.id
  profile = Profile.objects.get(user=user)


  if 'project' in request.GET and request.GET['project']:
    search_term = request.GET.get('project')
    message = f'{search_term}'
    title = 'Search Results'

    try:
      no_ws = search_term.strip()
      searched_projects = Project.objects.filter(title__icontains = no_ws)

    except ObjectDoesNotExist:
      searched_projects = []

    return render(request, 'search.html',{'message':message ,'title':title, 'searched_projects':searched_projects,'profile':profile})

  else:
    message = 'You havenot searched for any projects'
    
    title = 'Search Error'
    return render(request,'search.html',{'message':message,'title':title,'profile':profile})

