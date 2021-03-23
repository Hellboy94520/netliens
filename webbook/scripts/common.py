from webbook.scripts.log import create_logger
from webbook.models import User
import logging

def deleteModel(model, modelData, logging: logging):
    logging.debug(f"Deleting all {model._meta.model.__name__}s from database...")
    model.objects.all().delete()
    if model.objects.all().count() != 0:
        logging.critical(f"{model._meta.model.__name__}s have not been deleted !")
        return False
    if modelData.objects.all().count() != 0:
        logging.critical(f"{modelData._meta.model.__name__}s have not been deleted !")
        return False
    logging.info(f"all {model._meta.model.__name__}s have been deleted from Django database")
    return True

class Manager():
    sqlTableName = None

    def __init__(self, className, model, modelData, modelSql):
        # Creation of the log
        self.logging = create_logger(className)
        self.logging.debug("init starting...")
        # Init value with input parameters
        self.__model = model
        self.__modelData = modelData
        self.__sqlModel = modelSql

        # Init variable
        self.__sqlObjectList = dict()

        self.logging.debug("init done")


    def deleteModel(self):
        self.logging.debug(f"Deleting all {self.__model._meta.model.__name__} from database...")
        self.__model.objects.all().delete()
        if self.__model.objects.all().count() != 0:
            self.logging.critical(f"{self.__model._meta.model.__name__} have not been deleted !")
            return False
        if self.__modelData.objects.all().count() != 0:
            self.logging.critical(f"{self.__modelData._meta.model.__name__} have not been deleted !")
            return False
        self.logging.info(f"all {self.__model._meta.model.__name__} have been deleted from Django database")
        return True


    def createSqlObject(self, sqlObjectMap: dict, functionnalUser: User):
        # Verifying input
        if len(sqlObjectMap) == 0:
            self.logging.critical(f"Map of {self.sqlTableName} is empty !")
            return False
        # Convert Map to Python object
        for key, value in sqlObjectMap.items():
            self.__sqlObjectList[key] = self.__sqlModel(value)
        # Verifying output
        if len(sqlObjectMap) != len(self.__sqlObjectList):
            self.logging.critical(f"Expected {len(sqlObjectMap)} {self.__sqlModel.__class__.__name__}, " \
            f"I have {len(self.__sqlObjectList)} {self.__sqlModel.__class__.__name__} !")


        self.logging.info(f"{len(self.__sqlObjectList)} {self.__sqlModel.__class__.__name__} has been created.")
        return True

class ManagerSqlObject():
    def __str__(self):
        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        print(members)
        return ""
