from django.test import TestCase
from django.conf import settings
from django.core import mail

from webbook.models import User
from webbook.forms import PublicUserForm, SignUpForm#, AdminUserForm

import re

SIGNUP_CONFIRMATION_LINK=r'(http:\/\/.*\/account\/signup\/.*\/.*\/)'
RESET_REQUEST_LINK=r'(http:\/\/.*\/account\/password_reset\/.*\/.*\/)'
MAX_POSITIVE_INTEGER_FIELD_VALUE = 2147483647

# -----------------------------
# Models
# -----------------------------
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

# -----------------------------
# Forms
# -----------------------------
class PublicUserFormTestCase(TestCase):
    def setUp(self):
        self.email = "toto@toto.fr"
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = "Tutu"

    def test_userform_valid(self):
        l_user = PublicUserForm(data={  'email': self.email,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertTrue(l_user.is_valid(), "Form is not valid !")
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        l_user.save()
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created after save form !")
        l_user = User.objects.get(email=self.email)
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
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
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "Enter a valid email address.", "Error message not expected !")

        l_user = PublicUserForm(data={  'email': "toto@titi",
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "Enter a valid email address.", "Error message not expected !")

    def test_userform_constructor_error_email_exist(self):
        l_user = PublicUserForm(data={  'email': self.email,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertTrue(l_user.is_valid(), "Form is not valid !")
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        l_user.save()
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created after save form !")

        l_user = PublicUserForm(data={  'email': self.email,
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
        self.assertEqual(len(l_user.errors), 3, "Expected only 5 errors !")
        self.assertEqual(len(l_user['last_name'].errors), 1, "Expected only 1 error for 'last_name' field !")
        self.assertEqual(l_user['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['first_name'].errors), 1, "Expected only 1 error for 'first_name' field !")
        self.assertEqual(l_user['first_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['company'].errors), 1, "Expected only 1 error for 'company' field !")
        self.assertEqual(l_user['company'].errors[0], "This field is required.", "Error message not expected !")

    def test_userform_not_valid_no_data(self):
        l_user = PublicUserForm(data={})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 4, "Expected only 5 errors !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['last_name'].errors), 1, "Expected only 1 error for 'last_name' field !")
        self.assertEqual(l_user['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['first_name'].errors), 1, "Expected only 1 error for 'first_name' field !")
        self.assertEqual(l_user['first_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['company'].errors), 1, "Expected only 1 error for 'company' field !")
        self.assertEqual(l_user['company'].errors[0], "This field is required.", "Error message not expected !")

class AdminUserFormTestCase(TestCase):
    #TODO
    pass

# -----------------------------
class SignUpFormTestCase(TestCase):
    def setUp(self):
        self.email = "toto@gmail.com"
        self.password = "tototititutu"
        self.last_name = "toto"
        self.first_name = "titi"
        self.company = "tyty"

    def test_valid(self):
        l_form = SignUpForm(
            data={
                'email': self.email,
                'password1': self.password,
                'password2': self.password,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'company': self.company})
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        l_form.save(
            use_https=False,
            site_domain="netliens",
            site_name="netliens",
            email_template_name="account/email_signup_content.html",
            subject_template_name="account/email_signup_subject.txt",
            from_email="contact@netliens.fr")
        self.assertEqual(len(mail.outbox), 1, "Email does not send" )
        self.assertIsNotNone(re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body))
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created !")
        l_user = User.objects.get(email=self.email)
        self.assertFalse(l_user.is_active)

    def test_invalid_email(self):
        # Empty Email
        l_form = SignUpForm(
            data={
                'email': "",
                'password1': self.password,
                'password2': self.password,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'company': self.company})
        self.assertFalse(l_form.is_valid(), "Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 errors !")
        self.assertEqual(len(l_form['email'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['email'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(mail.outbox), 0, "Email has been sent !" )

        # No Email
        l_form = SignUpForm(
            data={
                'email': "toto",
                'password1': self.password,
                'password2': self.password,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'company': self.company})
        self.assertFalse(l_form.is_valid(), "Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 errors !")
        self.assertEqual(len(l_form['email'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['email'].errors[0], "Enter a valid email address.", "Error message not expected !")
        self.assertEqual(len(mail.outbox), 0, "Email has been sent !" )

    def test_invalid_password(self):
        # Empty password1
        l_form = SignUpForm(
            data={
                'email': self.email,
                'password1': "",
                'password2': self.password,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'company': self.company})
        self.assertFalse(l_form.is_valid(), "Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 errors !")
        self.assertEqual(len(l_form['password1'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['password1'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(mail.outbox), 0, "Email has been sent !" )

        # Empty password2
        l_form = SignUpForm(
            data={
                'email': self.email,
                'password1': self.password,
                'password2': "",
                'last_name': self.last_name,
                'first_name': self.first_name,
                'company': self.company})
        self.assertFalse(l_form.is_valid(), "Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 errors !")
        self.assertEqual(len(l_form['password2'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['password2'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(mail.outbox), 0, "Email has been sent !" )

        # Password 1 != Password 2
        l_form = SignUpForm(
            data={
                'email': self.email,
                'password1': self.password,
                'password2': "tititututoto",
                'last_name': self.last_name,
                'first_name': self.first_name,
                'company': self.company})
        self.assertFalse(l_form.is_valid(), "Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 errors !")
        self.assertEqual(len(l_form['password2'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['password2'].errors[0], "The two password fields didn't match.", "Error message not expected !")
        self.assertEqual(len(mail.outbox), 0, "Email has been sent !" )

    def test_invalid_last_name(self):
        # Empty Last_name
        l_form = SignUpForm(
            data={
                'email': self.email,
                'password1': self.password,
                'password2': self.password,
                'last_name': "",
                'first_name': self.first_name,
                'company': self.company})
        self.assertFalse(l_form.is_valid(), "Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 errors !")
        self.assertEqual(len(l_form['last_name'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(mail.outbox), 0, "Email has been sent !" )

    def test_invalid_first_name(self):
        # Empty Last_name
        l_form = SignUpForm(
            data={
                'email': self.email,
                'password1': self.password,
                'password2': self.password,
                'last_name': self.last_name,
                'first_name': "",
                'company': self.company})
        self.assertFalse(l_form.is_valid(), "Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 errors !")
        self.assertEqual(len(l_form['first_name'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['first_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(mail.outbox), 0, "Email has been sent !" )

    def test_invalid_company_name(self):
        # Empty Last_name
        l_form = SignUpForm(
            data={
                'email': self.email,
                'password1': self.password,
                'password2': self.password,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'company': ""})
        self.assertFalse(l_form.is_valid(), "Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 errors !")
        self.assertEqual(len(l_form['company'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['company'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(mail.outbox), 0, "Email has been sent !" )

# -----------------------------
# View
# -----------------------------
class HomeViewTestCase(TestCase):
    pass
    #TODO

# -----------------------------
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
        self.assertEqual(response.url, "/account/signup/done/", "Invalid response url")
        self.assertEqual(User.objects.all().count(), 1, "UserForm has not been created after submit valid form !")
        l_user = User.objects.get(email=self.email)
        self.assertEqual(l_user.email, self.email)
        self.assertEqual(l_user.first_name, self.first_name)
        self.assertEqual(l_user.last_name, self.last_name)
        self.assertEqual(l_user.company, self.company)
        self.assertEqual(l_user.groups.count(), 0)
        self.assertEqual(l_user.user_permissions.count(), 0)
        self.assertFalse(l_user.is_staff)
        self.assertFalse(l_user.is_active)
        self.assertFalse(l_user.is_superuser)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIsNotNone(re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body))

    def test_invalid(self):
        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(response.url, "/account/signup/done/", "Invalid response url")
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        self.assertEqual(len(mail.outbox), 1)

        # User already exist
        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has been created after submit incorrect form !")
        self.assertEqual(len(mail.outbox), 1)

# -----------------------------
class SignUpConfirmationTestCase(TestCase):
    def setUp(self):
        self.email = "toto@toto.fr"
        self.password = "tototititutu" 
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = "Tutu"

    def test_valid(self):
        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(response.url, "/account/signup/done/", "Invalid response url")
        self.assertEqual(User.objects.all().count(), 1, "UserForm has not been created after submit valid form !")
        l_user = User.objects.get(email=self.email)
        self.assertFalse(l_user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        l_re = re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body)
        self.assertIsNotNone(l_re)
        l_confirmation_link = l_re.group(0)
        response = self.client.get(l_confirmation_link)
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(User.objects.all().count(), 1, "UserForm has not been created after submit valid form !")
        l_user = User.objects.get(email=self.email)
        self.assertTrue(l_user.is_active)

    def test_invalid(self):
        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(response.url, "/account/signup/done/", "Invalid response url")
        self.assertEqual(User.objects.all().count(), 1, "UserForm has not been created after submit valid form !")
        l_user = User.objects.get(email=self.email)
        self.assertFalse(l_user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        l_re = re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body)
        self.assertIsNotNone(l_re)
        l_confirmation_link = l_re.group(0)
        response = self.client.get(f"{l_confirmation_link}/toto")
        self.assertEqual(response.status_code, 404, "No Code 200 page return")
        response = self.client.get(f"{l_confirmation_link}t")
        self.assertEqual(response.status_code, 404, "No Code 200 page return")

# -----------------------------
class LoginViewTestCase(TestCase):
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

# -----------------------------
class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.email = "toto@gmail.com"
        self.password = "tototititutu"
        User.objects.create_user(email=self.email, password=self.password)

    def test_valid(self):
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/login/", {    'username': self.email,
                                    'password': self.password })
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")
        response = self.client.get("/account/logout/")
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")
        self.assertIsNone(response.context, "Response has a context !")

    def test_invalid(self):
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 302, "No Code 302 page return")
        self.assertEqual(response.url, "/account/login?next=/account/")
        response = self.client.get("/account/logout/")
        self.assertEqual(response.status_code, 302, "No Code 302 page return")
        self.assertEqual(response.url, "/")

# -----------------------------
class PasswordChangeViewTestCase(TestCase):
    def setUp(self):
        self.email = "toto@gmail.com"
        self.password = "tototititutu"
        self.new_password = "tututititoto"
        User.objects.create_user(email=self.email, password=self.password, is_active=True)

    def test_valid(self):
        # Authentificate User
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/login/", {    'username': self.email,
                                    'password': self.password })
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL, f"Redirection not exist in response '{response}'")
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTrue(response.context['user'].is_authenticated, "User is not authentificated !")
        self.assertEqual(response.context['user'].email, self.email, "Wrong user authentificated !")
        # Request Password change
        response = self.client.post(
            "/account/password_change/",
            {   'old_password': self.password,
                'new_password1': self.new_password,
                'new_password2': self.new_password })
        self.assertEqual(response.status_code, 302, "No Code 200 page return")
        self.assertEqual(response.url, "/account/password_change/done")
        self.assertEqual(len(mail.outbox), 1)

    def test_invalid(self):
        # Authentificate User
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 302, "No Code 302 page return")
        self.assertEqual(response.url, "/account/login?next=/account/")
        # Request password change without account
        response = self.client.get("/account/password_change/")
        self.assertEqual(response.status_code, 302, "No Code 302 page return")
        self.assertEqual(response.url, "/account/login?next=/account/password_change/")

# -----------------------------
class PasswordResetViewTestCase(TestCase):
    def setUp(self):
        self.email = "toto@gmail.com"
        self.password = "tototititutu"
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = "Tutu"

    def test_valid(self):
        User.objects.create_user(email=self.email, password=self.password, is_active=True)
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/password_reset/", { 'email': self.email })
        self.assertEqual(response.url, "/account/password_reset/done/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 1)
        l_re = re.search(RESET_REQUEST_LINK, mail.outbox[0].body)
        self.assertIsNotNone(l_re)
        l_confirmation_link = l_re.group(0)
        response = self.client.get(l_confirmation_link)

    def test_invalid_email(self):
        User.objects.create_user(email=self.email, password=self.password, is_active=True)
        # Empty Email
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/password_reset/", { 'email': "" })
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        self.assertEqual(len(mail.outbox), 0)
        # Not an Email
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/password_reset/", { 'email': "toto" })
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        self.assertEqual(len(mail.outbox), 0)
        # Email does not exist
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created after submit valid form !")
        response = self.client.post(
            "/account/password_reset/", { 'email': "titi@gmail.com" })
        self.assertEqual(response.url, "/account/password_reset/done/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_user_unactive(self):
        User.objects.create_user(email=self.email, password=self.password, is_active=False)
        # If account unactive, no mail send
        response = self.client.post(
            "/account/password_reset/", { 'email': self.email })
        self.assertEqual(response.url, "/account/password_reset/done/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_no_perturbation(self):
        response = self.client.post(
            "/account/signup/", data={  "email": self.email,
                                        "password1": self.password,
                                        "password2": self.password,
                                        "last_name": self.last_name,
                                        "first_name": self.first_name,
                                        "company": self.company})
        self.assertEqual(response.url, "/account/signup/done/", "Invalid response url")
        self.assertEqual(User.objects.all().count(), 1, "UserForm has not been created after submit valid form !")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIsNotNone(re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body))
        l_user = User.objects.get(email=self.email)
        self.assertFalse(l_user.is_active)
        # If account unactive, no more mail send
        response = self.client.post(
            "/account/password_reset/", { 'email': self.email })
        self.assertEqual(response.url, "/account/password_reset/done/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 1)
        # Check if account can be activated
        l_re = re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body)
        self.assertIsNotNone(l_re)
        l_confirmation_link = l_re.group(0)
        response = self.client.get(l_confirmation_link)
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        self.assertEqual(User.objects.all().count(), 1, "UserForm has not been created after submit valid form !")
        l_user = User.objects.get(email=self.email)
        self.assertTrue(l_user.is_active)

# -----------------------------
class PasswordResetDoneViewTestCase(TestCase):
    """
        Nothing to test it is just a template
    """
    pass

class PasswordResetConfirmViewTestCase(TestCase):
    def setUp(self):
        self.email = "toto@gmail.com"
        self.password = "tototititutu"
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = "Tutu"

    def test_valid(self):
        User.objects.create_user(email=self.email, password=self.password, is_active=True)
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created !")
        response = self.client.post(
            "/account/password_reset/", { 'email': self.email })
        self.assertEqual(response.url, "/account/password_reset/done/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 1)
        l_re = re.search(RESET_REQUEST_LINK, mail.outbox[0].body)
        self.assertIsNotNone(l_re)
        l_confirmation_link = l_re.group(0)
        response = self.client.get(l_confirmation_link)
        response = self.client.post(response.url, {  'new_password1': self.password,
                                                     'new_password2': self.password })
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(response.url, "/account/password_reset/complete/", f"Redirection not exist in response '{response}'")

    def test_invalid_password(self):
        User.objects.create_user(email=self.email, password=self.password, is_active=True)
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created !")
        response = self.client.post(
            "/account/password_reset/", { 'email': self.email })
        self.assertEqual(response.url, "/account/password_reset/done/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 1)
        l_re = re.search(RESET_REQUEST_LINK, mail.outbox[0].body)
        self.assertIsNotNone(l_re)
        l_confirmation_link = l_re.group(0)
        # Password 1 empty
        response = self.client.get(l_confirmation_link)
        response = self.client.post(response.url, {  'new_password1': "",
                                                     'new_password2': self.password })
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        # Password 2 empty
        response = self.client.get(l_confirmation_link)
        response = self.client.post(response.url, {  'new_password1': self.password,
                                                     'new_password2': "" })
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        # Both Password empty
        response = self.client.get(l_confirmation_link)
        response = self.client.post(response.url, {  'new_password1': "",
                                                     'new_password2': "" })
        self.assertEqual(response.status_code, 200, "No Code 200 page return")
        # Not same password
        response = self.client.get(l_confirmation_link)
        response = self.client.post(response.url, {  'new_password1': self.password,
                                                     'new_password2': "tititututyty" })
        self.assertEqual(response.status_code, 200, "No Code 200 page return")

    def test_invalid_link(self):
        User.objects.create_user(email=self.email, password=self.password, is_active=True)
        self.assertEqual(User.objects.all().count(), 1, "[DB] UserForm has not been created !")
        response = self.client.post(
            "/account/password_reset/", { 'email': self.email })
        self.assertEqual(response.url, "/account/password_reset/done/", f"Redirection not exist in response '{response}'")
        self.assertEqual(len(mail.outbox), 1)
        l_re = re.search(RESET_REQUEST_LINK, mail.outbox[0].body)
        self.assertIsNotNone(l_re)
        l_confirmation_link = l_re.group(0)
        response = self.client.get(f"{l_confirmation_link}/toto")
        self.assertEqual(response.status_code, 404, "No Code 404 page return")
        response = self.client.get(f"{l_confirmation_link}t")
        self.assertEqual(response.status_code, 404, "No Code 404 page return")
