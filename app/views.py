from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
import datetime as dt
from .models import Profile, Project
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, ProfileForm, ProjectForm
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
    return render(request, 'registration/registration_form.html', {'form': form, 'name': name})


@login_required(login_url='/accounts/login/')
def profile(request):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)
  user = request.user
  projects = Project.objects.filter(poster=frank).order_by('-pub_date')
  projectcount = projects.count()
  return render(request, 'profile/profile.html', {'profile': profile, 'user': user, 'projectcount': projectcount, 'projects': projects})


@login_required(login_url='/accounts/login/')
def newprofile(request):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)

  if request.method == 'POST':
    instance = get_object_or_404(Profile, user=user)
    form = ProfileForm(request.POST, request.FILES, instance=instance)
    if form.is_valid():
      form.save()
    return redirect('profile', user)

  else:

    form = ProfileForm()

  return render(request, 'profile/newprofile.html', {'form': form, 'profile': profile})


@login_required(login_url='/accounts/login/')
def myprojects(request):
  id = request.user.id
  profile = Profile.objects.get(user=id)

  projects = Project.objects.all().order_by('-pub_date')

  return render(request, 'project/myprojects.html', {'projects': projects, 'profile': profile})


@login_required(login_url='/accounts/login/')
def home(request):

  id = request.user.id
  profile = Profile.objects.get(user=id)
  projects = Project.objects.all().order_by('-pub_date')
  return render(request, 'index.html', {'projects': projects,'profile': profile})


@login_required(login_url='/accounts/login/')
def search_results(request):
    current_user = request.user
    profile = Profile.objects.get(username=current_user)
    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Project.search_project(search_term)
        message = f"{search_term}"

        print(searched_projects)

    return render(request,'search.html',{"message":message,"projects":searched_projects,"profile":profile})

@login_required(login_url='/accounts/login/')
def project(request, id):
  user = request.user.id
  profile = Profile.objects.get(user=user)
  project = Project.objects.get(pk=id)
  ratings = Rating.objects.filter(project=id)

  
  project = Project.objects.get(pk=id)

  a = Rating.objects.filter(project=id).aggregate(Avg('design'))
  b = Rating.objects.filter(project=id).aggregate(Avg('usability'))
  c = Rating.objects.filter(project=id).aggregate(Avg('content'))
  d = Rating.objects.filter(project=id).aggregate(Avg('average'))
  


  return render(request, 'project/project.html',{'profile':profile,'project':project,'ratings':ratings,'a':a,'b':b,'c':c,'d':d})

@login_required(login_url='/accounts/login/')
def newproject(request):
  user = request.user.id
  profile = Profile.objects.get(user=user)
  current_user = request.user
  current_username = request.user.username

  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.poster = current_user
      project.postername = current_username
      project.save()
    return redirect('home')

  else:
    form = ProjectForm()
  return render(request, 'project/newproject.html',{'form':form,'profile':profile})

@login_required(login_url='/accounts/login/')
def password(request):
  id = request.user.id
  profile = Profile.objects.get(user=id)
  return render(request, 'password.html',{'profile':profile})

