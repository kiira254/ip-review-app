from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Profile, Project, Rating


class ProfileTestClass(TestCase):

  def setUp(self):
    self.profile =Profile(profile_photo='test.jpg', bio='test bio', contact='nkamotho69@gmail.com',user_id=1)

  def test_instance(self):
      self.assertTrue(isinstance(self.profile, Profile))

  def test_save_method(self):
     
      self.profile.save_profile()
      profiles = Profile.objects.all()
      self.assertTrue(len(profiles) > 0)

  def test_delete_method(self):
      
      self.profile.save_profile()
      self.profile.delete_profile()
      profiles = Profile.objects.all()
      self.assertTrue(len(profiles) == 0)

class ProjecTestClass(TestCase):
  def setUp(self):
    self.project =Project(title='test',image='test.jpg', description='test description', link='htt//.test')
  
  def test_instance(self):
      self.assertTrue(isinstance(self.project, Project))

  def test_save_method(self):
      
      self.project.save_project()
      projects = Project.objects.all()
      self.assertTrue(len(projects) > 0)

  def test_delete_method(self):
      
      self.project.save_project()
      self.project.delete_project()
      projects = Project.objects.all()
      self.assertTrue(len(projects) == 0)