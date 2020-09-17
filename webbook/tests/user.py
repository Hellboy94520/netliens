from django.test import TestCase
from django.utils import timezone

from webbook.models import User

class UserModel(TestCase):
    def setUp(self):
        self.username = "toto"
        self.email = "alexandre.delahaye@free.fr"
        self.password = "tototititutu"        
        self.user = User.objects.create(username=self.username, email=self.email, password=self.password)

    def test_default_construction(self):
        self.assertEqual(self.user.username, self.username, "[LOCAL] username invalid !")
        self.assertEqual(self.user.email, self.email, "[LOCAL] email invalid !")
        self.assertEqual(self.user.password, self.password, "[LOCAL] password invalid !")
        self.assertEqual(self.user.first_name, "", "[LOCAL] first_name is not empty !")
        self.assertEqual(self.user.last_name, "", "[LOCAL] last_name is not empty !")
        self.assertEqual(self.user.company, "", "[LOCAL] company is not empty !")
        # self.assertIsNone(self.user.groups, "[LOCAL] groups is not None !")
        # self.assertIsNone(self.user.permissions, "[LOCAL] permissions is not None !")
        self.assertFalse(self.user.is_staff, "[LOCAL] is_staff is not False !")
        self.assertTrue(self.user.is_active, "[LOCAL] is_active is not True !")
        self.assertFalse(self.user.is_superuser, "[LOCAL] is_super_user is not False !")

    def test_default_construction_database(self):
        self.assertEqual(User.objects.all().count(), 1, "User has not been created !")
        l_user = User.objects.get(username=self.username)
        self.assertEqual(l_user.username, self.username, "[DB] username invalid !")
        self.assertEqual(l_user.email, self.email, "[DB] email invalid !")
        self.assertEqual(l_user.password, self.password, "[DB] password invalid !")        
        self.assertEqual(l_user.first_name, "", "[DB] first_name is not empty !")
        self.assertEqual(l_user.last_name, "", "[DB] last_name is not empty !")
        self.assertEqual(l_user.company, "", "[DB] company is not empty !")
        # self.assertIsNone(l_user.groups, "[DB] groups is not None !")
        # self.assertIsNone(l_user.permissions, "[DB] permissions is not None !")
        self.assertFalse(l_user.is_staff, "[DB] is_staff is not False !")
        self.assertTrue(l_user.is_active, "[DB] is_active is not True !")
        self.assertFalse(l_user.is_superuser, "[DB] is_super_user is not False !")

