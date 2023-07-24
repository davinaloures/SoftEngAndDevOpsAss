from datetime import timedelta
from importlib import import_module
from time import sleep

from django.contrib.auth import get_user_model, login, logout
from django.http import HttpRequest
from django.test import override_settings, TestCase
from django.urls import reverse

from axes.conf import settings
from axes.helpers import get_cache, make_cache_key_list, get_cool_off, get_failure_limit
from axes.models import AccessAttempt
from requests.unit_tests.base import AxesTestCase


class DjangoLoginTestCase(TestCase):
    def setUp(self):
        engine = import_module(settings.SESSION_ENGINE)

        self.request = HttpRequest()
        self.request.session = engine.SessionStore()

        self.username = "john.doe"
        self.password = "hunter2"

        self.user = get_user_model().objects.create(username=self.username, is_staff=True)
        self.user.set_password(self.password)
        self.user.save()
        self.user.backend = "django.contrib.auth.backends.ModelBackend"


class DjangoContribAuthLoginTestCase(DjangoLoginTestCase):
    def test_login(self):
        login(self.request, self.user)

    def test_logout(self):
        login(self.request, self.user)
        logout(self.request)


@override_settings(AXES_ENABLED=False)
class DjangoTestClientLoginTestCase(DjangoLoginTestCase):
    def test_client_login(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

    def test_client_logout(self):
        self.client.login(username=self.username, password=self.password)
        self.client.logout()
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)

    def test_client_force_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)


class DatabaseLoginTestCase(AxesTestCase):
    """
    Test for lockouts under different configurations and circumstances to prevent false positives and false negatives.

    Always block attempted logins for the same user from the same IP.
    Always allow attempted logins for a different user from a different IP.
    """

    IP_1 = "10.1.1.1"
    IP_2 = "10.2.2.2"
    IP_3 = "10.2.2.3"
    USER_1 = "valid-user-1"
    USER_2 = "valid-user-2"
    USER_3 = "valid-user-3"
    EMAIL_1 = "valid-email-1@example.com"
    EMAIL_2 = "valid-email-2@example.com"

    VALID_USERNAME = USER_1
    VALID_EMAIL = EMAIL_1
    VALID_PASSWORD = "valid-password"

    VALID_IP_ADDRESS = IP_1

    WRONG_PASSWORD = "wrong-password"
    LOCKED_MESSAGE = "Account locked: too many login attempts."
    LOGIN_FORM_KEY = '<input type="submit" value="Log in" />'
    ATTEMPT_NOT_BLOCKED = 200
    ALLOWED = 302
    BLOCKED = 429

    def _login(self, username, password, ip_addr="127.0.0.1", user_agent="test-browser", **kwargs):
        """
        Login a user and get the response.

        IP address can be configured to test IP blocking functionality.
        """

        post_data = {"username": username, "password": password}

        post_data.update(kwargs)

        return self.client.post(
            reverse("admin:login"),
            post_data,
            REMOTE_ADDR=ip_addr,
            HTTP_USER_AGENT=user_agent,
        )

    def _lockout_user_from_ip(self, username, ip_addr, user_agent="test-browser"):
        for _ in range(settings.AXES_FAILURE_LIMIT):
            response = self._login(
                username=username, password=self.WRONG_PASSWORD, ip_addr=ip_addr, user_agent=user_agent,
            )
        return response

    def _lockout_user1_from_ip1(self):
        return self._lockout_user_from_ip(username=self.USER_1, ip_addr=self.IP_1)
