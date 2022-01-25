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
from webbook.scripts.common import Manager, ManagerSqlObject
from webbook.scripts.log import create_logger


def to_integer(value: str):
    try:
        result = int(value)
    except ValueError:
        return None
    else:
        return result

def to_lowerCase(value: str):
    regexp = re.compile("[\w\ \-\']+")
    string = regexp.match(value)
    if not string:
        return None
    lower_string = string[0].lower()
    string = lower_string.title()
    return string


class LocalisationManager(Manager):
    sqlTableName = "annu_dept"

    def __init__(self):
        super(LocalisationManager, self).__init__(
            className = self.__class__.__name__,
            model = Localisation,
            modelData = LocalisationData,
            modelSql = self.LocalisationSql
        )
        self.sqlAssociationMap = dict()

    def createModelsFromInseeFile(self, sqlObjectMap: dict(), functionnalUser: User):
        # Create Localisation
        self.logging.info("Creation of Localisation from Insee files...")
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

        self.logging.debug("Creation of association Map between old Database and new one...")
        self.__createSqlAssociationMap(
            sqlObjectMap = sqlObjectMap,
            functionnalUser = functionnalUser
        )
        self.logging.debug('Creation of Localisation from Insee files done')


    def __createSqlAssociationMap(self, sqlObjectMap: dict, functionnalUser: User):
        super(LocalisationManager, self).createSqlObject(
            sqlObjectMap = sqlObjectMap,
            functionnalUser = functionnalUser
        )

        for i in range(1,95):
            # French Department
            if i==20:
                # Corse (Department) --> Corse (Region)
                self.sqlAssociationMap[i] = '2A004'
            else:
                self.sqlAssociationMap[i] = str(i).zfill(2)
        self.sqlAssociationMap[201] = "FRA"
        self.sqlAssociationMap[202] = "EUR"
        self.sqlAssociationMap[203] = "AMR"
        self.sqlAssociationMap[204] = "AMR"
        self.sqlAssociationMap[205] = "AFR"
        self.sqlAssociationMap[206] = "AFR"
        self.sqlAssociationMap[207] = "ASA"
        self.sqlAssociationMap[208] = "OCE"
        self.sqlAssociationMap[209] = "" #TODO
        self.sqlAssociationMap[210] = "" #TODO
        self.sqlAssociationMap[211] = "OCE"

        self.sqlAssociationMap[301] = "67482"
        self.sqlAssociationMap[302] = "33063"
        self.sqlAssociationMap[303] = "69123"
        self.sqlAssociationMap[304] = "76540"
        self.sqlAssociationMap[305] = "21231"
        self.sqlAssociationMap[306] = "35238"
        self.sqlAssociationMap[307] = "45234"
        self.sqlAssociationMap[308] = "67482"
        self.sqlAssociationMap[309] = "2A004"
        self.sqlAssociationMap[311] = "21231"
        self.sqlAssociationMap[312] = "76540"
        self.sqlAssociationMap[313] = "75056"
        self.sqlAssociationMap[314] = "31555"
        self.sqlAssociationMap[315] = "33063"
        self.sqlAssociationMap[316] = "67482"
        self.sqlAssociationMap[317] = "31555"
        self.sqlAssociationMap[318] = "59350"
        self.sqlAssociationMap[319] = "44109"
        self.sqlAssociationMap[320] = "59350"
        self.sqlAssociationMap[321] = "33063"
        self.sqlAssociationMap[322] = "13055"
        self.sqlAssociationMap[323] = "69123"
        self.sqlAssociationMap[325] = "" #TODO: Which region to use for DOM-TOM ?

        self.sqlAssociationMap[401] = "FRA"
        self.sqlAssociationMap[402] = "DEU"
        self.sqlAssociationMap[403] = "AUT"
        self.sqlAssociationMap[404] = "BEL"
        self.sqlAssociationMap[405] = "CYP"
        self.sqlAssociationMap[406] = "DNK"
        self.sqlAssociationMap[407] = "ESP"
        self.sqlAssociationMap[408] = "FIN"
        self.sqlAssociationMap[410] = "GRC"
        self.sqlAssociationMap[411] = "HUN"
        self.sqlAssociationMap[412] = "IRL"
        self.sqlAssociationMap[413] = "ISL"
        self.sqlAssociationMap[414] = "ITA"
        self.sqlAssociationMap[415] = "LUX"
        self.sqlAssociationMap[416] = "MKD"
        self.sqlAssociationMap[417] = "MLT"
        self.sqlAssociationMap[418] = "MCO"
        self.sqlAssociationMap[419] = "NOR"
        self.sqlAssociationMap[420] = "NLD"
        self.sqlAssociationMap[421] = "POL"
        self.sqlAssociationMap[422] = "PRT"
        self.sqlAssociationMap[423] = "ROU"
        self.sqlAssociationMap[424] = "GBR"
        self.sqlAssociationMap[425] = "SWE"
        self.sqlAssociationMap[426] = "CHE"
        self.sqlAssociationMap[427] = "UKR"
        self.sqlAssociationMap[463] = "YEM"
        self.sqlAssociationMap[464] = "VNM"
        self.sqlAssociationMap[465] = "TUR"
        self.sqlAssociationMap[466] = "" #TODO: Not found
        self.sqlAssociationMap[467] = "THA"
        self.sqlAssociationMap[468] = "" #TODO: Not found
        self.sqlAssociationMap[469] = "" #TODO: Not found
        self.sqlAssociationMap[470] = "LKA"
        self.sqlAssociationMap[471] = "SGP"
        self.sqlAssociationMap[472] = "PHL"
        self.sqlAssociationMap[473] = "PSE"
        self.sqlAssociationMap[474] = "PAK"
        self.sqlAssociationMap[475] = "NPL"
        self.sqlAssociationMap[476] = "MMR"
        self.sqlAssociationMap[477] = "MNG"
        self.sqlAssociationMap[478] = "MDV"
        self.sqlAssociationMap[479] = "MYS"
        self.sqlAssociationMap[480] = "LBN"
        self.sqlAssociationMap[481] = "LAO"
        self.sqlAssociationMap[482] = "KWT"
        self.sqlAssociationMap[483] = "JOR"
        self.sqlAssociationMap[484] = "JPN"
        self.sqlAssociationMap[485] = "ISR"
        self.sqlAssociationMap[486] = "IRN"
        self.sqlAssociationMap[487] = "IRQ"
        self.sqlAssociationMap[488] = "IDN"
        self.sqlAssociationMap[489] = "IND"
        self.sqlAssociationMap[490] = "" #TODO: Not found
        self.sqlAssociationMap[491] = "ARE"
        self.sqlAssociationMap[492] = "PRK" #INFO: Choose PRK (South Corea)
        self.sqlAssociationMap[493] = "CHN"
        self.sqlAssociationMap[494] = "KHM"
        self.sqlAssociationMap[495] = "BTN"
        self.sqlAssociationMap[496] = "BGD"
        self.sqlAssociationMap[497] = "ARM"
        self.sqlAssociationMap[498] = "SAU"
        self.sqlAssociationMap[499] = "AFG"

        self.sqlAssociationMap[500] = "USA"
        self.sqlAssociationMap[501] = "CAN"
        self.sqlAssociationMap[502] = "MEX"
        self.sqlAssociationMap[503] = "" #TODO: Where put this one ?
        self.sqlAssociationMap[504] = "ARG"
        self.sqlAssociationMap[505] = "CRI"
        self.sqlAssociationMap[506] = "BOL"
        self.sqlAssociationMap[507] = "BLZ"
        self.sqlAssociationMap[508] = "BRA"
        self.sqlAssociationMap[509] = "CHL"
        self.sqlAssociationMap[510] = "COL"
        self.sqlAssociationMap[511] = "ECU"
        self.sqlAssociationMap[512] = "GTM"
        self.sqlAssociationMap[513] = "GUY"
        self.sqlAssociationMap[514] = "HND"
        self.sqlAssociationMap[515] = "NIC"
        self.sqlAssociationMap[516] = "PAN"
        self.sqlAssociationMap[517] = "PRY"
        self.sqlAssociationMap[518] = "PER"
        self.sqlAssociationMap[519] = "" #TODO: Not found
        self.sqlAssociationMap[520] = "URY"
        self.sqlAssociationMap[521] = "VEN"
        self.sqlAssociationMap[522] = "" #TODO: Where put this one ?
        self.sqlAssociationMap[523] = "AFR"
        self.sqlAssociationMap[524] = "DZA"
        self.sqlAssociationMap[525] = "AGO"
        self.sqlAssociationMap[526] = "BEN"
        self.sqlAssociationMap[527] = "BFA"
        self.sqlAssociationMap[528] = "CMR"
        self.sqlAssociationMap[529] = "CPV"
        self.sqlAssociationMap[530] = "CAF"
        self.sqlAssociationMap[531] = "COM"
        self.sqlAssociationMap[532] = "COG"
        self.sqlAssociationMap[533] = "CIV"
        self.sqlAssociationMap[534] = "DJI"
        self.sqlAssociationMap[535] = "EGY"
        self.sqlAssociationMap[536] = "ETH"
        self.sqlAssociationMap[537] = "GAB"
        self.sqlAssociationMap[538] = "GMB"
        self.sqlAssociationMap[539] = "GHA"
        self.sqlAssociationMap[540] = "GNQ"
        self.sqlAssociationMap[541] = "KEN"
        self.sqlAssociationMap[542] = "LBR"
        self.sqlAssociationMap[543] = "LBY"
        self.sqlAssociationMap[544] = "MDG"
        self.sqlAssociationMap[545] = "MLI"
        self.sqlAssociationMap[546] = "MAR"
        self.sqlAssociationMap[547] = "MRT"
        self.sqlAssociationMap[548] = "MOZ"
        self.sqlAssociationMap[549] = "NAM"
        self.sqlAssociationMap[550] = "NER"
        self.sqlAssociationMap[551] = "NGA"
        self.sqlAssociationMap[552] = "UGA"
        self.sqlAssociationMap[553] = "RWA"
        self.sqlAssociationMap[554] = "" #TODO: Not found
        self.sqlAssociationMap[555] = "SEN"
        self.sqlAssociationMap[556] = "SYC"
        self.sqlAssociationMap[557] = "SLE"
        self.sqlAssociationMap[558] = "SOM"
        self.sqlAssociationMap[559] = "SDN"
        self.sqlAssociationMap[560] = "TZA"
        self.sqlAssociationMap[561] = "TCD"
        self.sqlAssociationMap[562] = "TGO"
        self.sqlAssociationMap[563] = "TUN"
        self.sqlAssociationMap[564] = "ZMB"
        self.sqlAssociationMap[565] = "ZWE"
        self.sqlAssociationMap[566] = "" #TODO: Where put this one?
        self.sqlAssociationMap[567] = "" #TODO: Where put this one?
        self.sqlAssociationMap[570] = "AUS"
        self.sqlAssociationMap[571] = "NZL"
        self.sqlAssociationMap[572] = "FJI"
        self.sqlAssociationMap[573] = "" #TODO: Where put this one?
        self.sqlAssociationMap[575] = "" #TODO: Where put this one?
        self.sqlAssociationMap[576] = "" #TODO: 'Ile Maurice' not found to not confuse with 'Maurice' !
        self.sqlAssociationMap[598] = "" #TODO: Where put this one?
        self.sqlAssociationMap[599] = "" #TODO: Where put this one?

        self.sqlAssociationMap[600] = "ALB"
        self.sqlAssociationMap[601] = "AND"
        self.sqlAssociationMap[603] = "BLR"
        self.sqlAssociationMap[604] = "BIH"
        self.sqlAssociationMap[605] = "BGR"
        self.sqlAssociationMap[606] = "HRV"
        self.sqlAssociationMap[607] = "EST"
        self.sqlAssociationMap[608] = "" #TODO: Not found
        self.sqlAssociationMap[609] = "" #TODO: Not found
        self.sqlAssociationMap[610] = "" #TODO: Not found
        self.sqlAssociationMap[611] = "" #TODO: Not found
        self.sqlAssociationMap[612] = "LIE"
        self.sqlAssociationMap[613] = "LTU"
        self.sqlAssociationMap[614] = "MDA"
        self.sqlAssociationMap[615] = "" #TODO: Not found
        self.sqlAssociationMap[616] = "RUS"
        self.sqlAssociationMap[617] = "SMR"
        self.sqlAssociationMap[618] = "SVK"
        self.sqlAssociationMap[619] = "SVN"
        self.sqlAssociationMap[620] = "" #TODO: Not found
        self.sqlAssociationMap[621] = "" #TODO: Not found

        self.sqlAssociationMap[9999] = "" #TODO: Not found

        for key, code in self.sqlAssociationMap.items():
            log = f"Old one, key={key}, Name:'{self.sqlObjectMap.get(key).nom_dept}' --> "
            if code:
                try:
                    localisation = Localisation.objects.get(code=code)
                except:
                    self.logging.critical(f"No Localisation find for SqlKey='{key}'")
                log += f"code={code}, Name:'{localisation.get_data(LanguageAvailable.FR.value).name}'"
                self.logging.debug(log)
            else:
                log += "None"
                self.logging.error(log)


    class LocalisationSql(ManagerSqlObject):
        def __init__(self, sqlObject):
            self.id_dept = sqlObject[0]
            self.nom_dept = sqlObject[1]
            self.id_region = sqlObject[2]
            self.id_zone = sqlObject[3]


    """ ---------------------------------------------------- """
    """ Virtual Class                                        """
    """ ---------------------------------------------------- """
    class ObjectManager(ABC):
        """
            AbstractClass used for every type of object
        """

        def __init__(self, className: str, csvPath, cvsDelimiter, functionnalUser: User, **kwargs):
            self.logging = create_logger(className)
            self.logging.debug("init...")
            self.mongo_list = []
            self.create_csv(
                csvPath=csvPath,
                cvsDelimiter=cvsDelimiter,
                functionnalUser=functionnalUser,
                **kwargs
            )
            self.logging.debug("done.")

        def create_csv(self, csvPath, cvsDelimiter, functionnalUser: User, **kwargs):
            try:
                cvsFile = open(csvPath, newline='', encoding='utf-8')
            except IOError as e:
                self.logging.critical(f"Impossible to open file \'{csvPath}\': {e}")
            else:
                order = 1
                spamreader = csv.reader(cvsFile, delimiter=cvsDelimiter, quotechar='|')
                next(spamreader) # Avoid first line
                for row in spamreader:
                    order += 1
                    self.CsvObject(
                        fromCvsFile=row,
                        mongo_list=self.mongo_list,
                        functionnalUser=functionnalUser,
                        order=order,
                        **kwargs
                    )



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
                className = self.__class__.__name__,
                csvPath = '/django_project/app/webbook/scripts/InseeData/continent2020.csv',
                cvsDelimiter = ';',
                functionnalUser = functionnalUser
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            def __init__(self, fromCvsFile, mongo_list, functionnalUser: User, order: int):
                self.logging = create_logger("ContinentData")
                self.cog = to_integer(fromCvsFile[0])
                self.libcog = to_lowerCase(fromCvsFile[1])
                self.libcog_en = to_lowerCase(fromCvsFile[2])
                self.codeiso2 = fromCvsFile[3]
                self.codeiso3 = fromCvsFile[4]

                # Check Variable
                if not self.cog:
                    self.logging.error(f"Value '{self.cog}' is not a number ! Ignore it...")
                    return
                if not self.libcog:
                    self.logging.error(f"Value '{self.libcog}' is empty after regexp ! Ignore it...")
                    return
                if not self.libcog_en:
                    self.logging.error(f"Value '{self.libcog_en}' is empty after regexp ! Ignore it...")
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
                    self.logging.critical(f"Error on Localisation with code={self.codeiso3}: {l_localisationForm.errors}")
                l_localisation = l_localisationForm.save(user=functionnalUser)

                # Create LocalisationData (FR)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.libcog,
                        'resume': 'Continent',
                        'language': LanguageAvailable.FR.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    self.logging.critical(f"Error on LocalisationData with name={self.libcog}: {l_localisationDataForm.errors}")
                l_localisationDataForm.save()

                # Create LocalisationData (EN)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.libcog_en,
                        'resume': 'Continent',
                        'language': LanguageAvailable.EN.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    self.logging.critical(f"Error on LocalisationData with name={self.libcog_en}: {l_localisationDataForm.errors}")
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
            super().__init__(
                className = self.__class__.__name__,
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
                # Check input variable
                if not parent_list:
                    self.logging.critical("No parent list impossible to continue !")

                self.logging = create_logger("CountryData")
                self.cog = to_integer(fromCvsFile[0])
                self.actual = to_integer(fromCvsFile[1])
                self.capay = fromCvsFile[2]
                self.crpay = fromCvsFile[3]
                self.ani = fromCvsFile[4]
                self.libcog = to_lowerCase(fromCvsFile[5])
                self.libenr = fromCvsFile[6]
                self.ancnom = fromCvsFile[7]
                self.codeiso2 = fromCvsFile[8]
                self.codeiso3 = fromCvsFile[9]
                self.codenum3 = fromCvsFile[10]

                # To Ignore:
                if self.actual != 1:
                    return

                # Check value
                if self.cog is None:
                    if self.libcog != "France":
                        self.logging.error(f"Value '{self.cog}' is not a number ! Ignore it...")
                        return
                    self.cog=99100
                if self.cog < self.cog_minimum_value:
                    self.logging.warning(f"cog value \'{self.cog}\' is less than {self.cog_minimum_value} ! Ignore it...")
                    return
                if not self.libcog:
                    self.logging.error(f"Value '{self.libcog}' is empty after regexp ! Ignore it...")
                    return

                # - parent
                l_parent = None
                l_parent_insee = int(str(self.cog)[:3])*100
                for parent in parent_list:
                    if parent.insee == l_parent_insee:
                        l_parent = parent
                if not l_parent:
                    self.logging.warning(f"Parent not find with insee value \'{l_parent_insee}\' ! Ignore it...")
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
                    self.logging.critical(f"Error on Localisation with code={self.libcog}: {l_localisationForm.errors}")
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
                    self.logging.critical(f"Error on LocalisationData with name={self.libcog}: {l_localisationDataForm.errors}")
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
                    self.logging.critical(f"Error on LocalisationData with name={self.libcog}: {l_localisationDataForm.errors}")
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
            # Find parent
            france = None
            for parent in parent_list:
                if parent.get_data(LanguageAvailable.FR.value).name == "France":
                    france = parent

            super().__init__(
                className = self.__class__.__name__,
                csvPath = '/django_project/app/webbook/scripts/InseeData/region2020.csv',
                cvsDelimiter = ',',
                functionnalUser = functionnalUser,
                france = france
            )

        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            def __init__(self, fromCvsFile, mongo_list, functionnalUser: User, france, order: int):
                if not france:
                    self.critical(f"France contains nothing impossible to continue !")

                self.logging = create_logger("RegionData")
                self.reg = to_integer(fromCvsFile[0])
                self.cheflieu = fromCvsFile[1]
                self.tncc = to_lowerCase(fromCvsFile[2])
                self.ncc = to_lowerCase(fromCvsFile[3])
                self.nccenr = to_lowerCase(fromCvsFile[4])
                self.libelle = fromCvsFile[5]

                # Check Variables
                # - Reg
                if not self.reg:
                    self.logging.error(f"Value '{self.cog}' is not a number ! Ignore it...")
                    return

                # Create Localisation
                l_localisationForm = LocalisationForm(
                    data = {
                        'code': self.cheflieu,
                        'insee': self.reg,
                        'is_enable': True,
                        'is_linkeable': True,
                        'parent': france,
                        'order': order
                    }
                )
                if l_localisationForm.is_valid() is False:
                    self.logging.critical(f"Error on Localisation with code={self.cheflieu}: {l_localisationForm.errors}")
                l_localisation = l_localisationForm.save(user=functionnalUser)

                # Create LocalisationData (FR)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.nccenr,
                        'resume': 'Région Française',
                        'localisation': l_localisation,
                        'language': LanguageAvailable.FR.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    self.logging.critical(f"Error on LocalisationData with name={self.cheflieu}: {l_localisationDataForm.errors}")
                l_localisationDataForm.save()

                # Create LocalisationData (EN)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.nccenr,
                        'resume': 'French Region',
                        'localisation': l_localisation,
                        'language': LanguageAvailable.EN.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    self.logging.critical(f"Error on LocalisationData with name={self.cheflieu}: {l_localisationDataForm.errors}")
                l_localisationDataForm.save()

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
            super().__init__(
                className = self.__class__.__name__,
                csvPath = '/django_project/app/webbook/scripts/InseeData/departement2020.csv',
                cvsDelimiter = ',',
                functionnalUser = functionnalUser,
                parent_list = parent_list
            )



        """ ---------------------------------------------------- """
        """ ---------------------------------------------------- """
        class CsvObject():
            def __init__(self, fromCvsFile, mongo_list, functionnalUser: User, parent_list, order: int):
                # Check input variable
                if not parent_list:
                    self.logging.critical("No parent list impossible to continue !")

                self.logging = create_logger("DepartmentData")
                self.dep = fromCvsFile[0]
                self.reg = to_integer(fromCvsFile[1])
                self.cheflieu = str(fromCvsFile[2])
                self.tncc = fromCvsFile[3]
                self.ncc = fromCvsFile[4]
                self.nccenr = fromCvsFile[5]
                self.libelle = fromCvsFile[6]

                # Check variable
                # - dep
                if not self.dep:
                    self.logging.critical(f"Value '{self.dep}' is not a number !")
                # - reg
                if not self.reg:
                    self.logging.critical(f"Value '{self.reg}' is not a number !")
                # - nccenr
                if not self.nccenr:
                    self.logging.critical(f"Value '{self.nccenr}' is empty !")
                # - parent
                l_parent = None
                for parent in parent_list:
                    if parent.insee == self.reg:
                        l_parent = parent
                if not parent:
                    self.logging.critical(f"Parent not find with insee value '{self.reg}' !")

                # Create Localisation
                l_localisationForm = LocalisationForm(
                    data={
                        'code':self.dep,
                        'insee': int(re.compile("(\d+)").match(self.dep).group(1)), # required for 2A and 2B
                        'is_enable': True,
                        'is_linkeable': True,
                        'parent': l_parent,
                        'order': order
                    }
                )
                if l_localisationForm.is_valid() is False:
                    self.logging.critical(f"Error on Localisation with code={self.codeiso3}: {l_localisationForm.errors}")
                l_localisation = l_localisationForm.save(user=functionnalUser)

                # Create LocalisationData (FR)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.nccenr,
                        'resume': 'Département Français',
                        'language': LanguageAvailable.FR.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    self.logging.critical(f"Error on LocalisationData with name={self.libcog}: {l_localisationDataForm.errors}")
                l_localisationDataForm.save()

                # Create LocalisationData (EN)
                l_localisationDataForm = LocalisationDataForm(
                    data={
                        'name': self.nccenr,
                        'resume': 'French Department',
                        'language': LanguageAvailable.EN.value
                    }
                )
                if l_localisationDataForm.is_valid(localisation=l_localisation) is False:
                    self.logging.critical(f"Error on LocalisationData with name={self.libcog_en}: {l_localisationDataForm.errors}")
                l_localisationDataForm.save()

                # Register localisation
                mongo_list.append(l_localisation)

            def __repr__(self):
                return f"{self.__class__.__name__}: {self.dep} - {self.nccenr}"

            def __str__(self):
                return f"""{self.__class__.__name__}: \
dep = {self.dep}, reg = {self.reg}, cheflieu = {self.cheflieu}, tncc = {self.tncc}, ncc = {self.ncc}, nccenr = {self.nccenr}, libelle = {self.libelle}"""
