from django.test import TestCase

from webbook.models import User

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
