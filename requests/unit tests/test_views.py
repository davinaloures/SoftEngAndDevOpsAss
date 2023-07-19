from django.test import TestCase, Client
from django.urls import reverse
from requests.models import Post
from .test_setup import TestSetUp


class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res=self.client.post(self.register_url)
        self.assertEqual(res.status_code, 200)

    def test_user_can_register_successfully(self):
        res=self.client.post(
            self.register_url, self.user_data, format="json")
       # self.assertEqual(res.data['email'], self.user_data['email'])
      #  self.assertEqual(res.data['username'], self.user_data['username'])
       # self.assertEqual(res.status_code, 201)
            