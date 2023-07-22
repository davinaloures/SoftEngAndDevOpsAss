

# Create your tests here.
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engagement_webapp.settings')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'engagement_webapp.settings'
django.setup()
from django.contrib.auth.models import User
from django.test import TestCase

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
    



    '''def test_password_reset(self):
        response = self.client.post('/password_reset/', {'email': 'louresdavina@gmail.com'}) #replace with email address    
        self.assertRedirects(response, '/password_reset/done/')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].to, ['louresdavina@gmail.com']) #replace with email address'''


        




