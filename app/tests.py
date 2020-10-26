from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Profile, Project, Rating


class ProfileTestClass(TestCase):
  """  
  Test class that tests profile
  """
  def setUp(self):
    self.prof =Profile(profpic='test.jpg', bio='test bio', contact='cchelangat16@gmail.com',user=1)

  def test_instance(self):
      self.assertTrue(isinstance(self.prof, Profile))

  def test_save_method(self):
      """
      Function to test that profile is being saved
      """
      self.prof.save_profile()
      profiles = Profile.objects.all()
      self.assertTrue(len(profiles) > 0)

  def test_delete_method(self):
      """
      Function to test that a profile can be deleted
      """
      self.prof.save_profile()
      self.prof.delete_profile()
      profiles = Profile.objects.all()
      self.assertTrue(len(profiles) == 0)

class ProjecTestClass(TestCase):
  """  
  Tests Project class and its functions
  """

  def test_instance(self):
      self.assertTrue(isinstance(self.project, Project))

  def test_save_method(self):
      """
      Testing whether a new project is being saved
      """
      self.project.save_project()
      projects = Project.objects.all()
      self.assertTrue(len(projects) > 0)

  def test_delete_method(self):
      """
      Function to test that a project can be deleted
      """
      self.project.save_project()
      self.project.delete_project()
      projects = Project.objects.all()
      self.assertTrue(len(projects) == 0)