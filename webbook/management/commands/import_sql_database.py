from configparser import ConfigParser
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from webbook.models import Category, Localisation, User

from time import time
from os.path import abspath, exists
from configparser import ConfigParser, ExtendedInterpolation
import pymysql

from .sql_object import category as SqlCategory
from .sql_object import localisation as SqlLocation

EXPECTED_ANSWER_TO_START = "YES"

SQL_TABLE_CATS = "annu_cats"
SQL_TABLE_DEPT = "annu_dept"
SQL_TABLE_SITE = "annu_site"

class Command(BaseCommand):
    help = 'Import Old Sql Database'

    def print_info(self, msg):
        self.stdout.write(f"[INFO] {msg}.")

    def print_running(self, msg):
        self.stdout.write(f"[RUNNING] {msg}...", ending="\r")

    def print_ok(self, msg):
        self.stdout.write("\033[2K", ending="\r") # Cleaning current line
        self.stdout.write(f"{self.style.SUCCESS('[OK]')} {msg}.")

    def check_models_empty(self, model):
        if model.objects.count() != 0:
            if not settings.DEBUG:
                result = input(f"Model {model.__name__} is not empty, do you want to delete them ? ({EXPECTED_ANSWER_TO_START}/NO)")
                assert result==EXPECTED_ANSWER_TO_START, CommandError(f"[ERROR] {model.__name__} is not empty !")
            self.print_running(f"'{model.__name__}' will be deleted")
            model.objects.all().delete()
            self.print_ok(f"'{model.__name__}' has been deleted")

    def getSqlModel(self, sql_key):
        """
            @params:
            - object: Python object to save on
        """
        with self.connection.cursor() as cursor:
            self.print_running(f"Download '{sql_key}' from Sql Database")
            # dataList = []
            cursor.execute(f"select * from `{sql_key}`")
            self.print_ok(f"'{sql_key}' downloaded")
            return cursor.fetchall()

    def handle(self, *args, **options):
        tic = time()
        # ------------------------------------
        # Verification
        # ------------------------------------
        # Check if PostGreSql models are empty
        self.stdout.write("[INFO] Vérifying local Database is empty")
        for model in [
            Category, Localisation
        ]:
            self.check_models_empty(model)

        self.print_ok("Local Database is empty")

        # Read Sql Database Configuration file
        SQL_CONFIG_PATH = abspath("../config/sql_config.ini")
        self.print_running(f"SQL Configuration file '{SQL_CONFIG_PATH}' opening")
        try:
            sql_config = ConfigParser()
            sql_config._interpolation = ExtendedInterpolation()
            sql_config.read(SQL_CONFIG_PATH)
        except:
            CommandError(f"[ERROR] Impossible to open SQL Configuration file '{SQL_CONFIG_PATH}'")
        self.print_ok(f"SQL Configuration file '{SQL_CONFIG_PATH}' opened")

        # Check if Sql Database Connection is working
        self.print_running("SQL Network connection")
        try:
            self.connection = pymysql.connect(host=sql_config.get('sql_netLiens', 'address'),
                user=sql_config.get('sql_netLiens', 'user'),
                password=sql_config.get('sql_netLiens', 'password'),
                database=sql_config.get('sql_netLiens', 'databasename'),
                cursorclass=pymysql.cursors.DictCursor)
        except:
            raise CommandError(f"[ERROR] SQL Network Failed ({sql_config.get('sql_netLiens', 'address')}")
        self.print_ok("SQL Network established")

        # Read Insee Data
        INSEE_PATH_FOLDER = abspath(sql_config.get("InseeData", 'folder'))
        if not exists(INSEE_PATH_FOLDER):
            raise CommandError(f"[ERROR] Folder not found '{INSEE_PATH_FOLDER}' from '{SQL_CONFIG_PATH}' config file.")

        # ------------------------------------
        # Preparation
        # ------------------------------------
        # Creation on a staff user to import
        try:
            IMPORT_ACCOUNT_EMAIL = f"{sql_config.get('sql_netLiens', 'user')}@netliens.com"
            import_account = User.objects.get(email=IMPORT_ACCOUNT_EMAIL)
        except User.DoesNotExist:
            import_account = User.objects.create(
                email = IMPORT_ACCOUNT_EMAIL,
                password = sql_config.get('sql_netLiens', 'password'),
                first_name = sql_config.get('sql_netLiens', 'user'),
                last_name = sql_config.get('sql_netLiens', 'user'),
                company="NetLiens",
                is_active = True,
                is_staff = True,
                is_superuser = False
            )
        except Exception as e:
            raise CommandError(f"[ERROR] Account '{IMPORT_ACCOUNT_EMAIL}' can not be created/get: {e}")
        self.print_ok(f"Account '{IMPORT_ACCOUNT_EMAIL}' ready")

        # ------------------------------------
        # Import DB
        # ------------------------------------
        annu_cats = self.getSqlModel(SQL_TABLE_CATS)
        annu_dept = self.getSqlModel(SQL_TABLE_DEPT)
        annu_site = self.getSqlModel(SQL_TABLE_SITE)

        # ------------------------------------
        # Creation DB
        # ------------------------------------
        self.print_running(f"Creation of {Category.__name__} in PostgreSql")
        # SqlCategory.conversion(annu_cats, import_account)
        self.print_ok(f"{Category.objects.all().count()} {Category.__name__} imported.")
        self.print_running(f"Creation of {Localisation.__name__} in PostgreSql")
        # SqlLocation.generateModels(import_account, INSEE_PATH_FOLDER, sql_config)
        self.print_ok(f"{Localisation.objects.all().count()} {Localisation.__name__} imported.")

        # ------------------------------------
        # End
        # ------------------------------------
        toc = time()
        self.stdout.write(f"[INFO] Command finished in {int(round((toc - tic)))} s")
