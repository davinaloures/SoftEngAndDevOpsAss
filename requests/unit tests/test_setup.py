from django.test import TestCase
from django.urls import reverse
import users
import requests
import engagement_webapp
packages= ['users', 'requests', 'engagement_webapp']
class TestSetUp(TestCase):

    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')

        self.user_data={
            'email':"email@gmail.com",
            'username':"username",
            'password':"password",
        }

        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
