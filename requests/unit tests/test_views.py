from django.test import TestCase, Client
from django.urls import reverse
from requests.models import Post
from .test_setup import TestSetUp


class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res=self.client.post(self.register_url)
        self.assertEqual(res.status_code, 200)

    


   # def test_user_can_register_successfully(self):
    #    res=self.client.post(self.register_url, self.user_data, format='text/html')
     #   self.assertEqual(res.status_code, 200)
      #  self.assertRedirects(res, self.login_url, status_code=200, target_status_code=200, fetch_redirect_response=True)

    def test_user_cannot_login_with_unregistered_email(self):
        res=self.client.post(self.login_url, self.user_data, format='text/html')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'users/login.html')
        self.assertFalse(res.context['user'].is_authenticated)    
    
    #test that password1 and password2 match when registering a user
#def test_passwords_match_when_registering(self):
  #      res=self.client.post(self.register_url, self.user_data, format='text/html')
  #      self.assertEqual(res.status_code, 200)
   #     self.assertRedirects(res, self.login_url, status_code=200, target_status_code=200, fetch_redirect_response=True)
    #    self.assertEqual(self.user_data['password'], self.user_data['password2'])







