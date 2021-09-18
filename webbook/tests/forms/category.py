from django.test import TestCase

from webbook.models import Category, CategoryData, MINIMUM_ORDER, TITLE_MAX_LENGTH
from webbook.forms import CategoryForm, CategoryDataForm

from webbook.models import LanguageAvailable, User

class CategoryForm(TestCase):
    """
        -----------------------------------------
        CategoryFormTestCase tests
        -----------------------------------------
    """
    def setUp(self):
        self.default_is_enable = False
        self.is_enable = True
        self.parent = None
        self.order = 1
        self.user = User.objects.create(email='toto', password='titi')


    def test_user_valid(self):
        l_form = CategoryForm(
            data={
                'parent': self.parent,
                'order': self.order})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Category.objects.all().count(), 0, "An object already exist !")
        l_form.save(user=self.user)
        # Check Category
        self.assertEqual(Category.objects.all().count(), 1, "Object has not been save !")
        l_category = Category.objects.filter()[0]
        self.assertEqual(l_category.is_enable, self.default_is_enable)
        self.assertIsNone(l_category.parent)
        self.assertEqual(l_category.order, self.order)
        # Check CategoryStat
        l_category_stat = l_category.get_statistics()
        self.assertIsNotNone(l_category_stat, "Stats does not exist !")
        self.assertIsNotNone(l_category_stat.date_creation)
        self.assertEqual(l_category_stat.user_creation, self.user)
        self.assertIsNone(l_category_stat.date_validation)
        self.assertIsNone(l_category_stat.user_validation)


    def test_admin_valid(self):
        l_form = CategoryForm(
            data={
                'is_enable': self.is_enable,
                'parent': self.parent,
                'order': self.order})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Category.objects.all().count(), 0, "An object already exist !")
        l_form.save(user=self.user)
        # Check Category
        self.assertEqual(Category.objects.all().count(), 1, "Object has not been save !")
        l_category = Category.objects.filter()[0]
        self.assertEqual(l_category.is_enable, self.is_enable)
        self.assertIsNone(l_category.parent, "Unexpected value !")
        self.assertEqual(l_category.order, self.order, "Unexpected value !")
        # Check CategoryStat
        l_category_stat = l_category.get_statistics()
        self.assertIsNotNone(l_category_stat, "Stats does not exist !")
        self.assertIsNotNone(l_category_stat.date_creation)
        self.assertEqual(l_category_stat.user_creation, self.user)
        self.assertIsNotNone(l_category_stat.date_validation)
        self.assertEqual(l_category_stat.user_validation, self.user)


    def test_invalid_order(self):
        l_form = CategoryForm(data={'is_enable': self.is_enable,
                                    'parent': self.parent,
                                    'order': MINIMUM_ORDER-1})
        self.assertFalse(l_form.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_form.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_form['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_form['order'].errors[0], f"Ensure this value is greater than or equal to {MINIMUM_ORDER}.", "Error message not expected !")


    def test_unique_order(self):
        # Create first category
        l_form = CategoryForm(data={'order': MINIMUM_ORDER})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Category.objects.all().count(), 0, "An object already exist !")
        l_form.save(user=self.user)

        # Create second category with same order value (error)
        l_form = CategoryForm(data={'order': MINIMUM_ORDER})
        self.assertFalse(l_form.is_valid(), f"Form is valid !")
        self.assertEqual(len(l_form.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_form['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_form['order'].errors[0], "A category with this order and parent already exist.", "Error message not expected !")


    def test_unique_order_with_children(self):
        # Create Parent category
        l_form = CategoryForm(data={'order': MINIMUM_ORDER})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Category.objects.all().count(), 0)
        l_category_parent = l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 1)

        # Create first children
        l_form = CategoryForm(data={'order': MINIMUM_ORDER,
                                    'parent': l_category_parent.pk})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 2)

        # Create second children with same order value (error)
        l_form = CategoryForm(data={'order': MINIMUM_ORDER,
                                    'parent': l_category_parent.pk})
        self.assertFalse(l_form.is_valid(), f"Form is valid !")
        self.assertEqual(len(l_form.errors), 1, f"Unexpected errors quantity ! {l_form.errors}")
        self.assertEqual(len(l_form['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_form['order'].errors[0], "A category with this order and parent already exist.", "Error message not expected !")


    def test_parent(self):
        # Create Parent category
        l_form = CategoryForm(data={'order': MINIMUM_ORDER})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Category.objects.all().count(), 0)
        l_category_parent = l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 1)

        # Create first children
        l_form = CategoryForm(data={'order': MINIMUM_ORDER,
                                    'parent': l_category_parent.pk})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 2)

        # Create second children
        l_form = CategoryForm(data={'order': MINIMUM_ORDER+1,
                                    'parent': l_category_parent.pk})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 3)


    def test_parent_deletion(self):
        """
            Test if Childrens will inherit of parent of their parent
        """
        # Create Top Parent
        l_form = CategoryForm(data={'order': MINIMUM_ORDER})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Category.objects.all().count(), 0)
        l_category_parent = l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 1)

        # Create Mid Parent
        l_form = CategoryForm(data={'order': MINIMUM_ORDER,
                                    'parent': l_category_parent.pk})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_mid_parent = l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 2)

        # Create Children 1
        l_form = CategoryForm(data={'order': MINIMUM_ORDER,
                                    'parent': l_mid_parent.pk})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_children_1 = l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 3)

        # Create Children 2
        l_form = CategoryForm(data={'order': MINIMUM_ORDER+1,
                                    'parent': l_mid_parent.pk})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_children_2 = l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 4)

        # Delete Mid Parent
        l_mid_parent.delete()
        self.assertEqual(Category.objects.all().count(), 3)

        # Update children local queryset
        l_children_1 = Category.objects.get(pk=l_children_1.pk)
        l_children_2 = Category.objects.get(pk=l_children_2.pk)

        # Test if parent is now Parent
        self.assertEqual(l_children_1.parent, l_category_parent)
        self.assertEqual(l_children_2.parent, l_category_parent)

    def test_parent_deletion_without_parent_to_replace(self):
        """
            Test if Childrens will inherit of parent of their parent which is None
        """
        # Create Top Parent
        l_form = CategoryForm(data={'order': MINIMUM_ORDER})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(Category.objects.all().count(), 0)
        l_category_parent = l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 1)

        # Create Children 1
        l_form = CategoryForm(data={'order': MINIMUM_ORDER,
                                    'parent': l_category_parent.pk})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_children_1 = l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 2)

        # Create Children 2
        l_form = CategoryForm(data={'order': MINIMUM_ORDER+1,
                                    'parent': l_category_parent.pk})
        self.assertTrue(l_form.is_valid(), f"Form is not valid ! {l_form.errors}")
        l_children_2 = l_form.save(user=self.user)
        self.assertEqual(Category.objects.all().count(), 3)

        # Delete Parent
        l_category_parent.delete()
        self.assertEqual(Category.objects.all().count(), 2)

        # Update children local queryset
        l_children_1 = Category.objects.get(pk=l_children_1.pk)
        l_children_2 = Category.objects.get(pk=l_children_2.pk)

        # Test if parent is now Parent
        self.assertIsNone(l_children_1.parent, None)
        self.assertIsNone(l_children_2.parent, None)


    def test_parent_list(self):
        """
            This test verify that the field Parent choices is human friendly
            and keep order right even for random creation
        """
        # Create Parent 1
        l_form = CategoryForm(
            data={'is_enable': False,
                'parent': None,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_category_1 = l_form.save(user=self.user)

        # Create Parent 2
        l_form = CategoryForm(
            data={'is_enable': False,
                'parent': None,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_category_2 = l_form.save(user=self.user)

        # Create Children 13
        l_form = CategoryForm(
            data={'is_enable': False,
                'parent': l_category_1.pk,
                'order': MINIMUM_ORDER+2
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_category_13 = l_form.save(user=self.user)

        # Create Children 11
        l_form = CategoryForm(
            data={'is_enable': False,
                'parent': l_category_1.pk,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_category_11 = l_form.save(user=self.user)

        # Create Children 22
        l_form = CategoryForm(
            data={'is_enable': False,
                'parent': l_category_2.pk,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_category_22 = l_form.save(user=self.user)

        # Create Children 12
        l_form = CategoryForm(
            data={'is_enable': False,
                'parent': l_category_1.pk,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_category_12 = l_form.save(user=self.user)

        # Create Children 21
        l_form = CategoryForm(
            data={'is_enable': False,
                'parent': l_category_2.pk,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_category_21 = l_form.save(user=self.user)

        # Create Children 122
        l_form = CategoryForm(
            data={'is_enable': False,
                'parent': l_category_12.pk,
                'order': MINIMUM_ORDER+1
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_category_122 = l_form.save(user=self.user)

        # Create Children 121
        l_form = CategoryForm(
            data={'is_enable': False,
                'parent': l_category_12.pk,
                'order': MINIMUM_ORDER
            }
        )
        self.assertTrue(l_form.is_valid(), "Form is not valid !")
        l_category_121 = l_form.save(user=self.user)

        # Check if all required Category has been created
        self.assertEqual(len(Category.objects.all()), 9, "Form has not been save !")

        # Check display order in form
        for i, pk in enumerate(CategoryForm().fields['parent'].choices):
            if i==0:
                self.assertEqual(pk, l_category_1.pk, f"Unexpected object ! {pk}")
            elif i==1:
                self.assertEqual(pk, l_category_11.pk, f"Unexpected object ! {pk}")
            elif i==2:
                self.assertEqual(pk, l_category_12.pk, f"Unexpected object ! {pk}")
            elif i==3:
                self.assertEqual(pk, l_category_121.pk, f"Unexpected object ! {pk}")
            elif i==4:
                self.assertEqual(pk, l_category_122.pk, f"Unexpected object ! {pk}")
            elif i==5:
                self.assertEqual(pk, l_category_13.pk, f"Unexpected object ! {pk}")
            elif i==6:
                self.assertEqual(pk, l_category_2.pk, f"Unexpected object ! {pk}")
            elif i==7:
                self.assertEqual(pk, l_category_21.pk, f"Unexpected object ! {pk}")
            elif i==8:
                self.assertEqual(pk, l_category_22.pk, f"Unexpected object ! {pk}")


class CategoryDataForm(TestCase):
    """
        -----------------------------------------
        CategoryDataFormTestCase tests
        -----------------------------------------
    """

    def setUp(self):
        # Create a default Category Form
        self.category = Category.objects.create()
        self.name_fr = "Catégorie"
        self.resume_fr = "Ceci est une catégorie !"
        self.language_fr = LanguageAvailable.FR.value
        self.name_en = "Category"
        self.resume_en = "This is a category !"
        self.language_en = LanguageAvailable.EN.value


    def test_valid_en(self):
        l_form = CategoryDataForm(
            data={'name': self.name_en,
                'resume': self.resume_en,
                'language': self.language_en
            }
        )
        self.assertTrue(l_form.is_valid(self.category), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(CategoryData.objects.all().count(), 0)
        l_object = l_form.save()
        self.assertEqual(CategoryData.objects.all().count(), 1)
        self.assertEqual(l_object.name, self.name_en)
        self.assertEqual(l_object.resume, self.resume_en)
        self.assertEqual(l_object.language, self.language_en)


    def test_valid_fr(self):
        l_form = CategoryDataForm(
            data={'name': self.name_fr,
                'resume': self.resume_fr,
                'language': self.language_fr
            }
        )
        self.assertTrue(l_form.is_valid(self.category), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(CategoryData.objects.all().count(), 0)
        l_object = l_form.save()
        self.assertEqual(CategoryData.objects.all().count(), 1)
        self.assertEqual(l_object.name, self.name_fr)
        self.assertEqual(l_object.resume, self.resume_fr)
        self.assertEqual(l_object.language, self.language_fr)


    def test_invalid_name(self):
        error_field = 'name'

        # Empty Field
        l_form = CategoryDataForm(
            data={'name': "",
                'resume': self.resume_fr,
                'language': self.language_fr
            }
        )
        self.assertFalse(l_form.is_valid(self.category), f"Form is valid !")
        self.assertEqual(CategoryData.objects.all().count(), 0)
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_form[error_field].errors), 1, f"Expected only 1 error for '{error_field}' field !")
        self.assertEqual(l_form[error_field].errors[0], "This field is required.", "Error message not expected !")

        # Field too large
        l_form = CategoryDataForm(
            data={'name': "s" * (TITLE_MAX_LENGTH+1),
                'resume': self.resume_en,
                'language': self.language_en
            }
        )
        self.assertFalse(l_form.is_valid(self.category), f"Form is valid !")
        self.assertEqual(CategoryData.objects.all().count(), 0)
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_form[error_field].errors), 1, f"Expected only 1 error for '{error_field}' field !")
        self.assertEqual(l_form[error_field].errors[0], f"Ensure this value has at most {TITLE_MAX_LENGTH} characters (it has {TITLE_MAX_LENGTH+1}).", "Error message not expected !")


    def test_resume(self):
        error_field = 'resume'

        # Empty Field
        l_form = CategoryDataForm(
            data={'name': self.name_fr,
                'resume': "",
                'language': self.language_fr
            }
        )
        self.assertFalse(l_form.is_valid(self.category), f"Form is valid !")
        self.assertEqual(CategoryData.objects.all().count(), 0)
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_form[error_field].errors), 1, f"Expected only 1 error for '{error_field}' field !")
        self.assertEqual(l_form[error_field].errors[0], "This field is required.", "Error message not expected !")


    def test_invalid_language(self):
        error_field = 'language'

        # Empty Language
        l_form = CategoryDataForm(
            data={'name': self.name_fr,
                'resume': self.resume_fr,
                'language': ""
            }
        )
        self.assertFalse(l_form.is_valid(self.category), f"Form is valid !")
        self.assertEqual(CategoryData.objects.all().count(), 0)
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_form[error_field].errors), 1, f"Expected only 1 error for '{error_field}' field !")
        self.assertEqual(l_form[error_field].errors[0], "This field is required.", "Error message not expected !")

        # Invalid Language value
        l_language = "ZZ"
        l_form = CategoryDataForm(
            data={'name': self.name_fr,
                'resume': self.resume_fr,
                'language': l_language
            }
        )
        self.assertFalse(l_form.is_valid(self.category), f"Form is valid !")
        self.assertEqual(CategoryData.objects.all().count(), 0)
        self.assertEqual(len(l_form.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_form[error_field].errors), 1, f"Expected only 1 error for '{error_field}' field !")
        self.assertEqual(l_form[error_field].errors[0], f"Select a valid choice. {l_language} is not one of the available choices.", "Error message not expected !")


    def test_unique_language(self):
        error_field = 'language'

        # Generate a valid English Language
        l_form = CategoryDataForm(
            data={'name': self.name_en,
                'resume': self.resume_en,
                'language': self.language_en
            }
        )
        self.assertTrue(l_form.is_valid(self.category), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(CategoryData.objects.all().count(), 0)
        l_form.save()
        self.assertEqual(CategoryData.objects.all().count(), 1)

        # English Language already exist
        l_form = CategoryDataForm(
            data={'name': self.name_en,
                'resume': self.resume_en,
                'language': self.language_en
            }
        )
        self.assertFalse(l_form.is_valid(self.category), f"Form is valid !")
        self.assertEqual(CategoryData.objects.all().count(), 1)
        self.assertEqual(len(l_form.errors), 1, f"Expected only 1 error ! {l_form.errors}")
        self.assertEqual(len(l_form[error_field].errors), 1, f"Expected only 1 error for '{error_field}' field !")
        self.assertEqual(l_form[error_field].errors[0], f"This language already exist for this category.")

    def test_category_delete(self):
        # Create CategoryData associated to Category
        l_form = CategoryDataForm(
            data={'name': self.name_en,
                'resume': self.resume_en,
                'language': self.language_en
            }
        )
        self.assertTrue(l_form.is_valid(self.category), f"Form is not valid ! {l_form.errors}")
        self.assertEqual(CategoryData.objects.all().count(), 0)
        l_object = l_form.save()
        self.assertEqual(CategoryData.objects.all().count(), 1)
        self.assertEqual(Category.objects.all().count(), 1)

        # Delete Category which delete CategoryData
        self.category.delete()
        self.assertEqual(Category.objects.all().count(), 0)
        self.assertEqual(CategoryData.objects.all().count(), 0)
