from webbook.models import Category, CategoryData, LanguageAvailable
from webbook.forms import CategoryForm, CategoryDataForm
from webbook.scripts.common import Manager, ManagerSqlObject
from webbook.models.user import User

class CategoryManager(Manager):
    sqlTableName = "annu_cats"

    def __init__(self):
        super(CategoryManager, self).__init__(
            className = self.__class__.__name__,
            model = Category,
            modelData = CategoryData,
            modelSql = self.CategorySql
        )


    class CategorySql(ManagerSqlObject):
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

    def createModelFromSql(self, key, sqlObject, sqlObjectMap, functionnalUser: User, *args, **kwargs):
        # Check if parent is key is not identical as current key
        if key == sqlObject.cat_parent:
            self.logging.error(f"Key and Parent key is identical, skip {key} creation !")
            self.error += 1
            return

        # Find Parent and create it if does not exist
        is_enable = sqlObject.cat_show
        parent = None
        if sqlObject.cat_parent != 0:
            # Check if parent has been created or not
            parent = Category.objects.filter(order=sqlObject.cat_parent)
            if parent.count() > 0:
                parent = parent[0]
            else:
                self.logging.debug(f"No parent find with key='{sqlObject.cat_parent}', try to create it...")
                # Check if parent exist on SQL Database
                if sqlObject.cat_parent in sqlObjectMap:
                    self.createModelFromSql(
                        key=sqlObject.cat_parent,
                        sqlObject=sqlObjectMap[sqlObject.cat_parent],
                        sqlObjectMap=sqlObjectMap,
                        functionnalUser=functionnalUser)
                    parent = Category.objects.get(order=sqlObject.cat_parent)
                else:
                    self.logging.error(f"No parent find a parent with key='{sqlObject.cat_parent}' on SqlDatabase, skip key='{key}' creation !")
                    self.error += 1
                    return

        # Check if already exist
        if Category.objects.filter(order=key).count() > 0:
            self.logging.debug(f"Category with key='{key}' already exist, skip it !")
            return

        # Create Category
        l_categoryForm = CategoryForm(
            data={
                'is_enable': is_enable,
                'parent': parent,
                'order': key
            }
        )
        if l_categoryForm.is_valid() is False:
            self.critical(f"Error on Category with Name='{sqlObject.cat_name}': {l_categoryForm.errors}")
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
            self.logging.critical.fatal(f"Error on CategoryDataForm (FR) with Name='{sqlObject.cat_name}' - Key='{key}': {l_categoryDataForm.errors}")
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
            self.logging.critical.fatal(f"Error on CategoryDataForm (EN) with Name='{categorySql.cat_name}' - Key='{key}': {l_categoryDataForm.errors}")
        l_categoryDataForm.save(user=functionnalUser)

