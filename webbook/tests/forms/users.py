from django.test import TestCase
from django.core import mail

from webbook.models import User
from webbook.forms import PublicUserForm, SignUpForm#, AdminUserForm

import re

SIGNUP_CONFIRMATION_LINK=r'(http:\/\/.*\/account\/signup\/.*\/.*\/)'
RESET_REQUEST_LINK=r'(http:\/\/.*\/account\/password_reset\/.*\/.*\/)'

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
        self.assertEqual(l_form['password2'].errors[0], "The two password fields didn’t match.", "Error message not expected !")
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

    def test_empty_company_name(self):
        # Empty Last_name
        l_form = SignUpForm(
            data={
                'email': self.email,
                'password1': self.password,
                'password2': self.password,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'company': ""})
        l_form.save(
            use_https=False,
            site_domain="netliens",
            site_name="netliens",
            email_template_name="account/email_signup_content.html",
            subject_template_name="account/email_signup_subject.txt",
            from_email="contact@netliens.fr")
        self.assertTrue(l_form.is_valid(), "Form is valid !")
        self.assertEqual(len(mail.outbox), 1, "Email does not send" )
        self.assertIsNotNone(re.search(SIGNUP_CONFIRMATION_LINK, mail.outbox[0].body))
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created !")
        l_user = User.objects.get(email=self.email)
        self.assertFalse(l_user.is_active)

