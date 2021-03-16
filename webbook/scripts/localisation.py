# Documentation: https://www.insee.fr/fr/information/2560452
# Code officiel géographique Insee
import csv
import re
from abc import ABC

from webbook.models import Localisation, LocalisationData, LanguageAvailable
from webbook.scripts import log as Log


class LocalisationManager():
    sql_table_name = "annu_dept"

    def to_integer(className: str, valueName: str, value: str):
        try:
            result = int(value)
        except Exception as e:
            Log.warning(className, f"{valueName} value \'{value}\' is not a number ! Ignore it...")
            return None
        return result

    def to_lowerCase(className: str, valueName: str, value: str):
        regexp = re.compile('[\w ]+')
        string = regexp.match(value)
        if not string:
            Log.warning(className, f"{valueName} value \'{value}\' is None after regexp ! Ignore it...")
            return None
        string = string[0].lower()
        string = string.capitalize()
        return string


    def __init__(self):
        Log.debug(self.__class__.__name__, 'init', 'starting...')

        # Clean Database
        Log.info("Deleting all Localisation from database...")
        Localisation.objects.all().delete()
        if Localisation.objects.all().count() != 0:
            Log.fatal(self.__class__.__name__, "Impossible to delete all Localisation in database")

        # Create Localisation
        self.continentManager = self.ContinentManager()
        self.countryManager = self.CountryManager(parent_list = self.continentManager.mongo_list)
        self.regionManager = self.RegionManager(parent_list = self.countryManager.mongo_list)
        self.departmentManager = self.DepartmentManager(parent_list = self.regionManager.mongo_list)
        Log.debug(self.__class__.__name__, 'init', 'done')

    """ ---------------------------------------------------- """
    """ Virtual Class                                        """
    """ ---------------------------------------------------- """
    class ObjectManager(ABC):
        """
            AbstractClass used for every type of object
        """

        def __init__(self, csvPath, cvsDelimiter, **kwargs):
            Log.debug(self.__class__.__name__, "init", "starting...")
            self.mongo_list = []
            self.create_csv(csvPath, cvsDelimiter, **kwargs)
            Log.debug(self.__class__.__name__, "init", "done")

        def create_csv(self, csvPath, cvsDelimiter, **kwargs):
            try:
                with open(csvPath, newline='', encoding='utf-8') as cvsFile:
                    spamreader = csv.reader(cvsFile, delimiter=cvsDelimiter, quotechar='|')
                    next(spamreader) # Avoid first line
                    for row in spamreader:
                        self.CsvObject(fromCvsFile=row, mongo_list=self.mongo_list, **kwargs)
            except Exception as e:
                Log.error(self.__class__.__name__, f"Impossible to open file \'{csvPath}\': {e}")


    """ ---------------------------------------------------- """
    """ ---------------------------------------------------- """
    class ContinentManager(ObjectManager):
        """
            Continent:
            - 99100: Europe/Europe
            - 99200: Asia/Asie
            - 99300: Africa/Afrique
            - 99400: America/Amérique
            - 99500: Oceania/Océanie
        """
        def __init__(self):
            super().__init__(
                csvPath = '/django_project/app/webbook/scripts/InseeData/continent2020.csv',
                cvsDelimiter = ';'
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            def __init__(self, fromCvsFile, mongo_list):
                self.__class__.__name__ = "ContinentData"
                self.cog = LocalisationManager.to_integer(self.__class__.__name__, 'cog', fromCvsFile[0])
                self.libcog = LocalisationManager.to_lowerCase(self.__class__.__name__, 'libcog', fromCvsFile[1])
                self.libcog_en = LocalisationManager.to_lowerCase(self.__class__.__name__, 'libcog_en',fromCvsFile[2])
                self.codeiso2 = fromCvsFile[3]
                self.codeiso3 = fromCvsFile[4]

                # Check Variable
                if not self.cog:
                    return
                if not self.libcog:
                    return
                if not self.libcog_en:
                    return

                # Create Localisation
                l_localisation = Localisation.objects.create(
                    code = self.codeiso3,
                    insee = self.cog,
                    is_enable = True,
                    is_linkeable = True,
                    parent = None,
                    order = 0
                )
                LocalisationData.objects.create(
                    #TODO: libcog to small character
                    name = self.libcog,
                    resume = "",
                    localisation = l_localisation,
                    language = LanguageAvailable.FR.value
                )
                LocalisationData.objects.create(
                    #TODO: libcog to small character
                    name = self.libcog_en,
                    resume = "",
                    localisation = l_localisation,
                    language = LanguageAvailable.EN.value
                )
                # Register localisation
                mongo_list.append(l_localisation)

            def __repr__(self):
                return f"{self.__class__.__name__}: {self.cog} - {self.libcog}"

            def __str__(self):
                return f"""{self.__class__.__name__}: \
cog = {self.cog}, libcog = {self.libcog}, libcog_en = {self.libcog_en}, codeiso2 = {self.codeiso2}, codeiso3 = {self.codeiso3}"""


    """ ---------------------------------------------------- """
    """ ---------------------------------------------------- """
    class CountryManager(ObjectManager):
        """
            Country
        """
        def __init__(self, parent_list: list):
            # Check input variable
            if not parent_list:
                Log.error(self.__class__.__name__, "No parent list impossible to continue ! Ignore it...")
                return

            # Conversion
            super().__init__(
                csvPath = '/django_project/app/webbook/scripts/InseeData/pays2020_correction.csv',
                cvsDelimiter = ';',
                parent_list = parent_list
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            cog_minimum_value = 10000

            def __init__(self, fromCvsFile, mongo_list, parent_list):
                self.__class__.__name__ = "CountryData"
                self.cog = LocalisationManager.to_integer(self.__class__.__name__, 'cog', fromCvsFile[0])
                self.actual = LocalisationManager.to_integer(self.__class__.__name__, 'actual', fromCvsFile[1])
                self.capay = fromCvsFile[2]
                self.crpay = fromCvsFile[3]
                self.ani = fromCvsFile[4]
                self.libcog = LocalisationManager.to_lowerCase(self.__class__.__name__, 'libcog', fromCvsFile[5])
                self.libenr = fromCvsFile[6]
                self.ancnom = fromCvsFile[7]
                self.codeiso2 = fromCvsFile[8]
                self.codeiso3 = fromCvsFile[9]
                self.codenum3 = fromCvsFile[10]

                # To Ignore:
                if self.actual != 1:
                    return

                # Check value
                if not self.cog:
                    if self.libcog != "France":
                        return
                    self.cog=99100
                    Log.info(f"EXCEPTION - It is France ! So continue with a cog value of {self.cog}...")
                if self.cog < self.cog_minimum_value:
                    Log.warning(self.__class__.__name__, f"cog value \'{self.cog}\' is less than {self.cog_minimum_value} ! Ignore it...")
                    return
                if not self.libcog:
                    return

                # - parent
                l_parent = None
                l_parent_insee = int(str(self.cog)[:3])*100
                for parent in parent_list:
                    if parent.insee == l_parent_insee:
                        l_parent = parent
                if not l_parent:
                    Log.warning(self.__class__.__name__, f"parent not find with insee value \'{l_parent_insee}\' ! Ignore it...")
                    return

                # Create Localisation
                l_localisation = Localisation.objects.create(
                    code = self.codeiso3,
                    insee = self.cog,
                    is_enable = True,
                    is_linkeable = True,
                    parent = l_parent,
                    order = 0
                )
                LocalisationData.objects.create(
                    name = self.libcog,
                    resume = "",
                    localisation = l_localisation,
                    language = LanguageAvailable.FR.value
                )
                LocalisationData.objects.create(
                    name = self.libcog,
                    resume = "",
                    localisation = l_localisation,
                    language = LanguageAvailable.EN.value
                )

                # Register localisation
                mongo_list.append(l_localisation)


            def __repr__(self):
                return f"{self.__class__.__name__}: {self.cog} - {self.libcog}"

            def __str__(self):
                return f"""{self.__class__.__name__}: \
cog = {self.cog}, actual = {self.actual}, capay = {self.capay}, crpay = {self.crpay}, ani = {self.ani}, libcog = {self.libcog}, libenr = {self.libenr}, ancnom = {self.ancnom}, codeiso2 = {self.codeiso2}, codeiso3 = {self.codeiso3} codenum3 = {self.codenum3}"""


    """ ---------------------------------------------------- """
    """ ---------------------------------------------------- """
    class RegionManager(ObjectManager):
        """
            Region
        """
        def __init__(self, parent_list: list):
            # Check input variable
            if not parent_list:
                print(f"ERROR: {self.__class__.__name__}: No parent list impossible to continue ! Ignore it...")
                return

            france = None
            for parent in parent_list:
                if parent.get_data(LanguageAvailable.FR.value).name == "France":
                    france = parent
            if not france:
                print(f"ERROR: {self.__class__.__name__}: France is none impossible to continue ! Ignore it...")
                return

            super().__init__(
                csvPath = '/django_project/app/webbook/scripts/InseeData/region2020.csv',
                cvsDelimiter = ',',
                france = france
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            def __init__(self, fromCvsFile, mongo_list, france):
                self.__class__.__name__ = "RegionData"
                self.reg = LocalisationManager.to_integer(self.__class__.__name__, 'reg', fromCvsFile[0])
                self.cheflieu = fromCvsFile[1]
                self.tncc = LocalisationManager.to_lowerCase(self.__class__.__name__, 'tncc', fromCvsFile[2])
                self.ncc = LocalisationManager.to_lowerCase(self.__class__.__name__, 'ncc', fromCvsFile[3])
                self.nccenr = LocalisationManager.to_lowerCase(self.__class__.__name__, 'nccenr', fromCvsFile[4])
                self.libelle = fromCvsFile[5]

                # Check Variables
                # - Reg
                if not self.reg:
                    return

                # Create Localisation
                l_localisation = Localisation.objects.create(
                    code = self.reg,
                    insee = self.reg,
                    is_enable = True,
                    is_linkeable = True,
                    parent = france,
                    order = 0
                )
                LocalisationData.objects.create(
                    name = self.nccenr,
                    resume = "",
                    localisation = l_localisation,
                    language = LanguageAvailable.FR.value
                )
                LocalisationData.objects.create(
                    name = self.nccenr,
                    resume = "",
                    localisation = l_localisation,
                    language = LanguageAvailable.EN.value
                )

                # Register localisation
                mongo_list.append(l_localisation)


            def __repr__(self):
                return f"{self.__class__.__name__}: {self.reg} - {self.nccenr}"

            def __str__(self):
                return f"""{self.__class__.__name__}: \
reg = {self.reg}, cheflieu = {self.cheflieu}, tncc = {self.tncc}, ncc = {self.ncc}, nccenr = {self.nccenr}, libelle = {self.libelle}"""


    """ ---------------------------------------------------- """
    """ ---------------------------------------------------- """
    class DepartmentManager(ObjectManager):
        """
            Department
        """
        def __init__(self, parent_list: list):
            # Check input variable
            if not parent_list:
                print(f"ERROR: {self.__class__.__name__}: No parent list impossible to continue ! Ignore it...")
                return

            super().__init__(
                csvPath = '/django_project/app/webbook/scripts/InseeData/departement2020.csv',
                cvsDelimiter = ',',
                parent_list = parent_list
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            def __init__(self, fromCvsFile, mongo_list, parent_list):
                self.__class__.__name__ = "Department"
                self.dep = fromCvsFile[0]
                self.reg = LocalisationManager.to_integer(self.__class__.__name__, 'reg', fromCvsFile[1])
                self.cheflieu = str(fromCvsFile[2])
                self.tncc = fromCvsFile[3]
                self.ncc = fromCvsFile[4]
                self.nccenr = fromCvsFile[5]
                self.libelle = fromCvsFile[6]

                # Check variable
                # - dep
                if not self.dep:
                    return
                # - reg
                if not self.reg:
                    return
                # - nccenr
                if not self.nccenr:
                    return
                # - parent
                l_parent = None
                for parent in parent_list:
                    if parent.insee == self.reg:
                        l_parent = parent
                if not parent:
                    print(f"ERROR: {self.__class__.__name__} - parent not find with insee value \'{self.reg}\' ! Ignore it...")
                    return

                # Create Localisation
                l_localisation = Localisation.objects.create(
                    code = self.dep,
                    insee = int(re.compile("(\d+)").match(self.dep).group(1)), # required for 2A and 2B
                    is_enable = True,
                    is_linkeable = True,
                    parent = l_parent,
                    order = 0
                )
                LocalisationData.objects.create(
                    name = self.nccenr,
                    resume = "",
                    localisation = l_localisation,
                    language = LanguageAvailable.FR.value
                )
                LocalisationData.objects.create(
                    name = self.nccenr,
                    resume = "",
                    localisation = l_localisation,
                    language = LanguageAvailable.EN.value
                )

            def __repr__(self):
                return f"{self.__class__.__name__}: {self.dep} - {self.nccenr}"

            def __str__(self):
                return f"""{self.__class__.__name__}: \
dep = {self.dep}, reg = {self.reg}, cheflieu = {self.cheflieu}, tncc = {self.tncc}, ncc = {self.ncc}, nccenr = {self.nccenr}, libelle = {self.libelle}"""


    """ ---------------------------------------------------- """
    """ ---------------------------------------------------- """
    class LocalisationSql():
        def __init__(self, sqlObject):
            self.id_dept = sqlObject[0]
            self.nom_dept = sqlObject[1]
            self.id_region = sqlObject[2]
            self.id_zone = sqlObject[3]

        def __repr__(self):
            return f"{self.__class__.__name__}: {self.id_dept} - {self.nom_dept}"

        def __str__(self):
            return f"""{self.__class__.__name__}: \
id_dept = {self.id_dept}, nom_dept = {self.nom_dept}, id_region = {self.id_region}, id_zone = {self.id_zone}"""
