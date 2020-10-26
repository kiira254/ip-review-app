from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
import datetime as dt
from .models import Profile, Project, Rating
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, ProfileForm, ProjectForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

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
def password(request):
  id = request.user.id
  profile = Profile.objects.get(user=id)
  return render(request, 'password.html',{'profile':profile})


@login_required(login_url='/accounts/login/')
def profile(request):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)
  user = request.user
  projects = Project.objects.filter(poster=frank).order_by('-pub_date')
  projectcount = projects.count()
  return render(request, 'profile/profile.html', {'profile': profile, 'user': user, 'projectcount': projectcount, 'projects': projects})

@login_required(login_url='/accounts/login/')
def newprofile(request,):
  id = request.user.id
  profile = Profile.objects.get(user=id)
  frank = request.user.id
  profile = Profile.objects.get(user=frank)
  user = request.user
  projects = Project.objects.filter(poster=frank).order_by('-pub_date')
  projectcount = projects.count()

  if request.method == 'POST':
    instance = get_object_or_404(Profile, user=id)
    form = ProfileForm(request.POST, request.FILES,instance=instance)
    if form.is_valid():
      form.save()
    return redirect('profile', id)

  else:
    form = ProfileForm()

  return render(request, 'profile/new_profile.html',{'form':form,'profile':profile, 'user': user, 'projectcount': projectcount, 'projects': projects})

@login_required(login_url='/accounts/login/')
def myprojects(request):
  id = request.user.id
  profile = Profile.objects.get(user=id)

  projects = Project.objects.all().order_by('-pub_date')

  return render(request, 'project/myprojects.html', {'projects': projects, 'profile': profile})


# @login_required(login_url='/accounts/login/')
# def home(request):

#   id = request.user.id
#   profile = Profile.objects.get(user=id)
#   project=Project.save_project()
#   return render(request, 'index.html', {'profile': profile, project:'project'})


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
def home (request):
  id = request.user.id
  user = request.user.id
  profile = Profile.objects.get(user=user)
  project = Project.objects.get(pk=id)
  # ratings = Rating.objects.filter(project=id)

  
  # project = Project.objects.get(pk=id)

  # a = Rating.objects.filter(project=id).aggregate(Avg('design'))
  # b = Rating.objects.filter(project=id).aggregate(Avg('usability'))
  # c = Rating.objects.filter(project=id).aggregate(Avg('content'))
  # d = Rating.objects.filter(project=id).aggregate(Avg('average'))
  


  return render(request, 'index.html',{'profile':profile,'project':project})

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

# @login_required(login_url='/accounts/login/')
# def rating (request,id):
#   user = request.user.id
#   profile = Profile.objects.get(user=user)
#   id = id
#   current_username = request.user.username

#   if request.method == 'POST':
#     form = RatingForm(request.POST)
#     if form.is_valid():
#       rating = form.save(commit=False)

#       design_rating = form.cleaned_data['design']
#       usability_rating = form.cleaned_data['usability']
#       content_rating = form.cleaned_data['content']

#       avg = ((design_rating + usability_rating + content_rating)/3)

#       rating.average = avg
#       rating.postername = current_username
#       rating.project = Project.objects.get(pk=id)

#       rating.save()
#     return redirect('project',id)

#   else:
#     form = RatingForm()
#   return render(request, 'rating.html',{'form':form,'profile':profile,'id':id})

@login_required(login_url='/accounts/login/')
def site(request,site_id):
    current_user = request.user
    profile =Profile.objects.get(username=current_user)

    try:
        project = Project.objects.get(id=site_id)
    except:
        raise ObjectDoesNotExist()

    try:
        ratings = Rating.objects.filter(project_id=site_id)
        design = Rating.objects.filter(project_id=site_id).values_list('design',flat=True)
        usability = Rating.objects.filter(project_id=site_id).values_list('usability',flat=True)
        creativity = Rating.objects.filter(project_id=site_id).values_list('creativity',flat=True)
        content = Rating.objects.filter(project_id=site_id).values_list('content',flat=True)
        total_design=0
        total_usability=0
        total_creativity=0
        total_content = 0
        print(design)
        for rate in design:
            total_design+=rate
        print(total_design)

        for rate in usability:
            total_usability+=rate
        print(total_usability)

        for rate in creativity:
            total_creativity+=rate
        print(total_creativity)

        for rate in content:
            total_content+=rate
        print(total_content)

        overall_score=(total_design+total_content+total_usability+total_creativity)/4

        print(overall_score)

        project.design = total_design
        project.usability = total_usability
        project.creativity = total_creativity
        project.content = total_content
        project.overall_score = overall_score

        project.save()

    except:
        return None

    if request.method =='POST':
        form = RatingForm(request.POST,request.FILES)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.project= project
            rating.profile = profile
            rating.overall_score = (rating.design+rating.usability+rating.creativity+rating.content)/2
            rating.save()
    else:
        form = RatingForm()

    return render(request,"rating.html",{"project":project,"profile":profile,"ratings":ratings,"form":form})
