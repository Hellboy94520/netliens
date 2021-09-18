from django.test import TestCase

from webbook.models import get_all_model_in_order, get_all_modelWithData_in_order, get_all_modelDataWithPosition_in_order
from webbook.models import Category, CategoryData
from webbook.models import LanguageAvailable

class CategoryModel(TestCase):
    def createCategoryWithData(self, **kwargs):
        category = Category.objects.create(
            is_enable=True,
            parent=kwargs['parent'],
            order=kwargs['order']
        )
        categoryDataFr = CategoryData.objects.create(
            name=kwargs['name'],
            resume=kwargs['resume'],
            category=category,
            language=LanguageAvailable.FR.value
        )
        categoryDataEn = CategoryData.objects.create(
            name=kwargs['name'],
            resume=kwargs['resume'],
            category=category,
            language=LanguageAvailable.EN.value
        )
        return category, categoryDataFr, categoryDataEn

    def initCategoryWithDataForTest(self):
        # Creation random category
        self.category_2, self.category_2_fr, self.category_2_en = self.createCategoryWithData(
            parent=None,
            order=2,
            name="Category 2",
            resume="Category 2"
        )
        self.category_22, self.category_22_fr, self.category_22_en = self.createCategoryWithData(
            parent=self.category_2,
            order=2,
            name="Category 22",
            resume="Category 22"
        )
        self.category_21, self.category_21_fr, self.category_21_en = self.createCategoryWithData(
            parent=self.category_2,
            order=1,
            name="Category 21",
            resume="Category 21"
        )

        self.category_1, self.category_1_fr, self.category_1_en = self.createCategoryWithData(
            parent=None,
            order=1,
            name="Category 1",
            resume="Category 1"
        )
        self.category_12, self.category_12_fr, self.category_12_en = self.createCategoryWithData(
            parent=self.category_1,
            order=2,
            name="Category 12",
            resume="Category 12"
        )
        self.category_11, self.category_11_fr, self.category_11_en = self.createCategoryWithData(
            parent=self.category_1,
            order=1,
            name="Category 11",
            resume="Category 11"
        )
        self.category_112, self.category_112_fr, self.category_112_en = self.createCategoryWithData(
            parent=self.category_11,
            order=2,
            name="Category 112",
            resume="Category 112"
        )
        self.category_111, self.category_111_fr, self.category_111_en = self.createCategoryWithData(
            parent=self.category_11,
            order=1,
            name="Category 111",
            resume="Category 111"
        )

        # Check creation
        self.category_total = 8
        self.assertEqual(Category.objects.all().count(), self.category_total)
        self.assertEqual(CategoryData.objects.all().count(), self.category_total*2)



    def test_get_all_category_in_order(self):
        # Create random category
        self.initCategoryWithDataForTest()

        # Validate function
        category_list = get_all_model_in_order(model=Category)
        self.assertEqual(len(category_list), self.category_total)
        for i, category in enumerate(category_list):
            if i==0:
                self.assertEqual(category, self.category_1.pk)
            if i==1:
                self.assertEqual(category, self.category_11.pk)
            if i==2:
                self.assertEqual(category, self.category_111.pk)
            if i==3:
                self.assertEqual(category, self.category_112.pk)
            if i==4:
                self.assertEqual(category, self.category_12.pk)
            if i==5:
                self.assertEqual(category, self.category_2.pk)
            if i==6:
                self.assertEqual(category, self.category_21.pk)
            if i==7:
                self.assertEqual(category, self.category_22.pk)

    def test_get_all_categoryWithData_in_order(self):
        # Create random category
        self.initCategoryWithDataForTest()

        # Validate function
        category_map_fr = get_all_modelWithData_in_order(
            model=Category,
            language=LanguageAvailable.FR.value
        )
        category_map_en = get_all_modelWithData_in_order(
            model=Category,
            language=LanguageAvailable.EN.value
        )
        self.assertEqual(len(category_map_fr), self.category_total)
        self.assertEqual(len(category_map_en), self.category_total)

        for i, category in enumerate(category_map_fr):
            if i==0:
                self.assertEqual(category_map_fr[category], self.category_1_fr)
                self.assertEqual(category_map_en[category], self.category_1_en)
            if i==1:
                self.assertEqual(category_map_fr[category], self.category_11_fr)
                self.assertEqual(category_map_en[category], self.category_11_en)
            if i==2:
                self.assertEqual(category_map_fr[category], self.category_111_fr)
                self.assertEqual(category_map_en[category], self.category_111_en)
            if i==3:
                self.assertEqual(category_map_fr[category], self.category_112_fr)
                self.assertEqual(category_map_en[category], self.category_112_en)
            if i==4:
                self.assertEqual(category_map_fr[category], self.category_12_fr)
                self.assertEqual(category_map_en[category], self.category_12_en)
            if i==5:
                self.assertEqual(category_map_fr[category], self.category_2_fr)
                self.assertEqual(category_map_en[category], self.category_2_en)
            if i==6:
                self.assertEqual(category_map_fr[category], self.category_21_fr)
                self.assertEqual(category_map_en[category], self.category_21_en)
            if i==7:
                self.assertEqual(category_map_fr[category], self.category_22_fr)
                self.assertEqual(category_map_en[category], self.category_22_en)

    def test_get_all_categoryDataWithPosition_in_order(self):
        # Create random category
        self.initCategoryWithDataForTest()

        # Validate function
        category_map_fr = get_all_modelDataWithPosition_in_order(
            model=Category,
            language=LanguageAvailable.FR.value
        )
        category_map_en = get_all_modelDataWithPosition_in_order(
            model=Category,
            language=LanguageAvailable.EN.value
        )
        self.assertEqual(len(category_map_fr), self.category_total)

        for i, category in enumerate(category_map_fr):
            if i==0:
                self.assertEqual(category, self.category_1)
                self.assertEqual(category_map_fr[category][0], self.category_1_fr)
                self.assertEqual(category_map_en[category][0], self.category_1_en)
                self.assertEqual(category_map_fr[category][1], 0)
                self.assertEqual(category_map_en[category][1], 0)
            if i==1:
                self.assertEqual(category, self.category_11)
                self.assertEqual(category_map_fr[category][0], self.category_11_fr)
                self.assertEqual(category_map_en[category][0], self.category_11_en)
                self.assertEqual(category_map_fr[category][1], 1)
                self.assertEqual(category_map_en[category][1], 1)
            if i==2:
                self.assertEqual(category, self.category_111)
                self.assertEqual(category_map_fr[category][0], self.category_111_fr)
                self.assertEqual(category_map_en[category][0], self.category_111_en)
                self.assertEqual(category_map_fr[category][1], 2)
                self.assertEqual(category_map_en[category][1], 2)
            if i==3:
                self.assertEqual(category, self.category_112)
                self.assertEqual(category_map_fr[category][0], self.category_112_fr)
                self.assertEqual(category_map_en[category][0], self.category_112_en)
                self.assertEqual(category_map_fr[category][1], 2)
                self.assertEqual(category_map_en[category][1], 2)
            if i==4:
                self.assertEqual(category, self.category_12)
                self.assertEqual(category_map_fr[category][0], self.category_12_fr)
                self.assertEqual(category_map_en[category][0], self.category_12_en)
                self.assertEqual(category_map_fr[category][1], 1)
                self.assertEqual(category_map_en[category][1], 1)
            if i==5:
                self.assertEqual(category, self.category_2)
                self.assertEqual(category_map_fr[category][0], self.category_2_fr)
                self.assertEqual(category_map_en[category][0], self.category_2_en)
                self.assertEqual(category_map_fr[category][1], 0)
                self.assertEqual(category_map_en[category][1], 0)
            if i==6:
                self.assertEqual(category, self.category_21)
                self.assertEqual(category_map_fr[category][0], self.category_21_fr)
                self.assertEqual(category_map_en[category][0], self.category_21_en)
                self.assertEqual(category_map_fr[category][1], 1)
                self.assertEqual(category_map_en[category][1], 1)
            if i==7:
                self.assertEqual(category, self.category_22)
                self.assertEqual(category_map_fr[category][0], self.category_22_fr)
                self.assertEqual(category_map_en[category][0], self.category_22_en)
                self.assertEqual(category_map_fr[category][1], 1)
                self.assertEqual(category_map_en[category][1], 1)

