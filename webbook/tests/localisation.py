from django.test import TestCase
from django.test import Client
from django.core.exceptions import ObjectDoesNotExist

from webbook.models import Localisation, LocalisationData, MINIMUM_ORDER, TITLE_MAX_LENGTH, MAX_CODE_LENGTH
from webbook.forms import LocalisationForm

class LocalisationFormTestCase(TestCase):
    """ 
        -----------------------------------------
        LocalisationFormTestCase tests
        -----------------------------------------
    """

    def setUp(self):
        self.code = "ABCD"
        self.is_enable = False
        self.parent = None
        self.order = 1


    def test_valid(self):
        l_localisation = LocalisationForm(
            data={'code': self.code,
                'is_enable': self.is_enable,
                'parent': self.parent,
                'order': self.order
            }
        )
        self.assertTrue(l_localisation.is_valid(), "Form is not valid !")
        self.assertEqual(Localisation.objects.all().count(), 0, "An object already exist !")
        l_localisation.save()
        self.assertEqual(Localisation.objects.all().count(), 1, "Object has not been save !")
        l_localisation = Localisation.objects.filter()[0]
        self.assertEqual(l_localisation.code, self.code, "Unexpected value !")
        self.assertEqual(l_localisation.is_enable, self.is_enable, "Unexpected value !")
        self.assertIsNone(l_localisation.parent, "Unexpected value !")
        self.assertEqual(l_localisation.order, self.order, "Unexpected value !")


    def test_invalid_order(self):
        l_form = LocalisationForm(
            data={'code': self.code,
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
        l_form = LocalisationForm(data={'order': MINIMUM_ORDER, 'code': self.code})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0, "An object already exist !")
        l_form.save()

        # Create second localisation with same order value (error)
        l_form = LocalisationForm(data={'order': MINIMUM_ORDER, 'code': f"{self.code}A"})
        self.assertFalse(l_form.is_valid(), f"Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_form['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_form['order'].errors[0], "A localisation with this order and parent already exist.", "Error message not expected !")


    def test_invalid_code(self):
        # Empty Code
        l_form = LocalisationForm(data={'code': "",
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertFalse(l_form.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_form['code'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['code'].errors[0], "This field is required.", "Error message not expected !")

        # Code too long
        l_form = LocalisationForm(data={'code': "1" * (MAX_CODE_LENGTH+1),
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertFalse(l_form.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_form['code'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['code'].errors[0], f"Ensure this value has at most {MAX_CODE_LENGTH} characters (it has {MAX_CODE_LENGTH+1}).", "Error message not expected !")


    def test_unique_code(self):
        # Create first valid localisation
        l_form = LocalisationForm(data={'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0, "An object already exist !")
        l_form.save()

        # Create second localisation with same code as previous
        l_form = LocalisationForm(data={'code': self.code,
                                                'is_enable': self.is_enable,
                                                'parent': self.parent,
                                                'order': self.order})
        self.assertFalse(l_form.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_form['code'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_form['code'].errors[0], f"Localisation with this Code already exists.")


    def test_unique_order_with_children(self):
        # Create Parent localisation
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER, 'code': self.code})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0)
        l_localisation_parent = l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 1)

        # Create first children
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}A",
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 2)

        # Create second children with same order value (error)
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}B",
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
            data={'order': MINIMUM_ORDER, 'code': self.code})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0)
        l_localisation_parent = l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 1)

        # Create first children
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}A",
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 2)

        # Create second children
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER+1,
                'code': f"{self.code}B",
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 3)



    def test_parent_deletion(self):
        """
            Test if Childrens will inherit of parent of their parent
        """
        # Create Top Parent
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER, 'code': self.code})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0)
        l_localisation_parent = l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 1)

        # Create Mid Parent
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}A",
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_mid_parent = l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 2)

        # Create Children 1
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}B",
                'parent': l_localisation_mid_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_children_1 = l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 3)

        # Create Children 2
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER+1,
                'code': f"{self.code}C",
                'parent': l_localisation_mid_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_children_2 = l_form.save()
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
            data={'order': MINIMUM_ORDER, 'code': self.code})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Localisation.objects.all().count(), 0)
        l_localisation_parent = l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 1)

        # Create Children 1
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER,
                'code': f"{self.code}A",
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_children_1 = l_form.save()
        self.assertEqual(Localisation.objects.all().count(), 2)

        # Create Children 2
        l_form = LocalisationForm(
            data={'order': MINIMUM_ORDER+1,
                'code': f"{self.code}B",
                'parent': l_localisation_parent.pk
            }
        )
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_localisation_children_2 = l_form.save()
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
                'is_enable': False,
                'parent': None,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_1 = l_form.save()

        # Create Parent 2
        l_form = LocalisationForm(
            data={'code': f"{self.code}A",
                'is_enable': False,
                'parent': None,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_2 = l_form.save()

        # Create Children 13
        l_form = LocalisationForm(
            data={'code': f"{self.code}B",
                'is_enable': False,
                'parent': l_localisation_1.pk,
                'order': MINIMUM_ORDER+2
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_13 = l_form.save()

        # Create Children 11
        l_form = LocalisationForm(
            data={'code': f"{self.code}C",
                'is_enable': False,
                'parent': l_localisation_1.pk,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_11 = l_form.save()

        # Create Children 22
        l_form = LocalisationForm(
            data={'code': f"{self.code}D",
                'is_enable': False,
                'parent': l_localisation_2.pk,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_22 = l_form.save()

        # Create Children 12
        l_form = LocalisationForm(
            data={'code': f"{self.code}E",
                'is_enable': False,
                'parent': l_localisation_1.pk,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_12 = l_form.save()

        # Create Children 21
        l_form = LocalisationForm(
            data={'code': f"{self.code}F",
                'is_enable': False,
                'parent': l_localisation_2.pk,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_21 = l_form.save()

        # Create Children 122
        l_form = LocalisationForm(
            data={'code': f"{self.code}G",
                'is_enable': False,
                'parent': l_localisation_12.pk,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_122 = l_form.save()

        # Create Children 121
        l_form = LocalisationForm(
            data={'code': f"{self.code}H",
                'is_enable': False,
                'parent': l_localisation_12.pk,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_localisation_121 = l_form.save()

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

