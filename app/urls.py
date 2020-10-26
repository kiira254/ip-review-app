from django.conf.urls import url,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^new/profile$',views.newprofile, name='newprofile'),
    url(r'^profile/(\d+)', views.profile, name='profile'),
    url(r'^search/',views.search_results, name='search_results'),
    url(r'^project$', views.project, name='project'),
    url(r'^new/project$',views.newproject, name='newproject'),
    url(r'^myprojects/', views.myprojects, name='myprojects'),
    url(r'^password/', views.password, name='password'),
    url(r'^site/(\d+)',views.site,name='site'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)