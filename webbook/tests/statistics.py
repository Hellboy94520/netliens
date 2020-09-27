from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from webbook.models import Statistics

class StatisticsModelTestCase(TestCase):
    def test_default_construction(self):
        l_stats = Statistics()
        #TODO: Check format with time machine for example
        self.assertIsNotNone(l_stats.date_joined, "[LOCAL] Date Joined is None !")
        self.assertIsNotNone(l_stats.date_validation, "[LOCAL] Date Validation is None !")
        with self.assertRaises(ObjectDoesNotExist):
            l_stats.user_validation
        self.assertIsNotNone(l_stats.last_update, "[LOCAL] Last Update is None !")

    def test_default_construction_database(self):
        l_stats = Statistics()
        self.assertEqual(Statistics.objects.all().count(), 0, "[DB] Statistics already exist !")
        l_stats.save()
        self.assertEqual(Statistics.objects.all().count(), 1, "[DB] Statistics has not been created !")
        l_stats = Statistics.objects.filter()[0]
        #TODO: Check format with time machine for example
        self.assertIsNotNone(l_stats.date_joined, "[DB] Date Joined is None !")
        self.assertIsNotNone(l_stats.date_validation, "[DB] Date Validation is None !")
        with self.assertRaises(ObjectDoesNotExist):
            l_stats.user_validation
        self.assertIsNotNone(l_stats.last_update, "[DB] Last Update is None !")
