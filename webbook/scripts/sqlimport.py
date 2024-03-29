from webbook.scripts.sqlconnection import *
from webbook.scripts.category import CategoryManager
from webbook.scripts.localisation import LocalisationManager
from webbook.scripts.announcement import AnnouncementManager
from webbook.models import User
from webbook.scripts.log import create_logger

import os


def readSqlTable(logging, sqlConnection: SqlConnection, sql_table_name: str, order = ""):
    # Variables
    l_table = {}

    # Get all table
    sql_default_command = f"SELECT * FROM `{sql_table_name}`"
    if order:
        sql_default_command += f"ORDER BY `{sql_table_name}`.`{order}` ASC"

    l_table_sql = sqlConnection.set_command(sql_default_command)
    for table in l_table_sql:
        # Check doubles annu_cat
        if l_table.get(table[0], None) is not None:
            return logging.critical(f"{__name__} - {sql_table_name} with id={table[0]} already exist !")

        # Save Table
        l_table[table[0]] = table

    # Check after get data
    if len(l_table) == 0:
        logging.critical(f"{__name__} - No {sql_table_name} find from SQL Database !")
    if len(l_table) != len(l_table_sql):
        logging.critical(f"{__name__} - Impossible to get all {sql_table_name} from SQL Database ! \
            Get {len(l_table)} {sql_table_name} instead of {len(l_table_sql)}")

    logging.info(f"Get {len(l_table)} {sql_table_name} from SQL Database.")
    return l_table

def run():
    # -----------------------------------
    # Logger
    # -----------------------------------
    logging = create_logger('sqlImport', deletePreviousLog=True)
    logging.info("Start SQL importation...")


    # -----------------------------------
    # Read config file for SQL
    # -----------------------------------
    l_sqlConfig_filename = "config.ini"
    l_sqlConfig_folder = "/etc"
    l_sqlConfig_file = f"{l_sqlConfig_folder}/{l_sqlConfig_filename}"
    import configparser
    settings = configparser.ConfigParser()
    settings._interpolation = configparser.ExtendedInterpolation()
    if not settings.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), f"{l_sqlConfig_file}")):
        logging.critical(f"main - Impossible to open {l_sqlConfig_file} !")
    logging.info(f"File {l_sqlConfig_file} has been load !")


    # -----------------------------------
    # Connexion to SQL Database
    # -----------------------------------
    NetLiensSqlNetwork = SqlConnection(settings.get('sql_netLiens', 'address'),
                                    settings.get('sql_netLiens', 'user'),
                                    settings.get('sql_netLiens', 'password'),
                                    settings.get('sql_netLiens', 'databasename'))
    logging.info(f"SQL Database has been set !")


    # # -----------------------------------
    # # Start conversion
    # # -----------------------------------
    logging.info("*********************************")
    logging.info("Conversion starting...")

    logging.info("Get SQL Data...")
    # l_annuCat_map = readSqlTable(
    #     logging=logging,
    #     sqlConnection=NetLiensSqlNetwork,
    #     sql_table_name=CategoryManager.sqlTableName,
    #     order='cat_parent'
    # )
    # l_annuDept_map = readSqlTable(
    #     logging=logging,
    #     sqlConnection=NetLiensSqlNetwork,
    #     sql_table_name=LocalisationManager.sqlTableName
    # )
    l_annuSite_map = readSqlTable(
        logging=logging,
        sqlConnection=NetLiensSqlNetwork,
        sql_table_name=AnnouncementManager.sqlTableName
    )

    logging.info("Starting Management instances...")
    l_category = CategoryManager()
    l_localisation = LocalisationManager()
    l_announcement = AnnouncementManager()

    logging.info("Delete database...")
    l_category.deleteModel()
    l_localisation.deleteModel()
    l_announcement.deleteModel()
    User.objects.all().delete()

    logging.info("Creation of functionnal user...")
    l_functionnalUser = User.objects.create_superuser(
        email=settings.get('import_username', 'email'),
        password=settings.get('import_username', 'password')
    )

    logging.info("Category starting...")
    # l_category.createSqlObject(
    #     sqlObjectMap = l_annuCat_map,
    #     functionnalUser = l_functionnalUser
    # )
    # l_category.createModelsFromSqlObjectMap(
    #     functionnalUser = l_functionnalUser
    # )
    logging.info("Category conversion [OK]")

    logging.info("Localisation Conversion starting...")
    # l_localisation.createModelsFromInseeFile(
    #     sqlObjectMap = l_annuDept_map,
    #     functionnalUser = l_functionnalUser
    # )
    logging.info("Localisation conversion [OK]")

    logging.info("Announcement Conversion starting...")
    l_announcement.createSqlObject(
        sqlObjectMap=l_annuSite_map,
        functionnalUser=l_functionnalUser
    )
    l_announcement.createModelsFromSqlObjectMap(
        functionnalUser = l_functionnalUser
    )

    logging.info("Announcement conversion [OK]")

    logging.info("Conversion [OK]")
    logging.info("*********************************\n")
