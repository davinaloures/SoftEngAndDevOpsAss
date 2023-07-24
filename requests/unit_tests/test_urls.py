from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import register, profile
from requests.views import PostCreateView

#unit tests for urls - checking if urls are resolved

class TestUrls(SimpleTestCase):
    def test_register_url_is_resolved(self):
        url= reverse('register')
        print(resolve(url))
        self.assertEquals(resolve(url).func, register)

    def test_profile_url_is_resolved(self):
        url= reverse('profile')
        print(resolve(url))
        self.assertEquals(resolve(url).func, profile)
