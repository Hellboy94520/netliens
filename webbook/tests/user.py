from django.test import TestCase
from django.utils import timezone

from webbook.models import User, UserType
from webbook.forms import UserFormCreation

class UserModelTestCase(TestCase):
    def setUp(self):
        self.username = "toto"
        self.email = "alexandre.delahaye@free.fr"
        self.password = "tototititutu" 
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.is_staff = True
        self.is_active = False
        self.is_superuser = True       

    def test_minimal_construction(self):
        l_user = User.objects.create(username=self.username, email=self.email, password=self.password)
        self.assertEqual(l_user.username, self.username, "[LOCAL] username invalid !")
        self.assertEqual(l_user.email, self.email, "[LOCAL] email invalid !")
        self.assertEqual(l_user.password, self.password, "[LOCAL] password invalid !")
        self.assertEqual(l_user.first_name, "", "[LOCAL] first_name invalid !")
        self.assertEqual(l_user.last_name, "", "[LOCAL] last_name invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[LOCAL] Groups already exist !")        
        self.assertEqual(l_user.user_permissions.count(), 0, "[LOCAL] User_Permissions already exist !")
        self.assertFalse(l_user.is_staff, "[LOCAL] is_staff is not False !")
        self.assertFalse(l_user.is_active, "[LOCAL] is_active is not False !")
        self.assertFalse(l_user.is_superuser, "[LOCAL] is_super_user is not False !")

    def test_minimal_construction_database(self):
        User.objects.create(username=self.username, email=self.email, password=self.password)
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created !")
        l_user = User.objects.get(username=self.username)
        self.assertEqual(l_user.username, self.username, "[DB] username invalid !")
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.password, self.password, "[DB] password invalid !")        
        self.assertEqual(l_user.first_name, "", "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, "", "[DB] last_name invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")        
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertFalse(l_user.is_staff, "[DB] is_staff is not False !")
        self.assertFalse(l_user.is_active, "[DB] is_active is not False !")
        self.assertFalse(l_user.is_superuser, "[DB] is_super_user is not False !")

    def test_constructor(self):
        l_user = User.objects.create(username=self.username, email=self.email, password=self.password,
                                     first_name=self.first_name, last_name=self.last_name,
                                     is_staff=self.is_staff, is_active=self.is_active, is_superuser=self.is_superuser)
        self.assertEqual(l_user.username, self.username, "[LOCAL] username invalid !")
        self.assertEqual(l_user.email, self.email, "[LOCAL] email invalid !")
        self.assertEqual(l_user.password, self.password, "[LOCAL] password invalid !")
        self.assertEqual(l_user.first_name, self.first_name, "[LOCAL] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[LOCAL] last_name invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[LOCAL] Groups already exist !")        
        self.assertEqual(l_user.user_permissions.count(), 0, "[LOCAL] User_Permissions already exist !")
        self.assertTrue(l_user.is_staff, "[LOCAL] is_staff is not True !")
        self.assertFalse(l_user.is_active, "[LOCAL] is_active is not False !")
        self.assertTrue(l_user.is_superuser, "[LOCAL] is_super_user is not True !")

    def test_constructor_database(self):
        User.objects.create(username=self.username, email=self.email, password=self.password,
                              first_name=self.first_name, last_name=self.last_name,
                              is_staff=self.is_staff, is_active=self.is_active, is_superuser=self.is_superuser)
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created !")
        l_user = User.objects.get(username=self.username)
        self.assertEqual(l_user.username, self.username, "[DB] username invalid !")
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.password, self.password, "[DB] password invalid !")        
        self.assertEqual(l_user.first_name, self.first_name, "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[DB] last_name invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")        
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertTrue(l_user.is_staff, "[DB] is_staff is not True !")
        self.assertFalse(l_user.is_active, "[DB] is_active is not False !")
        self.assertTrue(l_user.is_superuser, "[DB] is_super_user is not True !")
    
    #TODO
    # def test_constructor_error(self):
    #     pass
    
    #TODO: username and email
    # def test_user_already exist(self):
    #     pass

class UserFormCreationTestCase(TestCase):
    def setUp(self):
        self.username = "toto"
        self.email = "alexandre.delahaye@free.fr"
        self.password = "tototititutu" 
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = "Tutu"
        self.is_staff = False
        self.is_active = False
        self.is_superuser = False

    def test_form_valid(self):
        l_user = UserFormCreation(UserType.User,
                                  data={'username': self.username,
                                        'email': self.email,
                                        'password': self.password,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'company': self.company})
        self.assertTrue(l_user.is_valid(), "Form is not valid !")
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        l_user.save()
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created after save form !")
        l_user = User.objects.get(username=self.username)
        self.assertEqual(l_user.username, self.username, "[DB] username invalid !")
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.password, self.password, "[DB] password invalid !")        
        self.assertEqual(l_user.first_name, self.first_name, "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[DB] last_name invalid !")
        self.assertEqual(l_user.company, self.company, "[DB] company invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")        
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertFalse(l_user.is_staff, "[DB] is_staff is not False !")
        self.assertFalse(l_user.is_active, "[DB] is_active is not False !")
        self.assertFalse(l_user.is_superuser, "[DB] is_super_user is not False !")

    def test_form_constructor_args_invalid(self):
        with self.assertRaisesRegexp(TypeError, 'userType'):
            l_user = UserFormCreation(data={'username': self.username})
        with self.assertRaises(UnboundLocalError):
            l_user.is_valid()
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        with self.assertRaisesRegexp(NameError, 'ValidationError'):
            l_user = UserFormCreation("toto", data={'username': self.username})
        with self.assertRaises(UnboundLocalError):
            l_user.is_valid()
        self.assertEqual(User.objects.all().count(), 0, "[DB] User has not to be created !")
        with self.assertRaisesRegexp(NameError, 'ValidationError'):
            l_user = UserFormCreation(1, data={'username': self.username})
        with self.assertRaises(UnboundLocalError):
            l_user.is_valid()
        self.assertEqual(User.objects.all().count(), 0, "[DB] User has not to be created !")

    def test_form_not_valid_only_username(self):
        l_user = UserFormCreation(UserType.User, data={'username': self.username})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 5)
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

    def test_form_not_valid_no_data(self):
        l_user = UserFormCreation(UserType.User, data={})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 6)
        self.assertEqual(len(l_user['password'].errors), 1, "Expected only 1 error for 'password' field !")
        self.assertEqual(l_user['password'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['username'].errors), 1, "Expected only 1 error for 'username' field !")
        self.assertEqual(l_user['username'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['last_name'].errors), 1, "Expected only 1 error for 'last_name' field !")
        self.assertEqual(l_user['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['first_name'].errors), 1, "Expected only 1 error for 'first_name' field !")
        self.assertEqual(l_user['first_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['company'].errors), 1, "Expected only 1 error for 'company' field !")
        self.assertEqual(l_user['company'].errors[0], "This field is required.", "Error message not expected !")

class StaffFormCreationTestCase(TestCase):
    def setUp(self):
        self.username = "toto"
        self.email = "alexandre.delahaye@free.fr"
        self.password = "tototititutu" 
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = ""
        self.is_staff = True
        self.is_active = False
        self.is_superuser = False

    def test_form_valid(self):
        l_user = UserFormCreation(UserType.Staff,
                                  data={'username': self.username,
                                        'email': self.email,
                                        'password': self.password,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name})
        self.assertTrue(l_user.is_valid(), "Form is not valid !")
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        l_user.save()
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created after save form !")
        l_user = User.objects.get(username=self.username)
        self.assertEqual(l_user.username, self.username, "[DB] username invalid !")
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.password, self.password, "[DB] password invalid !")        
        self.assertEqual(l_user.first_name, self.first_name, "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[DB] last_name invalid !")
        self.assertEqual(l_user.company, self.company, "[DB] company invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")        
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertTrue(l_user.is_staff, "[DB] is_staff is not True !")
        self.assertFalse(l_user.is_active, "[DB] is_active is not False !")
        self.assertFalse(l_user.is_superuser, "[DB] is_super_user is not False !")

    def test_form_constructor_args_invalid(self):
        with self.assertRaisesRegexp(TypeError, 'userType'):
            l_user = UserFormCreation(data={'username': self.username})
        with self.assertRaises(UnboundLocalError):
            l_user.is_valid()
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        with self.assertRaisesRegexp(NameError, 'ValidationError'):
            l_user = UserFormCreation("toto", data={'username': self.username})
        with self.assertRaises(UnboundLocalError):
            l_user.is_valid()
        self.assertEqual(User.objects.all().count(), 0, "[DB] User has not to be created !")
        with self.assertRaisesRegexp(NameError, 'ValidationError'):
            l_user = UserFormCreation(1, data={'username': self.username})
        with self.assertRaises(UnboundLocalError):
            l_user.is_valid()
        self.assertEqual(User.objects.all().count(), 0, "[DB] User has not to be created !")

    def test_form_not_valid_only_username(self):
        l_user = UserFormCreation(UserType.Staff, data={'username': self.username})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 4)
        self.assertEqual(len(l_user['password'].errors), 1, "Expected only 1 error for 'password' field !")
        self.assertEqual(l_user['password'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['last_name'].errors), 1, "Expected only 1 error for 'last_name' field !")
        self.assertEqual(l_user['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['first_name'].errors), 1, "Expected only 1 error for 'first_name' field !")
        self.assertEqual(l_user['first_name'].errors[0], "This field is required.", "Error message not expected !")

    def test_form_not_valid_no_data(self):
        l_user = UserFormCreation(UserType.Staff, data={})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 5)
        self.assertEqual(len(l_user['password'].errors), 1, "Expected only 1 error for 'password' field !")
        self.assertEqual(l_user['password'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['username'].errors), 1, "Expected only 1 error for 'username' field !")
        self.assertEqual(l_user['username'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['last_name'].errors), 1, "Expected only 1 error for 'last_name' field !")
        self.assertEqual(l_user['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['first_name'].errors), 1, "Expected only 1 error for 'first_name' field !")
        self.assertEqual(l_user['first_name'].errors[0], "This field is required.", "Error message not expected !")
     

class AdminFormCreationTestCase(TestCase):
    def setUp(self):
        self.username = "toto"
        self.email = "alexandre.delahaye@free.fr"
        self.password = "tototititutu" 
        self.first_name = "Toto"
        self.last_name = "Titi"
        self.company = ""
        self.is_staff = True
        self.is_active = True
        self.is_superuser = True

    def test_form_valid(self):
        l_user = UserFormCreation(UserType.Admin,
                                  data={'username': self.username,
                                        'email': self.email,
                                        'password': self.password,
                                        'first_name': self.first_name,
                                        'last_name': self.last_name})
        self.assertTrue(l_user.is_valid(), "Form is not valid !")
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        l_user.save()
        self.assertEqual(User.objects.all().count(), 1, "[DB] User has not been created after save form !")
        l_user = User.objects.get(username=self.username)
        self.assertEqual(l_user.username, self.username, "[DB] username invalid !")
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.password, self.password, "[DB] password invalid !")        
        self.assertEqual(l_user.first_name, self.first_name, "[DB] first_name invalid !")
        self.assertEqual(l_user.last_name, self.last_name, "[DB] last_name invalid !")
        self.assertEqual(l_user.company, self.company, "[DB] company invalid !")
        self.assertEqual(l_user.groups.count(), 0, "[DB] Groups already exist !")        
        self.assertEqual(l_user.user_permissions.count(), 0, "[DB] User_Permissions already exist !")
        self.assertTrue(l_user.is_staff, "[DB] is_staff is not True !")
        self.assertTrue(l_user.is_active, "[DB] is_active is not True !")
        self.assertTrue(l_user.is_superuser, "[DB] is_super_user is not true !")

    def test_form_constructor_args_invalid(self):
        with self.assertRaisesRegexp(TypeError, 'userType'):
            l_user = UserFormCreation(data={'username': self.username})
        with self.assertRaises(UnboundLocalError):
            l_user.is_valid()
        self.assertEqual(User.objects.all().count(), 0, "[DB] an User already exist !")
        with self.assertRaisesRegexp(NameError, 'ValidationError'):
            l_user = UserFormCreation("toto", data={'username': self.username})
        with self.assertRaises(UnboundLocalError):
            l_user.is_valid()
        self.assertEqual(User.objects.all().count(), 0, "[DB] User has not to be created !")
        with self.assertRaisesRegexp(NameError, 'ValidationError'):
            l_user = UserFormCreation(1, data={'username': self.username})
        with self.assertRaises(UnboundLocalError):
            l_user.is_valid()
        self.assertEqual(User.objects.all().count(), 0, "[DB] User has not to be created !")

    def test_form_not_valid_only_username(self):
        l_user = UserFormCreation(UserType.Admin, data={'username': self.username})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 4)
        self.assertEqual(len(l_user['password'].errors), 1, "Expected only 1 error for 'password' field !")
        self.assertEqual(l_user['password'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['last_name'].errors), 1, "Expected only 1 error for 'last_name' field !")
        self.assertEqual(l_user['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['first_name'].errors), 1, "Expected only 1 error for 'first_name' field !")
        self.assertEqual(l_user['first_name'].errors[0], "This field is required.", "Error message not expected !")

    def test_form_not_valid_no_data(self):
        l_user = UserFormCreation(UserType.Admin, data={})
        self.assertFalse(l_user.is_valid(), "Form is valid !")
        self.assertEqual(len(l_user.errors), 5)
        self.assertEqual(len(l_user['password'].errors), 1, "Expected only 1 error for 'password' field !")
        self.assertEqual(l_user['password'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['username'].errors), 1, "Expected only 1 error for 'username' field !")
        self.assertEqual(l_user['username'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['email'].errors), 1, "Expected only 1 error for 'email' field !")
        self.assertEqual(l_user['email'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['last_name'].errors), 1, "Expected only 1 error for 'last_name' field !")
        self.assertEqual(l_user['last_name'].errors[0], "This field is required.", "Error message not expected !")
        self.assertEqual(len(l_user['first_name'].errors), 1, "Expected only 1 error for 'first_name' field !")
        self.assertEqual(l_user['first_name'].errors[0], "This field is required.", "Error message not expected !")
