from django.test import TestCase
from django.conf import settings
from django.core import mail

from webbook.models import User

import re

SIGNUP_CONFIRMATION_LINK=r'(http:\/\/.*\/account\/signup\/.*\/.*\/)'
RESET_REQUEST_LINK=r'(http:\/\/.*\/account\/password_reset\/.*\/.*\/)'
MAX_POSITIVE_INTEGER_FIELD_VALUE = 2147483647

_EMAIL = "toto@toto.fr"
_PASSWORD = "tototititutu"
_FIRST_NAME = "Toto"
_LAST_NAME = "Titi"
_COMPANY = "Tutu"

_SIGNUP_URL = "/account/signup/"
_LOGIN_URL = f"{settings.LOGIN_URL}/"
_LOGOUT_URL = f"{settings.LOGOUT_URL}/"
_PASSWORD_CHANGE_URL = "/account/password_change/"
_PASSWORD_RESET_URL = "/account/password_reset/"

class SignUpView(TestCase):
    """
        Check Request Account Creation:
        - Valid creation
        - User already exist
    """
    def test_user_creation(self):
        response = self.client.post(
            _SIGNUP_URL, data={
                "email": _EMAIL,
                "password1": _PASSWORD,
                "password2": _PASSWORD,
                "last_name": _LAST_NAME,
                "first_name": _FIRST_NAME,
                "company": _COMPANY})
        self.assertEqual(response.url, "/account/signup/done/", "Invalid response url")
        self.assertEqual(User.objects.all().count(), 1, "UserForm has not been created after submit valid form !")
        l_user = User.objects.get(email=_EMAIL)
        self.assertEqual(l_user.email, _EMAIL)
        self.assertEqual(l_user.first_name, _FIRST_NAME)
        self.assertEqual(l_user.last_name, _LAST_NAME)
        self.assertEqual(l_user.company, _COMPANY)
        self.assertEqual(l_user.groups.count(), 0)
        self.assertEqual(l_user.user_permissions.count(), 0)
        self.assertFalse(l_user.is_staff)
        self.assertFalse(l_user.is_active)
        self.assertFalse(l_user.is_superuser)

    def test_user_already_exist(self):
        response = self.client.post(
            _SIGNUP_URL, data={  "email": _EMAIL,
                                        "password1": _PASSWORD,
                                        "password2": _PASSWORD,
                                        "last_name": _LAST_NAME,
                                        "first_name": _FIRST_NAME,
                                        "company": _COMPANY})
        self.assertEqual(response.url, "/account/signup/done/", "Invalid response url")
        self.assertEqual(User.objects.all().count(), 1, "UserForm has not been created after submit valid form !")
        # User already exist
        response = self.client.post(
            _SIGNUP_URL, data={  "email": _EMAIL,
                                        "password1": _PASSWORD,
                                        "password2": _PASSWORD,
                                        "last_name": _LAST_NAME,
                                        "first_name": _FIRST_NAME,
                                        "company": _COMPANY})
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        self.assertEqual(User.objects.all().count(), 1, "UserForm has been created after submit invalid form !")


class SignUpConfirmationView(TestCase):
    """
        Check SignUp Confirmation View when url send via email has been clicked
    """
    def setUp(self):
        """
            Call SignUpView
        """
        self.client.post(
            _SIGNUP_URL, data={  "email": _EMAIL,
                                        "password1": _PASSWORD,
                                        "password2": _PASSWORD,
                                        "last_name": _LAST_NAME,
                                        "first_name": _FIRST_NAME,
                                        "company": _COMPANY})


    def test_valid(self):
        """
            Test SignUp Confirmation View Read email to find validation link and clicked on it
        """
        # Check and Read Email
        self.assertEqual(len(mail.outbox), 1, "No Email received with confirmation link !")
        self.assertEqual(mail.outbox[0].to[0], _EMAIL, "Invalid destination email !")
        l_re = re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body)
        self.assertIsNotNone(l_re, "No Confirmation Link find in the email !")
        l_confirmation_link = l_re.group(0)

        # Click on Email
        response = self.client.get(l_confirmation_link)

        # Checks Behavior
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        self.assertEqual(len(mail.outbox), 2, "No confirmation mail has been received")
        l_user = User.objects.get(email=_EMAIL)
        self.assertTrue(l_user.is_active, "Account has not been activated after clicking on link !")


class LoginView(TestCase):
    """
        Testing Login View with valid and invalid information
    """
    def setUp(self):
        """
            Creation and Activation of an account and Logout
        """
        self.client.post(
            _SIGNUP_URL, data={  "email": _EMAIL,
                                        "password1": _PASSWORD,
                                        "password2": _PASSWORD,
                                        "last_name": _LAST_NAME,
                                        "first_name": _FIRST_NAME,
                                        "company": _COMPANY})
        self.assertEqual(len(mail.outbox), 1, "SetUp Invalid !")
        l_re = re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body)
        l_confirmation_link = l_re.group(0)
        self.client.get(l_confirmation_link)
        self.assertEqual(User.objects.all().count(), 1, "SetUp Invalid !")
        self.assertTrue(User.objects.get(email=_EMAIL).is_active, "SetUp Invalid !")
        self.assertEqual(self.client.get(_LOGOUT_URL).url, settings.LOGIN_REDIRECT_URL, f"SetUp Invalid !")
        self.assertFalse(self.client.get('/').context['user'].is_authenticated, "SetUp Invalid !")

    def test_valid(self):
        """
            Test LoginView is working
        """
        response = self.client.post(
            _LOGIN_URL, {   'username': _EMAIL,
                            'password': _PASSWORD })
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}' !")
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, _EMAIL, "User Authentificated not expected !")

    def test_invalid_email(self):
        """
            Test with an invalid email:
            - empty email
            - not an email
            - email does not exist
        """
        response = self.client.post(
            _LOGIN_URL, {   'email': '',
                            'password': _PASSWORD })
        self.assertFalse(response.context['user'].is_authenticated, "User is authentificated !")


        response = self.client.post(
            _LOGIN_URL, {   'email': 'titi',
                            'password': _PASSWORD })
        self.assertFalse(response.context['user'].is_authenticated, "User is authentificated !")


        response = self.client.post(
            _LOGIN_URL, {   'email': 'titi@gmail.com',
                            'password': _PASSWORD })
        self.assertFalse(response.context['user'].is_authenticated, "User is authentificated !")


    def test_invalid_password(self):
        """
            Test with an invalid password:
            - empty
            - wrong password
        """
        response = self.client.post(
            _LOGIN_URL, {   'email': _EMAIL,
                            'password': '' })
        self.assertFalse(response.context['user'].is_authenticated, "User is not authentificated !")

        response = self.client.post(
            _LOGIN_URL, {   'email': _EMAIL,
                            'password': 'titi' })
        self.assertFalse(response.context['user'].is_authenticated, "User is not authentificated !")


class PasswordChangeView(TestCase):
    _NEW_PASSWORD = "tytytutu"

    def setUp(self):
        """
            Creation and Activation of an account
            Cleaning Email
        """
        self.client.post(
            _SIGNUP_URL, data={
                "email": _EMAIL,
                "password1": _PASSWORD,
                "password2": _PASSWORD,
                "last_name": _LAST_NAME,
                "first_name": _FIRST_NAME,
                "company": _COMPANY})
        l_re = re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body)
        l_confirmation_link = l_re.group(0)
        self.client.get(l_confirmation_link)
        self.assertEqual(User.objects.all().count(), 1, "SetUp Invalid !")
        self.assertTrue(User.objects.get(email=_EMAIL).is_active, "SetUp Invalid !")
        mail.outbox.clear()

    def test_valid(self):
        """
            Test PasswordChangeView
        """
        response = self.client.post(
            _PASSWORD_CHANGE_URL, data={
                'old_password': _PASSWORD,
                'new_password1': self._NEW_PASSWORD,
                'new_password2': self._NEW_PASSWORD })
        self.assertEqual(response.status_code, 302, "No Code 200 page return")
        self.assertEqual(response.url, "/account/password_change/done")
        self.assertEqual(len(mail.outbox), 1)

    def test_invalid_password(self):
        """
            Test PasswordChangeView with different password
        """
        response = self.client.post(
            _PASSWORD_CHANGE_URL, data={
                'old_password': _PASSWORD,
                'new_password1': self._NEW_PASSWORD,
                'new_password2': f"{self._NEW_PASSWORD}0" })
        self.assertEqual(response.status_code, 200, "No Code 200 page return")

    def test_with_no_authentification(self):
        """
            Test PasswordChangeView without be authentificate
            Redirect to LogIn View
        """
        # SetUp
        self.assertEqual(self.client.get(_LOGOUT_URL).url, settings.LOGIN_REDIRECT_URL, f"Impossible to LogOut !")
        self.assertFalse(self.client.get('/').context['user'].is_authenticated, "Authentification has not been logout !")
        # Test
        response = self.client.post(
            _PASSWORD_CHANGE_URL, data={
                'old_password': _PASSWORD,
                'new_password1': self._NEW_PASSWORD,
                'new_password2': self._NEW_PASSWORD })
        self.assertEqual(response.status_code, 302, "No Code 302 page return")
        self.assertEqual(response.url, f"{settings.LOGIN_URL}?next={_PASSWORD_CHANGE_URL}")

class PasswordResetView(TestCase):
    def setUp(self):
        """
            Creation and Activation of an account, Logout, clean mail box
        """
        self.client.post(
            _SIGNUP_URL, data={
                "email": _EMAIL,
                "password1": _PASSWORD,
                "password2": _PASSWORD,
                "last_name": _LAST_NAME,
                "first_name": _FIRST_NAME,
                "company": _COMPANY})
        l_re = re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body)
        l_confirmation_link = l_re.group(0)
        self.client.get(l_confirmation_link)
        self.assertEqual(User.objects.all().count(), 1, "SetUp Invalid !")
        self.assertTrue(User.objects.get(email=_EMAIL).is_active, "SetUp Invalid !")
        self.assertEqual(self.client.get(_LOGOUT_URL).url, settings.LOGIN_REDIRECT_URL, f"SetUp Invalid !")
        self.assertFalse(self.client.get('/').context['user'].is_authenticated, "SetUp Invalid !")
        mail.outbox.clear()

    def test_valid(self):
        """
            Check that action is possible
        """
        response = self.client.post(
            _PASSWORD_RESET_URL, { 'email': _EMAIL })
        self.assertEqual(response.url, "/account/password_reset/done/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 1, "Email has not been received !")

    def test_with_authentification(self):
        """
            Check that action is not possible with a current authentification
        """
        response = self.client.post(
            _LOGIN_URL, {   'username': _EMAIL,
                            'password': _PASSWORD })
        self.assertEqual(response.status_code, 302, "Expected a redirect page")
        self.assertEqual(response.url, "/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 0, "Email has been send !")

    def test_with_unknown_user(self):
        """
            Check the behavior is the same as exist one but without sending mail
        """
        response = self.client.post(
            _PASSWORD_RESET_URL, { 'email': "titi@gmail.com" })
        self.assertEqual(response.url, "/account/password_reset/done/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 0, "Email has been send !")


class PasswordResetConfirmView(TestCase):
    def setUp(self):
        """
            Creation and Activation of an account, Logout, clean mailbox and request PasswordReset
        """
        self.client.post(
            _SIGNUP_URL, data={
                "email": _EMAIL,
                "password1": _PASSWORD,
                "password2": _PASSWORD,
                "last_name": _LAST_NAME,
                "first_name": _FIRST_NAME,
                "company": _COMPANY})
        l_re = re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body)
        l_confirmation_link = l_re.group(0)
        self.client.get(l_confirmation_link)
        self.assertEqual(User.objects.all().count(), 1, "SetUp Invalid !")
        self.assertTrue(User.objects.get(email=_EMAIL).is_active, "SetUp Invalid !")
        self.assertEqual(self.client.get(_LOGOUT_URL).url, settings.LOGIN_REDIRECT_URL, f"SetUp Invalid !")
        self.assertFalse(self.client.get('/').context['user'].is_authenticated, "SetUp Invalid !")
        mail.outbox.clear()
        self.client.post(_PASSWORD_RESET_URL, { 'email': _EMAIL })


    def test_valid(self):
        """
            Check Email Url
        """
        self.assertEqual(len(mail.outbox), 1, "Email has not been received !")
        l_re = re.search(RESET_REQUEST_LINK, mail.outbox[0].body)
        self.assertIsNotNone(l_re, "Impossible to find reset link in email !")
        l_confirmation_link = l_re.group(0)
        response = self.client.get(l_confirmation_link)
        self.assertEqual(response.status_code, 302, "Expected redirection page to reset password !")
        response = self.client.post(response.url, data={
            'new_password1': _PASSWORD,
            'new_password2': _PASSWORD })
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(response.url, "/account/password_reset/complete/", f"Redirection not exist in response '{response}'")

# -----------------------------
class PasswordResetDoneViewTestCase(TestCase):
    """
        Nothing to test it is just a Django View that is showing a template
    """
    pass
