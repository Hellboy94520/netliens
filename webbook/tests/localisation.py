from django.test import TestCase
from django.test import Client
from django.core.exceptions import ObjectDoesNotExist

from webbook.models import Localisation
from webbook.forms import LocalisationForm

class LocalisationFormTestCase(TestCase):
    def setUp(self):
        self.name = "This is a title !"
        self.resume = "This is an announcement !"
        self.code = "ABCD"
        self.is_enable = False
        self.parent = None
        self.order = 1

    def test_valid(self):
        l_localisation = LocalisationForm(data={'name': self.name,
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertTrue(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(Localisation.objects.all().count(), 0, "An object already exist !")
        l_localisation.save()
        self.assertEqual(Localisation.objects.all().count(), 1, "Object has not been save !")
        l_localisation = Localisation.objects.filter()[0]
        self.assertEqual(l_localisation.name, self.name, "Unexpected value !")
        self.assertEqual(l_localisation.resume, self.resume, "Unexpected value !")
        self.assertEqual(l_localisation.code, self.code, "Unexpected value !")
        self.assertEqual(l_localisation.is_enable, self.is_enable, "Unexpected value !")
        self.assertIsNone(l_localisation.parent, "Unexpected value !")
        self.assertEqual(l_localisation.order, self.order, "Unexpected value !")

    def test_clean_function(self):
        l_localisation = LocalisationForm(data={'name': self.name,
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertTrue(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(Localisation.objects.all().count(), 0, "An object already exist !")
        l_localisation = l_localisation.save()
        self.assertEqual(Localisation.objects.filter(name=self.name).exclude(pk=None).count(), 1)
        self.assertEqual(Localisation.objects.filter(name=self.name).exclude(pk=l_localisation.id).count(), 0)

    def test_name(self):
        # Empty Name
        l_localisation = LocalisationForm(data={'name': "",
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertFalse(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_localisation.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_localisation['name'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_localisation['name'].errors[0], "This field is required.", "Error message not expected !")

        # Name too long
        l_name_too_long = ""
        l_max_range = 50+1
        for i in range(0, l_max_range):
            l_name_too_long += "_"
        l_localisation = LocalisationForm(data={'name': l_name_too_long,
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertFalse(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_localisation.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_localisation['name'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_localisation['name'].errors[0], f"Ensure this value has at most 50 characters (it has {l_max_range}).", "Error message not expected !")

    def test_code(self):
        # Empty Code
        l_localisation = LocalisationForm(data={'name': self.name,
                                                'resume': self.resume,
                                                'code': "",
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertFalse(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_localisation.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_localisation['code'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_localisation['code'].errors[0], "This field is required.", "Error message not expected !")

        # Code too long
        l_code_too_long = ""
        l_code_max_range = 5+1
        for i in range(0, l_code_max_range):
            l_code_too_long += "r"
        l_localisation = LocalisationForm(data={'name': self.name,
                                                'resume': self.resume,
                                                'code': l_code_too_long,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertFalse(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_localisation.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_localisation['code'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_localisation['code'].errors[0], f"Ensure this value has at most 5 characters (it has {l_code_max_range}).", "Error message not expected !")

    def test_parent(self):
        l_parent = LocalisationForm(data={  'name': "Localisation Parent",
                                            'resume': "Localisation Parent",
                                            'code': self.code,
                                            'is_enable': False,
                                            'parent': None,
                                            'order': 1})
        self.assertTrue(l_parent.is_valid(), "Form is not valid !")
        l_parent.save()
        self.assertEqual(len(Localisation.objects.all()), 1, "Form has not been save !")
        l_parent = Localisation.objects.get(name="Localisation Parent")
        # One children
        l_localisation = LocalisationForm(data={'name': "Children 1",
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': l_parent.id,
                                                'order': 1})
        self.assertTrue(l_localisation.is_valid(), "Form is not valid !")
        l_localisation.save()
        self.assertEqual(len(Localisation.objects.all()), 2, "Form has not been save !")
        # Second children
        l_localisation = LocalisationForm(data={'name': "Children 2",
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': l_parent.pk,
                                                'order': 2})
        self.assertTrue(l_localisation.is_valid(), "Form is not valid !")
        l_localisation.save()
        self.assertEqual(len(Localisation.objects.all()), 3, "Form has not been save !")
        # Children with same parent and order as Children 1
        l_localisation = LocalisationForm(data={'name': "Children 3",
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': l_parent.pk,
                                                'order': 1})
        self.assertFalse(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_localisation.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_localisation['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_localisation['order'].errors[0], "A localisation with this order and parent already exist.", "Error message not expected !")
        # Children with same parent and name as Children 1
        l_localisation = LocalisationForm(data={'name': "Children 1",
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': l_parent.pk,
                                                'order': 3})
        self.assertFalse(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_localisation.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_localisation['name'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_localisation['name'].errors[0], "A localisation with this name and parent already exist.", "Error message not expected !")
        # Children with same parent, name and order as Children 1
        l_localisation = LocalisationForm(data={'name': "Children 1",
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': l_parent.pk,
                                                'order': 1})
        self.assertFalse(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_localisation.errors), 2, "Unexpected errors quantity !")
        self.assertEqual(len(l_localisation['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_localisation['order'].errors[0], "A localisation with this order and parent already exist.")
        self.assertEqual(len(l_localisation['name'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_localisation['name'].errors[0], "A localisation with this name and parent already exist.", "Error message not expected !")
        # Delete parent
        l_parent.delete()
        l_localisation_1 = Localisation.objects.get(name="Children 1")
        with self.assertRaises(ObjectDoesNotExist):
            l_localisation_1.parent
        l_localisation_2 = Localisation.objects.get(name="Children 2")
        with self.assertRaises(ObjectDoesNotExist):
            l_localisation_2.parent

    def test_order(self):
        # Null value
        l_localisation = LocalisationForm(data={'name': "Children 1",
                                                'resume': self.resume,
                                                'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': 0})
        self.assertFalse(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_localisation.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_localisation['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_localisation['order'].errors[0], "Ensure this value is greater than or equal to 1.", "Error message not expected !")
