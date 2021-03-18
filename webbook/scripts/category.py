from webbook.models import Category, CategoryData, LanguageAvailable
from webbook.models import User
from webbook.forms import CategoryForm, CategoryDataForm
from webbook.scripts import log as Log
import pprint

class CategoryManager():
    _sql_table_name = "annu_cats"
    _categorySql_list = {}
    _categoryMongo_dict = {}

    def deleteCategory():
        Log.info("Deleting all Category from database...")
        Category.objects.all().delete()
        if Category.objects.all().count() != 0:
            Log.fatal(self.__class__.__name__, "Category has not been deleted !")
        if CategoryData.objects.all().count() != 0:
            Log.fatal(self.__class__.__name__, "CategoryData has not been deleted !")
        Log.info("Deleting all Category OK")

    def createCategoryFromSql(self, key, sqlObject, functionnalUser: User):
        # Check if parent is key is not identical as current key
        if key == sqlObject.cat_parent:
            Log.error(self.__class__.__name__, f"Key and Parent key is identical, skip {key} creation !")
            self.error_quantity += 1
            return

        # Find Parent and create it if does not exist
        is_enable = sqlObject.cat_show
        parent = None
        if sqlObject.cat_parent != 0:
            # Check if parent has been created or not
            if sqlObject.cat_parent in self.sqlKeyWithModelAssociation:
                parent = Category.objects.get(pk=self.sqlKeyWithModelAssociation[sqlObject.cat_parent])
            else:
                Log.warning(self.__class__.__name__, f"Impossible to find a parent with key='{sqlObject.cat_parent}', create it !")
                # Check if parent exist on SQL Database
                if sqlObject.cat_parent in self._categorySql_list:
                    self.createCategoryFromSql(key=sqlObject.cat_parent, sqlObject=self._categorySql_list[sqlObject.cat_parent], functionnalUser=functionnalUser)
                else:
                    Log.error(self.__class__.__name__, f"Impossible to find a parent with key='{sqlObject.cat_parent}', skip {key} creation !")
                    self.error_quantity += 1
                    return

        # Check if already exist
        if key in self.sqlKeyWithModelAssociation:
            Log.warning(self.__class__.__name__, f"Category with key='{key}' already exist, skip it !")
            return

        # Create Category
        l_categoryForm = CategoryForm(
            data={
                'is_enable': is_enable,
                'parent': parent,
                'order': self.order
            }
        )
        if l_categoryForm.is_valid() is False:
            Log.fatal(self.__class__.__name__, f"Error on Category with Name='{sqlObject.cat_name}': {l_categoryForm.errors}")
        l_category = l_categoryForm.save(user=functionnalUser)

        # Create CategoryData (FR)
        l_categoryDataForm = CategoryDataForm(
            data={
                'name': sqlObject.cat_name,
                'resume': sqlObject.cat_name,
                'language': LanguageAvailable.FR.value
            }
        )
        if l_categoryDataForm.is_valid(l_category) is False:
            Log.fatal(self.__class__.__name__, f"Error on CategoryDataForm (FR) with Name='{sqlObject.cat_name}' - Key='{key}': {l_categoryDataForm.errors}")
        l_categoryDataForm.save(user=functionnalUser)

        # Create CategoryData (EN)
        l_categoryDataForm = CategoryDataForm(
            data={
                'name': sqlObject.cat_name,
                'resume': sqlObject.cat_name,
                'language': LanguageAvailable.EN.value
            }
        )
        if l_categoryDataForm.is_valid(l_category) is False:
            Log.fatal(self.__class__.__name__, f"Error on CategoryDataForm (EN) with Name='{categorySql.cat_name}' - Key='{key}': {l_categoryDataForm.errors}")
        l_categoryDataForm.save(user=functionnalUser)
        self.sqlKeyWithModelAssociation[key] = l_category.pk
        self.order += 1



    def createCategoryListFromSql(self, sqlObjectList: list, functionnalUser: User):
        # Convert Sql to Python object
        for key, value in sqlObjectList.items():
            self._categorySql_list[key] = self.CategorySql(value)

        if len(self._categorySql_list) == 0:
            Log.fatal(self.__class__.__name__, f"No {self.CategorySql.__class__.__name__} has been created !")
        if len(self._categorySql_list) != len(sqlObjectList):
            Log.fatal(self.__class__.__name__, f"Impossible to create all {CategorySql.__class__.__name__} ! \
                Get {len(self._categorySql_list)} {self.CategorySql.__class__.__name__} instead of {len(sqlObjectList)}")

        # Clean Database
        Category.objects.all().delete()
        if Category.objects.all().count() != 0:
            Log.fatal(self.__class__.__name__, "Impossible to delete all Category in database")

        # Create Category and CategoryData
        self.error_quantity = 0
        self.order = 1
        self.sqlKeyWithModelAssociation = {}
        for key, categorySql in self._categorySql_list.items():
            self.createCategoryFromSql(key, categorySql, functionnalUser)

        category_quantity = Category.objects.all().count()
        categoryData_quantity = CategoryData.objects.all().count()
        Log.info(f"{category_quantity} category and {categoryData_quantity} categoryData has been created")

        if category_quantity != len(sqlObjectList) - self.error_quantity:
            Log.fatal(self.__class__.__name__, f"Waiting {len(sqlObjectList)} less {self.error_quantity} = {len(sqlObjectList) - self.error_quantity} Category , I have {category_quantity}")
        if categoryData_quantity != (len(sqlObjectList) - self.error_quantity)*2:
            Log.fatal(self.__class__.__name__, f"Waiting {len(sqlObjectList)*2} less {self.error_quantity*2} = {(len(sqlObjectList) - self.error_quantity)*2} Category , I have {categoryData_quantity}")



    class CategorySql():
        def __init__(self, sqlObject):
            self.cat_id = sqlObject[0]
            self.cat_name = sqlObject[1]
            self.cat_parent = sqlObject[2]
            self.cat_priority = sqlObject[3]
            self.cat_show = sqlObject[4]
            self.cat_locked = sqlObject[5]
            self.cat_subd_geo = sqlObject[6]
            self.cat_subd_type = sqlObject[7]
            self.cat_color = sqlObject[8]

        def __repr__(self):
            return f"{self.__class__.__name__}: {self.cat_id} - {self.cat_name}"

        def __str__(self):
            return f"""{self.__class__.__name__}: \
cat_id = {self.cat_id}, cat_name = {self.cat_name}, cat_parent = {self.cat_parent}, cat_priority = {self.cat_priority}, \
cat_show = {self.cat_show}, cat_locked = {self.cat_locked}, cat_subd_geo = {self.cat_subd_geo}, cat_color = {self.cat_color}"""
