# Documentation: https://www.insee.fr/fr/information/2560452
# Code officiel géographique Insee
import csv
import re
from abc import ABC
import re
import pprint

from webbook.models import Localisation, LocalisationData, LanguageAvailable
from webbook.models import User
from webbook.forms import LocalisationForm, LocalisationDataForm
from webbook.scripts import log as Log


class LocalisationManager():
    sql_table_name = "annu_dept"

    def deleteLocalisation():
        Log.info("Deleting all Localisation from database...")
        Localisation.objects.all().delete()
        if Localisation.objects.all().count() != 0:
            Log.fatal(self.__class__.__name__, "Localisation has not been deleted !")
        if LocalisationData.objects.all().count() != 0:
            Log.fatal(self.__class__.__name__, "LocalisationData has not been deleted !")
        Log.info("Deleting all Localisation OK")
        return True

    def to_integer(className: str, valueName: str, value: str):
        try:
            result = int(value)
        except Exception as e:
            Log.warning(className, f"{valueName} value \'{value}\' is not a number ! Ignore it...")
            return None
        return result

    def to_lowerCase(className: str, valueName: str, value: str):
        regexp = re.compile("[\w\ \-\']+")
        string = regexp.match(value)
        if not string:
            Log.warning(className, f"{valueName} value \'{value}\' is None after regexp ! Ignore it...")
            return None
        lower_string = string[0].lower()
        string = lower_string.title()
        return string

    def __createSqlAssociationMap(self, sqlObjectList: list):
        self.sqlAssocationMap = dict()
        for i in range(1,95):
            # French Department
            if i==20:
                # Corse (Department) --> Corse (Region)
                self.sqlAssocationMap[i] = '2A004'
            else:
                self.sqlAssocationMap[i] = str(i).zfill(2)
        self.sqlAssocationMap[201] = "FRA"
        self.sqlAssocationMap[202] = "EUR"
        self.sqlAssocationMap[203] = "AMR"
        self.sqlAssocationMap[204] = "AMR"
        self.sqlAssocationMap[205] = "AFR"
        self.sqlAssocationMap[206] = "AFR"
        self.sqlAssocationMap[207] = "ASA"
        self.sqlAssocationMap[208] = "OCE"
        self.sqlAssocationMap[209] = ""
        self.sqlAssocationMap[210] = ""
        self.sqlAssocationMap[211] = "OCE"

        self.sqlAssocationMap[301] = "67482"
        self.sqlAssocationMap[302] = "33063"
        self.sqlAssocationMap[303] = "69123"
        self.sqlAssocationMap[304] = "76540"
        self.sqlAssocationMap[305] = "21231"
        self.sqlAssocationMap[306] = "35238"
        self.sqlAssocationMap[307] = "45234"
        self.sqlAssocationMap[308] = "67482"
        self.sqlAssocationMap[309] = "2A004"
        self.sqlAssocationMap[311] = "21231"
        self.sqlAssocationMap[312] = "76540"
        self.sqlAssocationMap[313] = "75056"
        self.sqlAssocationMap[314] = "31555"
        self.sqlAssocationMap[315] = "33063"
        self.sqlAssocationMap[316] = "67482"
        self.sqlAssocationMap[317] = "31555"
        self.sqlAssocationMap[318] = "59350"
        self.sqlAssocationMap[319] = "44109"
        self.sqlAssocationMap[320] = "59350"
        self.sqlAssocationMap[321] = "33063"
        self.sqlAssocationMap[322] = "13055"
        self.sqlAssocationMap[323] = "69123"
        self.sqlAssocationMap[325] = "" #TODO: Which region to use for DOM-TOM ?

        self.sqlAssocationMap[401] = "FRA"
        self.sqlAssocationMap[402] = "DEU"
        self.sqlAssocationMap[403] = "AUT"
        self.sqlAssocationMap[404] = "BEL"
        self.sqlAssocationMap[405] = "CYP"
        self.sqlAssocationMap[406] = "DNK"
        self.sqlAssocationMap[407] = "ESP"
        self.sqlAssocationMap[408] = "FIN"
        self.sqlAssocationMap[410] = "GRC"
        self.sqlAssocationMap[411] = "HUN"
        self.sqlAssocationMap[412] = "IRL"
        self.sqlAssocationMap[413] = "ISL"
        self.sqlAssocationMap[414] = "ITA"
        self.sqlAssocationMap[415] = "LUX"
        self.sqlAssocationMap[416] = "MKD"
        self.sqlAssocationMap[417] = "MLT"
        self.sqlAssocationMap[418] = "MCO"
        self.sqlAssocationMap[419] = "NOR"
        self.sqlAssocationMap[420] = "NLD"
        self.sqlAssocationMap[421] = "POL"
        self.sqlAssocationMap[422] = "PRT"
        self.sqlAssocationMap[423] = "ROU"
        self.sqlAssocationMap[424] = "GBR"
        self.sqlAssocationMap[425] = "SWE"
        self.sqlAssocationMap[426] = "CHE"
        self.sqlAssocationMap[427] = "UKR"
        self.sqlAssocationMap[463] = "YEM"
        self.sqlAssocationMap[464] = "VNM"
        self.sqlAssocationMap[465] = "TUR"
        self.sqlAssocationMap[466] = "" #TODO: Not found
        self.sqlAssocationMap[467] = "THA"
        self.sqlAssocationMap[468] = "" #TODO: Not found
        self.sqlAssocationMap[469] = "" #TODO: Not found
        self.sqlAssocationMap[470] = "LKA"
        self.sqlAssocationMap[471] = "SGP"
        self.sqlAssocationMap[472] = "PHL"
        self.sqlAssocationMap[473] = "PSE"
        self.sqlAssocationMap[474] = "PAK"
        self.sqlAssocationMap[475] = "NPL"
        self.sqlAssocationMap[476] = "MMR"
        self.sqlAssocationMap[477] = "MNG"
        self.sqlAssocationMap[478] = "MDV"
        self.sqlAssocationMap[479] = "MYS"
        self.sqlAssocationMap[480] = "LBN"
        self.sqlAssocationMap[481] = "LAO"
        self.sqlAssocationMap[482] = "KWT"
        self.sqlAssocationMap[483] = "JOR"
        self.sqlAssocationMap[484] = "JPN"
        self.sqlAssocationMap[485] = "ISR"
        self.sqlAssocationMap[486] = "IRN"
        self.sqlAssocationMap[487] = "IRQ"
        self.sqlAssocationMap[488] = "IDN"
        self.sqlAssocationMap[489] = "IND"
        self.sqlAssocationMap[490] = "" #TODO: Not found
        self.sqlAssocationMap[491] = "ARE"
        self.sqlAssocationMap[492] = "PRK" #INFO: Choose PRK (South Corea)
        self.sqlAssocationMap[493] = "CHN"
        self.sqlAssocationMap[494] = "KHM"
        self.sqlAssocationMap[495] = "BTN"
        self.sqlAssocationMap[496] = "BGD"
        self.sqlAssocationMap[497] = "ARM"
        self.sqlAssocationMap[498] = "SAU"
        self.sqlAssocationMap[499] = "AFG"

        self.sqlAssocationMap[500] = "USA"
        self.sqlAssocationMap[501] = "CAN"
        self.sqlAssocationMap[502] = "MEX"
        self.sqlAssocationMap[503] = "" #TODO: Where put this one ?
        self.sqlAssocationMap[504] = "ARG"
        self.sqlAssocationMap[505] = "CRI"
        self.sqlAssocationMap[506] = "BOL"
        self.sqlAssocationMap[507] = "BLZ"
        self.sqlAssocationMap[508] = "BRA"
        self.sqlAssocationMap[509] = "CHL"
        self.sqlAssocationMap[510] = "COL"
        self.sqlAssocationMap[511] = "ECU"
        self.sqlAssocationMap[512] = "GTM"
        self.sqlAssocationMap[513] = "GUY"
        self.sqlAssocationMap[514] = "HND"
        self.sqlAssocationMap[515] = "NIC"
        self.sqlAssocationMap[516] = "PAN"
        self.sqlAssocationMap[517] = "PRY"
        self.sqlAssocationMap[518] = "PER"
        self.sqlAssocationMap[519] = "" #TODO: Not found
        self.sqlAssocationMap[520] = "URY"
        self.sqlAssocationMap[521] = "VEN"
        self.sqlAssocationMap[522] = "" #TODO: Where put this one ?
        self.sqlAssocationMap[523] = "AFR"
        self.sqlAssocationMap[524] = "DZA"
        self.sqlAssocationMap[525] = "AGO"
        self.sqlAssocationMap[526] = "BEN"
        self.sqlAssocationMap[527] = "BFA"
        self.sqlAssocationMap[528] = "CMR"
        self.sqlAssocationMap[529] = "CPV"
        self.sqlAssocationMap[530] = "CAF"
        self.sqlAssocationMap[531] = "COM"
        self.sqlAssocationMap[532] = "COG"
        self.sqlAssocationMap[533] = "CIV"
        self.sqlAssocationMap[534] = "DJI"
        self.sqlAssocationMap[535] = "EGY"
        self.sqlAssocationMap[536] = "ETH"
        self.sqlAssocationMap[537] = "GAB"
        self.sqlAssocationMap[538] = "GMB"
        self.sqlAssocationMap[539] = "GHA"
        self.sqlAssocationMap[540] = "GNQ"
        self.sqlAssocationMap[541] = "KEN"
        self.sqlAssocationMap[542] = "LBR"
        self.sqlAssocationMap[543] = "LBY"
        self.sqlAssocationMap[544] = "MDG"
        self.sqlAssocationMap[545] = "MLI"
        self.sqlAssocationMap[546] = "MAR"
        self.sqlAssocationMap[547] = "MRT"
        self.sqlAssocationMap[548] = "MOZ"
        self.sqlAssocationMap[549] = "NAM"
        self.sqlAssocationMap[550] = "NER"
        self.sqlAssocationMap[551] = "NGA"
        self.sqlAssocationMap[552] = "UGA"
        self.sqlAssocationMap[553] = "RWA"
        self.sqlAssocationMap[554] = "" #TODO: Not found
        self.sqlAssocationMap[555] = "SEN"
        self.sqlAssocationMap[556] = "SYC"
        self.sqlAssocationMap[557] = "SLE"
        self.sqlAssocationMap[558] = "SOM"
        self.sqlAssocationMap[559] = "SDN"
        self.sqlAssocationMap[560] = "TZA"
        self.sqlAssocationMap[561] = "TCD"
        self.sqlAssocationMap[562] = "TGO"
        self.sqlAssocationMap[563] = "TUN"
        self.sqlAssocationMap[564] = "ZMB"
        self.sqlAssocationMap[565] = "ZWE"
        self.sqlAssocationMap[566] = "" #TODO: Where put this one?
        self.sqlAssocationMap[567] = "" #TODO: Where put this one?
        self.sqlAssocationMap[570] = "AUS"
        self.sqlAssocationMap[571] = "NZL"
        self.sqlAssocationMap[572] = "FJI"
        self.sqlAssocationMap[573] = "" #TODO: Where put this one?
        self.sqlAssocationMap[575] = "" #TODO: Where put this one?
        self.sqlAssocationMap[576] = "" #TODO: 'Ile Maurice' not found to not confuse with 'Maurice' !
        self.sqlAssocationMap[598] = "" #TODO: Where put this one?
        self.sqlAssocationMap[599] = "" #TODO: Where put this one?

        self.sqlAssocationMap[600] = "ALB"
        self.sqlAssocationMap[601] = "AND"
        self.sqlAssocationMap[603] = "BLR"
        self.sqlAssocationMap[604] = "BIH"
        self.sqlAssocationMap[605] = "BGR"
        self.sqlAssocationMap[606] = "HRV"
        self.sqlAssocationMap[607] = "EST"
        self.sqlAssocationMap[608] = "" #TODO: Not found
        self.sqlAssocationMap[609] = "" #TODO: Not found
        self.sqlAssocationMap[610] = "" #TODO: Not found
        self.sqlAssocationMap[611] = "" #TODO: Not found
        self.sqlAssocationMap[612] = "LIE"
        self.sqlAssocationMap[613] = "LTU"
        self.sqlAssocationMap[614] = "MDA"
        self.sqlAssocationMap[615] = "" #TODO: Not found
        self.sqlAssocationMap[616] = "RUS"
        self.sqlAssocationMap[617] = "SMR"
        self.sqlAssocationMap[618] = "SVK"
        self.sqlAssocationMap[619] = "SVN"
        self.sqlAssocationMap[620] = "" #TODO: Not found
        self.sqlAssocationMap[621] = "" #TODO: Not found

        self.sqlAssocationMap[9999] = "" #TODO: Not found

        for key, code in self.sqlAssocationMap.items():
            log = f"Old one, key={key}, Name:'{sqlObjectList.get(key)[1]}' --> "
            if code:
                log = log+f"code={code}, Name:'{Localisation.objects.get(code=code).get_data(LanguageAvailable.FR.value).name}'"
                Log.debug(self.__class__.__name__, '__createSqlAssociationMap', log)
            else:
                log = log + f"{None}"
                Log.error(self.__class__.__name__, log)


    def __init__(self, sqlObjectList: list, functionnalUser: User):
        Log.debug(self.__class__.__name__, 'init', 'starting...')

        if Localisation.objects.all().count() != 0:
            Log.fatal(self.__class__.__name__, "Impossible to delete all Localisation in database")

        # Create Localisation
        Log.info("Creation of Localisation from Insee files...")
        self.continentManager = self.ContinentManager(functionnalUser=functionnalUser)
        self.countryManager = self.CountryManager(
            functionnalUser = functionnalUser,
            parent_list = self.continentManager.mongo_list
        )
        self.regionManager = self.RegionManager(
            functionnalUser=functionnalUser,
            parent_list = self.countryManager.mongo_list
        )
        self.departmentManager = self.DepartmentManager(
            functionnalUser=functionnalUser,
            parent_list = self.regionManager.mongo_list
        )

        Log.info("Creation of association Map between old Database and new one...")
        self.__createSqlAssociationMap(sqlObjectList=sqlObjectList)
        Log.debug(self.__class__.__name__, 'init', 'done')


    """ ---------------------------------------------------- """
    """ Virtual Class                                        """
    """ ---------------------------------------------------- """
    class ObjectManager(ABC):
        """
            AbstractClass used for every type of object
        """

        def __init__(self, csvPath, cvsDelimiter, functionnalUser: User, **kwargs):
            Log.debug(self.__class__.__name__, "init", "starting...")
            self.mongo_list = []
            self.create_csv(csvPath=csvPath, cvsDelimiter=cvsDelimiter, functionnalUser=functionnalUser, **kwargs)
            Log.debug(self.__class__.__name__, "init", "done")

        def create_csv(self, csvPath, cvsDelimiter, functionnalUser: User, **kwargs):
            try:
                order = 1
                with open(csvPath, newline='', encoding='utf-8') as cvsFile:
                    spamreader = csv.reader(cvsFile, delimiter=cvsDelimiter, quotechar='|')
                    next(spamreader) # Avoid first line
                    for row in spamreader:
                        order += 1
                        self.CsvObject(fromCvsFile=row, mongo_list=self.mongo_list, functionnalUser=functionnalUser, order=order, **kwargs)
            except Exception as e:
                Log.fatal(self.__class__.__name__, f"Impossible to open file \'{csvPath}\': {e}")


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
        def __init__(self, functionnalUser: User):
            super().__init__(
                csvPath = '/django_project/app/webbook/scripts/InseeData/continent2020.csv',
                cvsDelimiter = ';',
                functionnalUser = functionnalUser
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            def __init__(self, fromCvsFile, mongo_list, functionnalUser: User, order: int):
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
                l_localisationForm = LocalisationForm(
                    data={
                        'code':self.codeiso3,
                        'insee': self.cog,
                        'is_enable': True,
                        'is_linkeable': True,
                        'parent': None,
                        'order': order
                    }
                )
                if l_localisationForm.is_valid() is False:
                    Log.fatal(self.__class__.__name__, f"Error on Localisation with code={self.codeiso3}: {l_localisationForm.errors}")
                l_localisation = l_localisationForm.save(user=functionnalUser)

                # Create LocalisationData (FR)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.libcog,
                        'resume': 'Continent',
                        'localisation': l_localisation,
                        'language': LanguageAvailable.FR.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    Log.fatal(self.__class__.__name__, f"Error on LocalisationData with name={self.libcog}: {l_localisationDataForm.errors}")
                l_localisationDataForm.save()

                # Create LocalisationData (EN)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.libcog_en,
                        'resume': 'Continent',
                        'localisation': l_localisation,
                        'language': LanguageAvailable.EN.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    Log.fatal(self.__class__.__name__, f"Error on LocalisationData with name={self.libcog_en}: {l_localisationDataForm.errors}")
                l_localisationDataForm.save()

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
        def __init__(self, functionnalUser: User, parent_list: list):
            # Check input variable
            if not parent_list:
                Log.error(self.__class__.__name__, "No parent list impossible to continue ! Ignore it...")
                return

            # Conversion
            super().__init__(
                csvPath = '/django_project/app/webbook/scripts/InseeData/pays2020_correction.csv',
                cvsDelimiter = ';',
                functionnalUser = functionnalUser,
                parent_list = parent_list
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            cog_minimum_value = 10000

            def __init__(self, fromCvsFile, mongo_list, functionnalUser: User, order: int, parent_list):
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
                l_localisationForm = LocalisationForm(
                    data={
                        'code':self.codeiso3,
                        'insee': self.cog,
                        'is_enable': True,
                        'is_linkeable': True,
                        'parent': l_parent,
                        'order': order
                    }
                )
                if l_localisationForm.is_valid() is False:
                    Log.fatal(self.__class__.__name__, f"Error on Localisation with code={self.libcog}: {l_localisationForm.errors}")
                l_localisation = l_localisationForm.save(user=functionnalUser)

                # Create LocalisationData (FR)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.libcog,
                        'resume': 'Pays',
                        'localisation': l_localisation,
                        'language': LanguageAvailable.FR.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    Log.fatal(self.__class__.__name__, f"Error on LocalisationData with name={self.libcog}: {l_localisationDataForm.errors}")
                l_localisationDataForm.save()

                # Create LocalisationData (EN)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.libcog,
                        'resume': 'Country',
                        'localisation': l_localisation,
                        'language': LanguageAvailable.EN.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    Log.fatal(self.__class__.__name__, f"Error on LocalisationData with name={self.libcog}: {l_localisationDataForm.errors}")
                l_localisationDataForm.save()

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
        def __init__(self, functionnalUser: User, parent_list: list):
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
                functionnalUser = functionnalUser,
                france = france
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            def __init__(self, fromCvsFile, mongo_list, functionnalUser: User, france, order: int):
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
                    code = self.cheflieu,
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
        def __init__(self, functionnalUser: User, parent_list: list):
            # Check input variable
            if not parent_list:
                print(f"ERROR: {self.__class__.__name__}: No parent list impossible to continue ! Ignore it...")
                return

            super().__init__(
                csvPath = '/django_project/app/webbook/scripts/InseeData/departement2020.csv',
                cvsDelimiter = ',',
                functionnalUser = functionnalUser,
                parent_list = parent_list
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            def __init__(self, fromCvsFile, mongo_list, functionnalUser: User, parent_list, order: int):
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

                # Register localisation
                mongo_list.append(l_localisation)

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
