from django.test import TestCase
from django.conf import settings

from webbook.models import User
from webbook.forms import PublicUserForm#, AdminUserForm

# Token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from webbook.views import account_activation_token

MAX_POSITIVE_INTEGER_FIELD_VALUE = 2147483647

class UserModelTestCase(TestCase):
    def setUp(self):
        self.email = "toto@toto.fr"
        self.password = "tototititutu" 
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.is_staff = True
        self.is_active = False
        self.is_superuser = True
        self.nl0 = MAX_POSITIVE_INTEGER_FIELD_VALUE
        self.nl1 = MAX_POSITIVE_INTEGER_FIELD_VALUE
        self.nl2 = MAX_POSITIVE_INTEGER_FIELD_VALUE
        self.nl3 = MAX_POSITIVE_INTEGER_FIELD_VALUE
        self.nl4 = MAX_POSITIVE_INTEGER_FIELD_VALUE
        self.nl5 = MAX_POSITIVE_INTEGER_FIELD_VALUE
        self.nl6 = MAX_POSITIVE_INTEGER_FIELD_VALUE
        self.nl7 = MAX_POSITIVE_INTEGER_FIELD_VALUE

    def test_minimal_construction(self):
        l_user = User.objects.create(email=self.email, password=self.password)
        self.assertEqual(l_user.email, self.email, "[LOCAL] email invalid !")
        self.assertEqual(l_user.password, self.password, "[LOCAL] password invalid !")
        self.assertEqual(l_user.first_name, "", "[LOCAL] first_name invalid !")
        self.assertEqual(l_user.last_name, "", "[LOCAL] last_name invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[LOCAL] Groups already exist !")
        self.assertEqual(l_user.user_permissions.count(), 0, "[LOCAL] User_Permissions already exist !")
        self.assertFalse(l_user.is_staff, "[LOCAL] is_staff is not False !")
        self.assertTrue(l_user.is_active, "[LOCAL] is_active is not True !")
        self.assertFalse(l_user.is_superuser, "[LOCAL] is_super_user is not False !")
        self.assertEqual(l_user.nl0, 1)
        self.assertEqual(l_user.nl1, 0)
        self.assertEqual(l_user.nl2, 0)
        self.assertEqual(l_user.nl3, 0)
        self.assertEqual(l_user.nl4, 0)
        self.assertEqual(l_user.nl5, 0)
        self.assertEqual(l_user.nl6, 0)
        self.assertEqual(l_user.nl7, 0)

    def test_minimal_construction_database(self):
        User.objects.create(email=self.email, password=self.password)
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created !")
        l_user = User.objects.get(email=self.email)
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.password, self.password, "[DB] password invalid !")
        self.assertEqual(l_user.first_name, "", "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, "", "[DB] last_name invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertFalse(l_user.is_staff, "[DB] is_staff is not False !")
        self.assertTrue(l_user.is_active, "[DB] is_active is not True !")
        self.assertFalse(l_user.is_superuser, "[DB] is_super_user is not False !")
        self.assertEqual(l_user.nl0, 1)
        self.assertEqual(l_user.nl1, 0)
        self.assertEqual(l_user.nl2, 0)
        self.assertEqual(l_user.nl3, 0)
        self.assertEqual(l_user.nl4, 0)
        self.assertEqual(l_user.nl5, 0)
        self.assertEqual(l_user.nl6, 0)
        self.assertEqual(l_user.nl7, 0)


    def test_constructor(self):
        l_user = User.objects.create(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            is_staff=self.is_staff,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            nl0=self.nl0,
            nl1=self.nl1,
            nl2=self.nl2,
            nl3=self.nl3,
            nl4=self.nl4,
            nl5=self.nl5,
            nl6=self.nl6,
            nl7=self.nl7)
        self.assertEqual(l_user.email, self.email, "[LOCAL] email invalid !")
        self.assertEqual(l_user.password, self.password, "[LOCAL] password invalid !")
        self.assertEqual(l_user.first_name, self.first_name, "[LOCAL] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[LOCAL] last_name invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[LOCAL] Groups already exist !")
        self.assertEqual(l_user.user_permissions.count(), 0, "[LOCAL] User_Permissions already exist !")
        self.assertTrue(l_user.is_staff, "[LOCAL] is_staff is not True !")
        self.assertFalse(l_user.is_active, "[LOCAL] is_active is not False !")
        self.assertTrue(l_user.is_superuser, "[LOCAL] is_super_user is not True !")
        self.assertEqual(l_user.nl0, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl1, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl2, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl3, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl4, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl5, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl6, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl7, MAX_POSITIVE_INTEGER_FIELD_VALUE)

    def test_constructor_database(self):
        User.objects.create(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            is_staff=self.is_staff,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            nl0=self.nl0,
            nl1=self.nl1,
            nl2=self.nl2,
            nl3=self.nl3,
            nl4=self.nl4,
            nl5=self.nl5,
            nl6=self.nl6,
            nl7=self.nl7)
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created !")
        l_user = User.objects.get(email=self.email)
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.password, self.password, "[DB] password invalid !")
        self.assertEqual(l_user.first_name, self.first_name, "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[DB] last_name invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertTrue(l_user.is_staff, "[DB] is_staff is not True !")
        self.assertFalse(l_user.is_active, "[DB] is_active is not False !")
        self.assertTrue(l_user.is_superuser, "[DB] is_super_user is not True !")
        self.assertEqual(l_user.nl0, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl1, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl2, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl3, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl4, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl5, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl6, MAX_POSITIVE_INTEGER_FIELD_VALUE)
        self.assertEqual(l_user.nl7, MAX_POSITIVE_INTEGER_FIELD_VALUE)

class PublicUserFormTestCase(TestCase):
    def setUp(self):
        self.email = "toto@toto.fr"
        self.password = "tototititutu" 
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = "Tutu"

    def test_userform_valid(self):
        l_user = PublicUserForm(data={  'email': self.email,
                                        'password': self.password,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertTrue(l_user.is_valid(), "Form is not valid !")
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        l_user.save()
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created after save form !")
        l_user = User.objects.get(email=self.email)
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.password, self.password, "[DB] password invalid !")
        self.assertEqual(l_user.first_name, self.first_name, "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[DB] last_name invalid !")
        self.assertEqual(l_user.company, self.company, "[DB] company invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertFalse(l_user.is_staff, "[DB] is_staff is not False !")
        self.assertTrue(l_user.is_active, "[DB] is_active is not True !")
        self.assertFalse(l_user.is_superuser, "[DB] is_super_user is not False !")

    def test_userform_constructor_error_email(self):
        l_user = PublicUserForm(data={  'email': "toto",
                                        'password': self.password,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "Enter a valid email address.", "Error message not expected !")

        l_user = PublicUserForm(data={  'email': "toto@titi",
                                        'password': self.password,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "Enter a valid email address.", "Error message not expected !")

    def test_userform_constructor_error_email_exist(self):
        l_user = PublicUserForm(data={  'email': self.email,
                                        'password': self.password,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertTrue(l_user.is_valid(), "Form is not valid !")
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        l_user.save()
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created after save form !")

        l_user = PublicUserForm(data={  'email': self.email,
                                        'password': self.password,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 1, "Expected only 1 errors !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "User with this Email address already exists.", "Error message not expected !")

    def test_userform_not_valid_only_email(self):
        l_user = PublicUserForm(data={'email': self.email})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 4, "Expected only 5 errors !")
        self.assertEqual(len(l_user['password'].errors), 1, "Expected only 1 error for 'password' field !")
        self.assertEqual(l_user['password'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['last_name'].errors), 1, "Expected only 1 error for 'last_name' field !")
        self.assertEqual(l_user['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['first_name'].errors), 1, "Expected only 1 error for 'first_name' field !")
        self.assertEqual(l_user['first_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['company'].errors), 1, "Expected only 1 error for 'company' field !")
        self.assertEqual(l_user['company'].errors[0], "This field is required.", "Error message not expected !")

    def test_userform_not_valid_no_data(self):
        l_user = PublicUserForm(data={})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 5, "Expected only 5 errors !")
        self.assertEqual(len(l_user['password'].errors), 1, "Expected only 1 error for 'password' field !")
        self.assertEqual(l_user['password'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['last_name'].errors), 1, "Expected only 1 error for 'last_name' field !")
        self.assertEqual(l_user['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['first_name'].errors), 1, "Expected only 1 error for 'first_name' field !")
        self.assertEqual(l_user['first_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['company'].errors), 1, "Expected only 1 error for 'company' field !")
        self.assertEqual(l_user['company'].errors[0], "This field is required.", "Error message not expected !")


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.email = "toto@gmail.com"
        self.password = "tototititutu"
        User.objects.create_user(email=self.email, password=self.password)

    def test_authentificated_account_home(self):
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/login/", {    'username': self.email,
                                    'password': self.password })
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 200, "No Error 200 page for access authentificated to account homepage !")

    def test_anonymous_account_home(self):
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 302, "No Error 302 page for access anonymously to account homepage !")
        self.assertEqual(response.url, "/account/login?next=/account/", "Incorrect url for access anonymously to account homepage !")


class SignUpView(TestCase):
    def setUp(self):
        self.email = "toto@toto.fr"
        self.password = "tototititutu" 
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = "Tutu"

    def test_valid_new_user_creation(self):
        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        l_user = User.objects.get(email=self.email)
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.first_name, self.first_name, "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[DB] last_name invalid !")
        self.assertEqual(l_user.company, self.company, "[DB] company invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertFalse(l_user.is_staff, "[DB] is_staff is not False !")
        self.assertFalse(l_user.is_active, "[DB] is_active is not False !")
        self.assertFalse(l_user.is_superuser, "[DB] is_super_user is not False !")


    def test_user_already_exist_creation(self):
        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")

        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has been created after submit incorrect form !")

class LoginView(TestCase):
    def setUp(self):
        self.email = "toto@gmail.com"
        self.password = "tototititutu"
        User.objects.create_user(email=self.email, password=self.password)

    def test_valid_login(self):
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/login/", {    'username': self.email,
                                    'password': self.password })
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")

    def test_wrong_email(self):
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/login/", {    'email': 'titi@gmail.com',
                                    'password': self.password })
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertFalse(response.context['user'].is_authenticated, "User is not authentificated !")

    def test_wrong_password(self):
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/login/", {    'email': self.email,
                                    'password': 'titi' })
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertFalse(response.context['user'].is_authenticated, "User is not authentificated !")

class ValidationAccount(TestCase):
    def setUp(self):
        self.email = "toto@toto.fr"
        self.password = "tototititutu"
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = "Tutu"

    def test_valid_new_user_creation(self):
        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        l_user = User.objects.get(email=self.email)
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.first_name, self.first_name, "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[DB] last_name invalid !")
        self.assertEqual(l_user.company, self.company, "[DB] company invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertFalse(l_user.is_staff, "[DB] is_staff is not False !")
        self.assertFalse(l_user.is_active, "[DB] is_active is not False !")
        self.assertFalse(l_user.is_superuser, "[DB] is_super_user is not False !")
        uidb64=urlsafe_base64_encode(force_bytes(l_user.pk))
        token=account_activation_token.make_token(l_user)
        self.assertEqual(l_user.pk, int(urlsafe_base64_decode(uidb64)))
        self.assertTrue(account_activation_token.check_token(l_user, token))
        response = self.client.get(f"/account/activation/{uidb64}/{token}/")
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")
        l_user = User.objects.get(email=self.email)
        self.assertTrue(l_user.is_active, "[DB] is_active is not True !")

    def test_invalid_new_user_creation(self):
        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        l_user = User.objects.get(email=self.email)
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.first_name, self.first_name, "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[DB] last_name invalid !")
        self.assertEqual(l_user.company, self.company, "[DB] company invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")        
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertFalse(l_user.is_staff, "[DB] is_staff is not False !")
        self.assertFalse(l_user.is_active, "[DB] is_active is not False !")
        self.assertFalse(l_user.is_superuser, "[DB] is_super_user is not False !")
        uidb64=urlsafe_base64_encode(force_bytes(l_user.pk))
        token=account_activation_token.make_token(l_user)
        self.assertEqual(l_user.pk, int(urlsafe_base64_decode(uidb64)))
        self.assertTrue(account_activation_token.check_token(l_user, token))
        response = self.client.get(f"/account/activation/{uidb64}/toto/")
        self.assertEqual(response.status_code, 404, "No Error 404 page for incorrect activation link token")
        response = self.client.get(f"/account/activation/toto/{token}/")
        self.assertEqual(response.status_code, 404, "No Error 404 page for incorrect activation link uidb64")

