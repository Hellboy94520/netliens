from django.test import TestCase
from django.test import Client
from django.core.exceptions import ObjectDoesNotExist

from webbook.models import get_all_model_in_order, get_all_modelWithData_in_order, get_all_modelDataWithPosition_in_order
from webbook.models import Localisation, LocalisationData, MINIMUM_ORDER, TITLE_MAX_LENGTH, MAX_CODE_LENGTH
from webbook.forms import LocalisationForm
from webbook.models import LanguageAvailable, User

class LocalisationModel(TestCase):
    def createLocalisationWithData(self, **kwargs):
        localisation = Localisation.objects.create(
            is_enable=True,
            parent=kwargs['parent'],
            order=kwargs['order']
        )
        localisationDataFr = LocalisationData.objects.create(
            name=kwargs['name'],
            resume=kwargs['resume'],
            localisation=localisation,
            language=LanguageAvailable.FR.value
        )
        localisationDataEn = LocalisationData.objects.create(
            name=kwargs['name'],
            resume=kwargs['resume'],
            localisation=localisation,
            language=LanguageAvailable.EN.value
        )
        return localisation, localisationDataFr, localisationDataEn

    def initLocalisationWithDataForTest(self):
        # Creation random localisation
        self.localisation_2, self.localisation_2_fr, self.localisation_2_en = self.createLocalisationWithData(
            parent=None,
            order=2,
            name="Localisation 2",
            resume="Localisation 2"
        )
        self.localisation_22, self.localisation_22_fr, self.localisation_22_en = self.createLocalisationWithData(
            parent=self.localisation_2,
            order=2,
            name="Localisation 22",
            resume="Localisation 22"
        )
        self.localisation_21, self.localisation_21_fr, self.localisation_21_en = self.createLocalisationWithData(
            parent=self.localisation_2,
            order=1,
            name="Localisation 21",
            resume="Localisation 21"
        )

        self.localisation_1, self.localisation_1_fr, self.localisation_1_en = self.createLocalisationWithData(
            parent=None,
            order=1,
            name="Localisation 1",
            resume="Localisation 1"
        )
        self.localisation_12, self.localisation_12_fr, self.localisation_12_en = self.createLocalisationWithData(
            parent=self.localisation_1,
            order=2,
            name="Localisation 12",
            resume="Localisation 12"
        )
        self.localisation_11, self.localisation_11_fr, self.localisation_11_en = self.createLocalisationWithData(
            parent=self.localisation_1,
            order=1,
            name="Localisation 11",
            resume="Localisation 11"
        )
        self.localisation_112, self.localisation_112_fr, self.localisation_112_en = self.createLocalisationWithData(
            parent=self.localisation_11,
            order=2,
            name="Localisation 112",
            resume="Localisation 112"
        )
        self.localisation_111, self.localisation_111_fr, self.localisation_111_en = self.createLocalisationWithData(
            parent=self.localisation_11,
            order=1,
            name="Localisation 111",
            resume="Localisation 111"
        )

        # Check creation
        self.localisation_total = 8
        self.assertEqual(Localisation.objects.all().count(), self.localisation_total)
        self.assertEqual(LocalisationData.objects.all().count(), self.localisation_total*2)



    def test_get_all_localisation_in_order(self):
        # Create random localisation
        self.initLocalisationWithDataForTest()

        # Validate function
        localisation_list = get_all_model_in_order(model=Localisation)
        self.assertEqual(len(localisation_list), self.localisation_total)
        for i, localisation in enumerate(localisation_list):
            if i==0:
                self.assertEqual(localisation, self.localisation_1.pk)
            if i==1:
                self.assertEqual(localisation, self.localisation_11.pk)
            if i==2:
                self.assertEqual(localisation, self.localisation_111.pk)
            if i==3:
                self.assertEqual(localisation, self.localisation_112.pk)
            if i==4:
                self.assertEqual(localisation, self.localisation_12.pk)
            if i==5:
                self.assertEqual(localisation, self.localisation_2.pk)
            if i==6:
                self.assertEqual(localisation, self.localisation_21.pk)
            if i==7:
                self.assertEqual(localisation, self.localisation_22.pk)

    def test_get_all_localisationWithData_in_order(self):
        # Create random localisation
        self.initLocalisationWithDataForTest()

        # Validate function
        localisation_map_fr = get_all_modelWithData_in_order(
            model=Localisation,
            language=LanguageAvailable.FR.value
        )
        localisation_map_en = get_all_modelWithData_in_order(
            model=Localisation,
            language=LanguageAvailable.EN.value
        )
        self.assertEqual(len(localisation_map_fr), self.localisation_total)
        self.assertEqual(len(localisation_map_en), self.localisation_total)

        for i, localisation in enumerate(localisation_map_fr):
            if i==0:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_1_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_1_en)
            if i==1:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_11_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_11_en)
            if i==2:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_111_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_111_en)
            if i==3:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_112_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_112_en)
            if i==4:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_12_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_12_en)
            if i==5:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_2_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_2_en)
            if i==6:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_21_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_21_en)
            if i==7:
                self.assertEqual(localisation_map_fr[localisation], self.localisation_22_fr)
                self.assertEqual(localisation_map_en[localisation], self.localisation_22_en)

    def test_get_all_localisationDataWithPosition_in_order(self):
        # Create random localisation
        self.initLocalisationWithDataForTest()

        # Validate function
        localisation_map_fr = get_all_modelDataWithPosition_in_order(
            model=Localisation,
            language=LanguageAvailable.FR.value
        )
        localisation_map_en = get_all_modelDataWithPosition_in_order(
            model=Localisation,
            language=LanguageAvailable.EN.value
        )
        self.assertEqual(len(localisation_map_fr), self.localisation_total)

        for i, localisation in enumerate(localisation_map_fr):
            if i==0:
                self.assertEqual(localisation, self.localisation_1)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_1_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_1_en)
                self.assertEqual(localisation_map_fr[localisation][1], 0)
                self.assertEqual(localisation_map_en[localisation][1], 0)
            if i==1:
                self.assertEqual(localisation, self.localisation_11)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_11_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_11_en)
                self.assertEqual(localisation_map_fr[localisation][1], 1)
                self.assertEqual(localisation_map_en[localisation][1], 1)
            if i==2:
                self.assertEqual(localisation, self.localisation_111)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_111_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_111_en)
                self.assertEqual(localisation_map_fr[localisation][1], 2)
                self.assertEqual(localisation_map_en[localisation][1], 2)
            if i==3:
                self.assertEqual(localisation, self.localisation_112)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_112_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_112_en)
                self.assertEqual(localisation_map_fr[localisation][1], 2)
                self.assertEqual(localisation_map_en[localisation][1], 2)
            if i==4:
                self.assertEqual(localisation, self.localisation_12)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_12_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_12_en)
                self.assertEqual(localisation_map_fr[localisation][1], 1)
                self.assertEqual(localisation_map_en[localisation][1], 1)
            if i==5:
                self.assertEqual(localisation, self.localisation_2)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_2_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_2_en)
                self.assertEqual(localisation_map_fr[localisation][1], 0)
                self.assertEqual(localisation_map_en[localisation][1], 0)
            if i==6:
                self.assertEqual(localisation, self.localisation_21)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_21_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_21_en)
                self.assertEqual(localisation_map_fr[localisation][1], 1)
                self.assertEqual(localisation_map_en[localisation][1], 1)
            if i==7:
                self.assertEqual(localisation, self.localisation_22)
                self.assertEqual(localisation_map_fr[localisation][0], self.localisation_22_fr)
                self.assertEqual(localisation_map_en[localisation][0], self.localisation_22_en)
                self.assertEqual(localisation_map_fr[localisation][1], 1)
                self.assertEqual(localisation_map_en[localisation][1], 1)



class LocalisationFormTestCase(TestCase):
    """
        -----------------------------------------
        LocalisationFormTestCase tests
        -----------------------------------------
    """
    def setUp(self):
        self.default_is_enable = False
        self.code = "ABCD"
        self.insee = 10
        self.is_enable = True
        self.parent = None
        self.order = 1
        self.user = User.objects.create(email='toto', password='titi')


    def test_user_valid(self):
        l_localisation = LocalisationForm(
            data={'code': self.code,
                'insee': self.insee,
                'parent': self.parent,
                'order': self.order})
        self.assertTrue(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(Localisation.objects.all().count(), 0, "An object already exist !")
        l_localisation.save(user=self.user)
        # Check Localisation
        self.assertEqual(Localisation.objects.all().count(), 1, "Object has not been save !")
        l_localisation = Localisation.objects.filter()[0]
        self.assertEqual(l_localisation.code, self.code, "Unexpected value !")
        self.assertEqual(l_localisation.insee, self.insee, "Unexpected value !")
        self.assertEqual(l_localisation.is_enable, self.default_is_enable, "Unexpected value !")
        self.assertIsNone(l_localisation.parent, "Unexpected value !")
        self.assertEqual(l_localisation.order, self.order, "Unexpected value !")
        # Check LocalisationStats
        l_localisation_stat = l_localisation.get_statistics()
        self.assertIsNotNone(l_localisation_stat, "Stats does not exist !")
        self.assertIsNotNone(l_localisation_stat.date_creation)
        self.assertEqual(l_localisation_stat.user_creation, self.user)
        self.assertIsNone(l_localisation_stat.date_validation)
        self.assertIsNone(l_localisation_stat.user_validation)


    def test_user_valid(self):
        l_localisation = LocalisationForm(
            data={'code': self.code,
                'insee': self.insee,
                'is_enable': self.is_enable,
                'parent': self.parent,
                'order': self.order})
        self.assertTrue(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(Localisation.objects.all().count(), 0, "An object already exist !")
        l_localisation.save(user=self.user)
        # Check Localisation
        self.assertEqual(Localisation.objects.all().count(), 1, "Object has not been save !")
        l_localisation = Localisation.objects.filter()[0]
        self.assertEqual(l_localisation.code, self.code, "Unexpected value !")
        self.assertEqual(l_localisation.insee, self.insee, "Unexpected value !")
        self.assertEqual(l_localisation.is_enable, self.is_enable, "Unexpected value !")
        self.assertIsNone(l_localisation.parent, "Unexpected value !")
        self.assertEqual(l_localisation.order, self.order, "Unexpected value !")
        # Check LocalisationStats
        l_localisation_stat = l_localisation.get_statistics()
        self.assertIsNotNone(l_localisation_stat, "Stats does not exist !")
        self.assertIsNotNone(l_localisation_stat.date_creation)
        self.assertEqual(l_localisation_stat.user_creation, self.user)
        self.assertIsNotNone(l_localisation_stat.date_validation)
        self.assertEqual(l_localisation_stat.user_validation, self.user)


    def test_invalid_order(self):
        l_form = LocalisationForm(
            data={'code': self.code,
                'insee': self.insee,
                'is_enable': self.is_enable,
                'parent': self.parent,
                'order': MINIMUM_ORDER-1
            }
        )
        self.assertFalse(l_form.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_form.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_form['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_form['order'].errors[0], f"Ensure this value is greater than or equal to {MINIMUM_ORDER}.", "Error message not expected !")


    def test_unique_order(self):
        # Create first localisation
        l_form = LocalisationForm(data={'order': MINIMUM_ORDER, 'code': self.code, 'insee': self.insee})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0, "An object already exist !")
        l_form.save(user=self.user)

        # Create second localisation with same order value (error)
        l_form = LocalisationForm(data={'order': MINIMUM_ORDER, 'code': f"{self.code}A", 'insee': self.insee})
        self.assertFalse(l_form.is_valid(), f"Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_form['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_form['order'].errors[0], "A localisation with this order and parent already exist.", "Error message not expected !")


    def test_invalid_code(self):
        # Empty Code
        l_form = LocalisationForm(data={'code': "",
                                                'insee': self.insee,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertFalse(l_form.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_form.errors), 1, f"Expected only 1 error ! {l_form.errors}")
        self.assertEqual(len(l_form['code'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['code'].errors[0], "This field is required.", "Error message not expected !")

        # Code too long
        l_form = LocalisationForm(data={'code': "1" * (MAX_CODE_LENGTH+1),
                                                'insee': self.insee,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertFalse(l_form.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_form['code'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['code'].errors[0], f"Ensure this value has at most {MAX_CODE_LENGTH} characters (it has {MAX_CODE_LENGTH+1}).", "Error message not expected !")

    def test_unique_order_with_children(self):
        # Create Parent localisation
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER, 'code': self.code, 'insee': self.insee})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0)
        l_localisation_parent = l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 1)

        # Create first children
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}A",
                'insee': self.insee,
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 2)

        # Create second children with same order value (error)
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}B",
                'insee': self.insee,
                'parent': l_localisation_parent.pk
            }
        )
        self.assertFalse(l_form.is_valid(), f"Form is valid !")
        self.assertEqual(len(l_form.errors), 1, f"Unexpected errors quantity ! {l_form.errors}")
        self.assertEqual(len(l_form['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_form['order'].errors[0], "A localisation with this order and parent already exist.", "Error message not expected !")

    def test_parent(self):
        # Create Parent localisation
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER, 'code': self.code, 'insee': self.insee})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0)
        l_localisation_parent = l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 1)

        # Create first children
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}A",
                'insee': self.insee,
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 2)

        # Create second children
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER+1,
                'code': f"{self.code}B",
                'insee': self.insee,
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 3)



    def test_parent_deletion(self):
        """
            Test if Childrens will inherit of parent of their parent
        """
        # Create Top Parent
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER, 'code': self.code, 'insee': self.insee})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0)
        l_localisation_parent = l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 1)

        # Create Mid Parent
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}A",
                'insee': self.insee,
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_mid_parent = l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 2)

        # Create Children 1
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}B",
                'insee': self.insee,
                'parent': l_localisation_mid_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_children_1 = l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 3)

        # Create Children 2
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER+1,
                'code': f"{self.code}C",
                'insee': self.insee,
                'parent': l_localisation_mid_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_children_2 = l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 4)

        # Delete Mid Parent
        l_localisation_mid_parent.delete()
        self.assertEqual(Localisation.objects.all().count(), 3)

        # Update children local queryset
        l_localisation_children_1 = Localisation.objects.get(pk=l_localisation_children_1.pk)
        l_localisation_children_2 = Localisation.objects.get(pk=l_localisation_children_2.pk)

        # Test if parent is now Parent
        self.assertEqual(l_localisation_children_1.parent, l_localisation_parent)
        self.assertEqual(l_localisation_children_2.parent, l_localisation_parent)


    def test_parent_deletion_without_parent_to_replace(self):
        """
            Test if Childrens will inherit of parent of their parent which is None
        """
        # Create Top Parent
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER, 'code': self.code, 'insee': self.insee})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0)
        l_localisation_parent = l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 1)

        # Create Children 1
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}A",
                'insee': self.insee,
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_children_1 = l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 2)

        # Create Children 2
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER+1,
                'code': f"{self.code}B",
                'insee': self.insee,
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_children_2 = l_form.save(user=self.user)
        self.assertEqual(Localisation.objects.all().count(), 3)

        # Delete Parent
        l_localisation_parent.delete()
        self.assertEqual(Localisation.objects.all().count(), 2)

        # Update children local queryset
        l_localisation_children_1 = Localisation.objects.get(pk=l_localisation_children_1.pk)
        l_localisation_children_2 = Localisation.objects.get(pk=l_localisation_children_2.pk)

        # Test if parent is now Parent
        self.assertIsNone(l_localisation_children_1.parent, None)
        self.assertIsNone(l_localisation_children_2.parent, None)


    def test_parent_list(self):
        """
            This test verify that the field Parent choices is human friendly
            and keep order right even for random creation
        """
        # Create Parent 1
        l_form = LocalisationForm(
            data={'code': self.code,
                'insee': self.insee,
                'is_enable': False,
                'parent': None,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_1 = l_form.save(user=self.user)

        # Create Parent 2
        l_form = LocalisationForm(
            data={'code': f"{self.code}A",
                'insee': self.insee,
                'is_enable': False,
                'parent': None,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_2 = l_form.save(user=self.user)

        # Create Children 13
        l_form = LocalisationForm(
            data={'code': f"{self.code}B",
                'insee': self.insee,
                'is_enable': False,
                'parent': l_localisation_1.pk,
                'order': MINIMUM_ORDER+2
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_13 = l_form.save(user=self.user)

        # Create Children 11
        l_form = LocalisationForm(
            data={'code': f"{self.code}C",
                'insee': self.insee,
                'is_enable': False,
                'parent': l_localisation_1.pk,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_11 = l_form.save(user=self.user)

        # Create Children 22
        l_form = LocalisationForm(
            data={'code': f"{self.code}D",
                'insee': self.insee,
                'is_enable': False,
                'parent': l_localisation_2.pk,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_22 = l_form.save(user=self.user)

        # Create Children 12
        l_form = LocalisationForm(
            data={'code': f"{self.code}E",
                'insee': self.insee,
                'is_enable': False,
                'parent': l_localisation_1.pk,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_12 = l_form.save(user=self.user)

        # Create Children 21
        l_form = LocalisationForm(
            data={'code': f"{self.code}F",
                'insee': self.insee,
                'is_enable': False,
                'parent': l_localisation_2.pk,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_21 = l_form.save(user=self.user)

        # Create Children 122
        l_form = LocalisationForm(
            data={'code': f"{self.code}G",
                'insee': self.insee,
                'is_enable': False,
                'parent': l_localisation_12.pk,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_122 = l_form.save(user=self.user)

        # Create Children 121
        l_form = LocalisationForm(
            data={'code': f"{self.code}H",
                'insee': self.insee,
                'is_enable': False,
                'parent': l_localisation_12.pk,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_121 = l_form.save(user=self.user)

        # Check if all required Localisation has been created
        self.assertEqual(len(Localisation.objects.all()), 9, "Form has not been save !")

        # Check display order in form
        for i, pk in enumerate(LocalisationForm().fields['parent'].choices):
            if i==0:
                self.assertEqual(pk, l_localisation_1.pk, f"Unexpected object ! {pk}")
            elif i==1:
                self.assertEqual(pk, l_localisation_11.pk, f"Unexpected object ! {pk}")
            elif i==2:
                self.assertEqual(pk, l_localisation_12.pk, f"Unexpected object ! {pk}")
            elif i==3:
                self.assertEqual(pk, l_localisation_121.pk, f"Unexpected object ! {pk}")
            elif i==4:
                self.assertEqual(pk, l_localisation_122.pk, f"Unexpected object ! {pk}")
            elif i==5:
                self.assertEqual(pk, l_localisation_13.pk, f"Unexpected object ! {pk}")
            elif i==6:
                self.assertEqual(pk, l_localisation_2.pk, f"Unexpected object ! {pk}")
            elif i==7:
                self.assertEqual(pk, l_localisation_21.pk, f"Unexpected object ! {pk}")
            elif i==8:
                self.assertEqual(pk, l_localisation_22.pk, f"Unexpected object ! {pk}")

