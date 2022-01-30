from configparser import ConfigParser
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from webbook.models import Category, Localisation, User, Announcement

from time import time
from os.path import abspath, exists

from .sql_object.configParser import parseSqlConfig
from .sql_object.sqlPointer import SqlPointer
from .sql_object import category as SqlCategory
from .sql_object import localisation as SqlLocation
from .sql_object import announcement as SqlAnnouncement

EXPECTED_ANSWER_TO_START = "YES"

SQL_TABLE_CATS = "annu_cats"
SQL_TABLE_SITE = "annu_site"
SQL_TABLE_SITE_APPARTIENT = "annu_site_appartient"

SQL_CONFIG_PATH = abspath("../config/sql_config.ini")

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

    def handle(self, *args, **options):
        tic = time()
        # ------------------------------------
        # Verification
        # ------------------------------------
        # Check if PostGreSql models are empty
        self.stdout.write("[INFO] Vérifying local Database is empty")
        for model in [
            Announcement, Category, Localisation, User
        ]:
            self.check_models_empty(model)
        self.print_ok("Local Database is empty")

        sqlConfigParser = parseSqlConfig(file=SQL_CONFIG_PATH)
        sqlPointer = SqlPointer(sqlConfig=sqlConfigParser)
        self.print_ok("SQL Network established")

        # Read Insee Data
        INSEE_PATH_FOLDER = abspath(sqlConfigParser.get("InseeData", 'folder'))
        if not exists(INSEE_PATH_FOLDER):
            raise CommandError(f"[ERROR] File not found '{INSEE_PATH_FOLDER}' from '{SQL_CONFIG_PATH}' config file.")

        # ------------------------------------
        # Preparation
        # ------------------------------------
        # Creation on a staff user to import
        try:
            IMPORT_ACCOUNT_EMAIL = f"{sqlConfigParser.get('sql_netLiens', 'user')}@netliens.com"
            import_account = User.objects.get(email=IMPORT_ACCOUNT_EMAIL)
        except User.DoesNotExist:
            import_account = User.objects.create(
                email = IMPORT_ACCOUNT_EMAIL,
                password = sqlConfigParser.get('sql_netLiens', 'password'),
                first_name = sqlConfigParser.get('sql_netLiens', 'user'),
                last_name = sqlConfigParser.get('sql_netLiens', 'user'),
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
        self.print_running("Models from SQL Database downloading")
        annu_cats = sqlPointer.getSqlModel(SQL_TABLE_CATS)
        annu_site = sqlPointer.getSqlModel(SQL_TABLE_SITE)
        self.print_ok("Models from SQL Database downloaded")

        # ------------------------------------
        # Creation DB
        # ------------------------------------
        self.print_running(f"Creation of {Category.__name__} in PostgreSql")
        SqlCategory.conversion(annu_cats, import_account)
        self.print_ok(f"{Category.objects.all().count()} {Category.__name__}/{len(annu_cats)} imported.")

        self.print_running(f"Creation of {Localisation.__name__} in PostgreSql")
        SqlLocation.generateModels(import_account, INSEE_PATH_FOLDER, sqlConfigParser)
        self.print_ok(f"{Localisation.objects.all().count()} {Localisation.__name__} imported.")

        self.print_running(f"Creation of {Announcement.__name__} in PostgreSql")
        SqlAnnouncement.conversion(annu_site, SQL_TABLE_SITE_APPARTIENT, sqlPointer, import_account)
        self.print_ok(f"{Announcement.objects.all().count()} {Announcement.__name__}/{len(annu_site)} imported.")
        self.print_ok(f"{User.objects.all().count()} {User.__name__} created.")

        # ------------------------------------
        # End
        # ------------------------------------
        toc = time()
        self.stdout.write(f"[INFO] Command finished in {int(round((toc - tic)))} s")
