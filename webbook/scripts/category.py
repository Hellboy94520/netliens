from webbook.models import Category, CategoryData, LanguageAvailable
from webbook.scripts import log as Log

class CategoryManager():
    sql_table_name = "annu_cats"
    categorySql_list = {}
    categoryMongo_dict = {}

    def deleteCategory():
        Category.objects.all().delete()

    def createCategoryFromSql(self, sqlObjectList: list):
        # Convert Sql to Python object
        for key, value in sqlObjectList.items():
            self.categorySql_list[key] = self.CategorySql(value)

        if len(self.categorySql_list) == 0:
            Log.fatal(self.__class__.__name__, f"No {self.CategorySql.__class__.__name__} has been created !")
        if len(self.categorySql_list) != len(sqlObjectList):
            Log.fatal(self.__class__.__name__, f"Impossible to create all {CategorySql.__class__.__name__} ! \
                Get {len(self.categorySql_list)} {self.CategorySql.__class__.__name__} instead of {len(sqlObjectList)}")

        # Clean Database
        Log.info("Deleting all Category from database...")
        Category.objects.all().delete()
        if Category.objects.all().count() != 0:
            Log.fatal(self.__class__.__name__, "Impossible to delete all Category in database")

        # Create Category and CategoryData without order and parent
        for key, categorySql in self.categorySql_list.items():
            l_categoryMongo = Category.objects.create(
                    is_enable = categorySql.cat_show,
                    parent = None,
                    order = 0
                )
            self.categoryMongo_dict[key] = l_categoryMongo
            CategoryData.objects.create(
                name = categorySql.cat_name,
                resume = "",
                language = LanguageAvailable.FR.value,
                category = l_categoryMongo
            )
            CategoryData.objects.create(
                name = categorySql.cat_name,
                resume = "",
                language = LanguageAvailable.EN.value,
                category = l_categoryMongo
            )

        # Check Data
        if Category.objects.all().count() == 0:
            Log.fatal(self.__class__.__name__, f"No Category has been created !")
        if Category.objects.all().count() != len(sqlObjectList):
            Log.fatal(self.__class__.__name__, f"Impossible to create all Category ! \
                Get {Category.objects.all().count()} Category instead of {len(sqlObjectList)}")
        if CategoryData.objects.all().count() == 0:
            Log.fatal(self.__class__.__name__, f"No CategoryData has been created !")
        if CategoryData.objects.all().count() != len(sqlObjectList) * LanguageAvailable.size():
            Log.fatal(self.__class__.__name__, f"Impossible to create all CategoryData ! \
                Get {CategoryData.objects.all().count()} CategoryData instead of {len(sqlObjectList)}")

        Log.info(f"{Category.objects.all().count()} category and {CategoryData.objects.all().count()} categoryData has been created")

        # Add parent to Category
        for key, categorySql in self.categorySql_list.items():
            l_categoryParent = self.categoryMongo_dict.get(categorySql.cat_parent, None)
            if categorySql.cat_parent != 0 and l_categoryParent is None:
                Log.error(self.__class__.__name__, f"Parent with id={categorySql.cat_parent} not found for Category {categorySql.cat_id}, set is_enabled variable to False !")
                self.categoryMongo_dict.get(key).is_enable = False
            self.categoryMongo_dict.get(key).parent = l_categoryParent
            self.categoryMongo_dict.get(key).save()

        #TODO: Add order in Category function of Parent

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
