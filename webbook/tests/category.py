from django.test import TestCase
from django.test import Client
from django.core.exceptions import ObjectDoesNotExist

from webbook.models import Category
from webbook.forms import CategoryForm

class CategoryFormTestCase(TestCase):
    def setUp(self):
        self.name = "This is a title !"
        self.resume = "This is an announcement !"
        self.is_enable = False
        self.parent = None
        self.order = 1

    def test_valid(self):
        l_category = CategoryForm(data={'name': self.name,
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': self.parent,
                                        'order': self.order})
        self.assertTrue(l_category.is_valid(), "Form is not valid !")
        self.assertEqual(Category.objects.all().count(), 0, "An object already exist !")
        l_category.save()
        self.assertEqual(Category.objects.all().count(), 1, "Object has not been save !")
        l_category = Category.objects.filter()[0]
        self.assertEqual(l_category.name, self.name, "Unexpected value !")
        self.assertEqual(l_category.resume, self.resume, "Unexpected value !")
        self.assertEqual(l_category.is_enable, self.is_enable, "Unexpected value !")
        self.assertIsNone(l_category.parent, "Unexpected value !")
        self.assertEqual(l_category.order, self.order, "Unexpected value !")

    def test_clean_function(self):
        l_category = CategoryForm(data={'name': self.name,
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': self.parent,
                                        'order': self.order})
        self.assertTrue(l_category.is_valid(), "Form is not valid !")
        self.assertEqual(Category.objects.all().count(), 0, "An object already exist !")
        l_category = l_category.save()
        self.assertEqual(Category.objects.filter(name=self.name).exclude(pk=None).count(), 1)
        self.assertEqual(Category.objects.filter(name=self.name).exclude(pk=l_category.id).count(), 0)

    def test_name(self):
        # Empty Name
        l_category = CategoryForm(data={'name': "",
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': self.parent,
                                        'order': self.order})
        self.assertFalse(l_category.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_category.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_category['name'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_category['name'].errors[0], "This field is required.", "Error message not expected !")

        # Name too long
        l_name_too_long = ""
        l_max_range = 50+1
        for i in range(0, l_max_range):
            l_name_too_long += "_"
        l_category = CategoryForm(data={'name': l_name_too_long,
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': self.parent,
                                        'order': self.order})
        self.assertFalse(l_category.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_category.errors), 1, "Expected only 1 error !")
        self.assertEqual(len(l_category['name'].errors), 1, "Expected only 1 error for this field !")
        self.assertEqual(l_category['name'].errors[0], f"Ensure this value has at most 50 characters (it has {l_max_range}).", "Error message not expected !")

    def test_parent(self):
        l_parent = CategoryForm(data={  'name': "Category Parent",
                                        'resume': "Category Parent",
                                        'is_enable': False,
                                        'parent': None,
                                        'order': 1})
        self.assertTrue(l_parent.is_valid(), "Form is not valid !")
        l_parent.save()
        self.assertEqual(len(Category.objects.all()), 1, "Form has not been save !")
        l_parent = Category.objects.get(name="Category Parent")
        # One children
        l_category = CategoryForm(data={'name': "Children 1",
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': l_parent.id,
                                        'order': 1})
        self.assertTrue(l_category.is_valid(), "Form is not valid !")
        l_category.save()
        self.assertEqual(len(Category.objects.all()), 2, "Form has not been save !")
        # Second children
        l_category = CategoryForm(data={'name': "Children 2",
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': l_parent.pk,
                                        'order': 2})
        self.assertTrue(l_category.is_valid(), "Form is not valid !")
        l_category.save()
        self.assertEqual(len(Category.objects.all()), 3, "Form has not been save !")
        # Children with same parent and order as Children 1
        l_category = CategoryForm(data={'name': "Children 3",
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': l_parent.pk,
                                        'order': 1})
        self.assertFalse(l_category.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_category.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_category['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_category['order'].errors[0], "A category with this order and parent already exist.", "Error message not expected !")
        # Children with same parent and name as Children 1
        l_category = CategoryForm(data={'name': "Children 1",
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': l_parent.pk,
                                        'order': 3})
        self.assertFalse(l_category.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_category.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_category['name'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_category['name'].errors[0], "A category with this name and parent already exist.", "Error message not expected !")
        # Children with same parent, name and order as Children 1
        l_category = CategoryForm(data={'name': "Children 1",
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': l_parent.pk,
                                        'order': 1})
        self.assertFalse(l_category.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_category.errors), 2, "Unexpected errors quantity !")
        self.assertEqual(len(l_category['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_category['order'].errors[0], "A category with this order and parent already exist.")
        self.assertEqual(len(l_category['name'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_category['name'].errors[0], "A category with this name and parent already exist.", "Error message not expected !")
        # Delete parent
        l_parent.delete()
        l_category_1 = Category.objects.get(name="Children 1")
        with self.assertRaises(ObjectDoesNotExist):
            l_category_1.parent
        l_category_2 = Category.objects.get(name="Children 2")
        with self.assertRaises(ObjectDoesNotExist):
            l_category_2.parent

    def test_parent_list(self):
        """
            This test verify init of the form
        """
        # Parent 1
        l_parent = CategoryForm(data={  'name': "Category Parent 1",
                                        'resume': "Category Parent",
                                        'is_enable': False,
                                        'parent': None,
                                        'order': 1})
        self.assertTrue(l_parent.is_valid(), "Form is not valid !")
        l_parent.save()
        l_parent_1 = Category.objects.get(name="Category Parent 1")
        # Parent 2
        l_parent = CategoryForm(data={  'name': "Category Parent 2",
                                        'resume': "Category Parent",
                                        'is_enable': False,
                                        'parent': None,
                                        'order': 2})
        self.assertTrue(l_parent.is_valid(), "Form is not valid !")
        l_parent.save()
        l_parent_2 = Category.objects.get(name="Category Parent 2")
        # Children 11
        l_children = CategoryForm(data={'name': "Category Children 11",
                                        'resume': "Category Parent",
                                        'is_enable': False,
                                        'parent': l_parent_1.pk,
                                        'order': 1})
        self.assertTrue(l_children.is_valid(), "Form is not valid !")
        l_children.save()
        # Children 22
        l_children = CategoryForm(data={'name': "Category Children 22",
                                        'resume': "Category Parent",
                                        'is_enable': False,
                                        'parent': l_parent_2.pk,
                                        'order': 2})
        self.assertTrue(l_children.is_valid(), "Form is not valid !")
        l_children.save()
        # Children 12
        l_children = CategoryForm(data={'name': "Category Children 12",
                                        'resume': "Category Parent",
                                        'is_enable': False,
                                        'parent': l_parent_1.pk,
                                        'order': 2})
        self.assertTrue(l_children.is_valid(), "Form is not valid !")
        l_children.save()
        # Children 21
        l_children = CategoryForm(data={'name': "Category Children 21",
                                        'resume': "Category Parent",
                                        'is_enable': False,
                                        'parent': l_parent_2.pk,
                                        'order': 1})
        self.assertTrue(l_children.is_valid(), "Form is not valid !")
        l_children.save()

        self.assertEqual(len(Category.objects.all()), 6, "Form has not been save !")
        # Children 13
        l_children = CategoryForm(data={'name': "Category Children 13",
                                        'resume': "Category Parent",
                                        'is_enable': False,
                                        'parent': l_parent_1.pk,
                                        'order': 3})
        self.assertTrue(l_children.is_valid(), "Form is not valid !")
        l_children.save()
        l_children = Category.objects.get(name="Category Children 13")
        l_sub_children = CategoryForm(data={'name': "Category Children 133",
                                            'resume': "Category Parent",
                                            'is_enable': False,
                                            'parent': l_children.pk,
                                            'order': 3})
        self.assertTrue(l_sub_children.is_valid(), "Form is not valid !")
        l_sub_children.save()
        l_sub_children = CategoryForm(data={'name': "Category Children 132",
                                            'resume': "Category Parent",
                                            'is_enable': False,
                                            'parent': l_children.pk,
                                            'order': 2})
        self.assertTrue(l_sub_children.is_valid(), "Form is not valid !")
        l_sub_children.save()
        l_sub_children = CategoryForm(data={'name': "Category Children 131",
                                            'resume': "Category Parent",
                                            'is_enable': False,
                                            'parent': l_children.pk,
                                            'order': 1})
        self.assertTrue(l_sub_children.is_valid(), "Form is not valid !")
        l_sub_children.save()

        self.assertEqual(len(Category.objects.all()), 10, "Form has not been save !")
        l_category = CategoryForm()
        for i, pk in enumerate(l_category.fields['parent'].choices):
            if i==0:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Parent 1", "Unexpected object !")
            elif i==1:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Children 11", "Unexpected object !")
            elif i==2:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Children 12", "Unexpected object !")
            elif i==3:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Children 13", "Unexpected object !")
            elif i==4:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Children 131", "Unexpected object !")
            elif i==5:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Children 132", "Unexpected object !")
            elif i==6:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Children 133", "Unexpected object !")
            elif i==7:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Parent 2", "Unexpected object !")
            elif i==8:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Children 21", "Unexpected object !")
            elif i==9:
                self.assertEqual(Category.objects.get(pk=pk).name, "Category Children 22", "Unexpected object !")

    def test_order(self):
        # Null value
        l_category = CategoryForm(data={'name': "Children 1",
                                        'resume': self.resume,
                                        'is_enable': self.is_enable,
                                        'parent': self.parent,
                                        'order': 0})
        self.assertFalse(l_category.is_valid(), "Form is not valid !")
        self.assertEqual(len(l_category.errors), 1, "Unexpected errors quantity !")
        self.assertEqual(len(l_category['order'].errors), 1, "Unexpected errors quantity for this field !")
        self.assertEqual(l_category['order'].errors[0], "Ensure this value is greater than or equal to 1.", "Error message not expected !")
