from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url('',views.home,name = 'home'),
    url(r'^profile/(\d+)', views.profile, name='profile'),
    url(r'^new/profile$',views.newprofile, name='newprofile'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)