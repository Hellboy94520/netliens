from faulthandler import is_enabled
from importlib.resources import contents
from webbook.models.localisation import Localisation, LocalisationData
from webbook.models.language import LanguageAvailable
from .localisation_mapping import SQL_MAP_LIST


from re import compile
from os.path import join
from datetime import datetime

CONTINENT_SQL_ASSOCIATION = {

}
CONTINENT_SQL_ASSOCIATION_2 = {
    "EUR": [202],
    "AMR": [203, 204],
    "AFR": [205, 206],
    "ASA": [207],
    "OCE": [208, 211],
    "UNKNOWN": [209, 210] #TODO: Find a match for that one
}

INSEE_KEY = "InseeData"

def __toInteger(value: str):
    try:
        result = int(value)
    except ValueError:
        return None
    else:
        return result

def __toLowerCase(value: str):
    regexp = compile("[\w\ \-\']+")
    string = regexp.match(value)
    if not string:
        return None
    lower_string = string[0].lower()
    string = lower_string.title()
    return string

def __getCsv(cvsFile, cvsDelimiter):
    import csv
    try:
        cvsFile = open(cvsFile, newline='', encoding='utf-8')
    except IOError as e:
        raise f"File '{cvsFile}' not found: {e}"
    else:
        spamreader = csv.reader(cvsFile, delimiter=cvsDelimiter, quotechar='|')
        next(spamreader) # Avoid first line
        return spamreader

def __getContinent(importUser, inseePath, sqlConfig):
    DELIMITER = ";"
    INI_KEY = "continent"

    contents = __getCsv(
        cvsFile=join(inseePath, sqlConfig.get(INSEE_KEY, INI_KEY)),
        cvsDelimiter=DELIMITER
    )

    for content in contents:
        localisation = Localisation.objects.create(
            code = content[4],
            insee = __toInteger(content[0]),
            is_enable = True,
            creation_user = importUser,
            approval_date = datetime.now(),
            approval_user = importUser
        )
        LocalisationData.objects.create(
            name = __toLowerCase(content[1]),
            resume = "Continent",
            language = LanguageAvailable.FR.value,
            localisation = localisation
        )
        LocalisationData.objects.create(
            name = __toLowerCase(content[2]),
            resume = "Continent",
            language = LanguageAvailable.EN.value,
            localisation = localisation
        )

def __getCountry(importUser, inseePath, sqlConfig):
    """
        File template:
        00 - cog
        01 - actual
        02 - capay
        03 - crpay
        04 - ani
        05 - libcog
        06 - libenr
        07 - ancnom
        08 - codeiso2
        09 - codeiso3
        10 - codenum3
    """
    EXPECTED_COLUMN = 11
    DELIMETER = ";"
    INI_KEY = "country"

    contents = __getCsv(
        cvsFile=join(inseePath, sqlConfig.get(INSEE_KEY, INI_KEY)),
        cvsDelimiter=DELIMETER
    )

    for line, content in enumerate(contents):
        # Verifying Variables from csv
        assert len(content)==EXPECTED_COLUMN, f"Column out of range on line '{line+1}', expected '{EXPECTED_COLUMN}', I have {len(content)}: {content}"
        assert content[0], f"Cog content is empty on line '{line+1}'"
        assert content[5], f"Libcog is empty on line '{line+1}'"
        assert content[9], f"Codeiso3 is empty on line '{line+1}'"

        # Verifying parent is existing
        parent_insee = int(str(__toInteger(content[0]))[:3])*100
        assert Localisation.objects.filter(insee=parent_insee).count()==1, f"Impossible to find a parent with an Insee value equal to {parent_insee}' on line '{line+1}'"

        # Generate Model
        localisation = Localisation.objects.create(
            code = content[9],
            insee = content[0],
            is_enable = True,
            creation_user = importUser,
            approval_date = datetime.now(),
            approval_user = importUser,
            parent = Localisation.objects.get(insee=parent_insee)
        )
        LocalisationData.objects.create(
            name = __toLowerCase(content[5]),
            resume = "Pays",
            language = LanguageAvailable.FR.value,
            localisation = localisation
        )

def __getFranceFromDb():
    # Get France Localisation to continue
    FRANCE_NAME = "France"
    franceData = LocalisationData.objects.filter(name=FRANCE_NAME, language=LanguageAvailable.FR.value)
    assert franceData.count() == 1, f"Impossible to find a parent with a name value equal to '{FRANCE_NAME}'"
    return franceData[0].localisation

def __getRegion(importUser, inseePath, sqlConfig, france):
    """
        File template:
        00 - reg
        01 - cheflieu
        02 - tncc
        03 - ncc
        04 - nccenr
        05 - libelle
    """

    EXPECTED_COLUMN = 6
    DELIMETER = ","
    INI_KEY = "region"

    contents = __getCsv(
        cvsFile=join(inseePath, sqlConfig.get(INSEE_KEY, INI_KEY)),
        cvsDelimiter=DELIMETER
    )

    for line, content in enumerate(contents):
        # Verifying Variables from csv
        assert len(content)==EXPECTED_COLUMN, f"Column out of range on line '{line+1}', expected '{EXPECTED_COLUMN}', I have {len(content)}: {content}"
        assert content[0], f"Reg content is empty on line '{line+1}'"
        assert content[4], f"Codeiso3 is empty on line '{line+1}'"

        # Generate Model
        localisation = Localisation.objects.create(
            code = "",
            insee = __toInteger(content[0]),
            is_enable = True,
            creation_user = importUser,
            approval_date = datetime.now(),
            approval_user = importUser,
            parent = france
        )
        LocalisationData.objects.create(
            name = __toLowerCase(content[4]),
            resume = "Région Française",
            language = LanguageAvailable.FR.value,
            localisation = localisation
        )

def __getDepartment(importUser, inseePath, sqlConfig, france):
    """
        File template:
        00 - dep
        01 - reg
        02 - cheflieu
        03 - tncc
        04 - ncc
        05 - nccenr
        06 - libelle
    """
    EXPECTED_COLUMN = 7
    DELIMETER = ";"
    INI_KEY = "departement"

    contents = __getCsv(
        cvsFile=join(inseePath, sqlConfig.get(INSEE_KEY, INI_KEY)),
        cvsDelimiter=DELIMETER
    )

    for line, content in enumerate(contents):
        # Verifying Variables from csv
        assert len(content)==EXPECTED_COLUMN, f"Column out of range on line '{line+1}', expected '{EXPECTED_COLUMN}', I have {len(content)}: {content}"
        assert content[0], f"Dep content is empty on line '{line+1}'"
        assert content[1], f"Reg is empty on line '{line+1}'"
        assert content[5], f"Nccenr is empty on line '{line+1}'"

        # Verifying parent is existing
        parent_insee = __toInteger(content[1])
        parent = Localisation.objects.filter(insee=parent_insee, parent=france)
        assert parent.count()==1, f"Impossible to find a parent with an Insee value equal to {parent_insee}' on line '{line+1}'"
        parent = parent[0]

        # Generate Model
        localisation = Localisation.objects.create(
            code = "",
            insee = __toInteger(content[0]),
            is_enable = True,
            creation_user = importUser,
            approval_date = datetime.now(),
            approval_user = importUser,
            parent = parent
        )
        LocalisationData.objects.create(
            name = content[5],
            resume = "Département Français",
            language = LanguageAvailable.FR.value,
            localisation = localisation
        )

def generateModels(importUser, inseePath, sqlConfig):
    __getContinent(importUser, inseePath, sqlConfig)
    __getCountry(importUser, inseePath, sqlConfig)

    france = __getFranceFromDb()

    __getRegion(importUser, inseePath, sqlConfig, france)
    __getDepartment(importUser, inseePath, sqlConfig, france)

def sqlAssociation(sqlKey: int) -> Localisation:
    for map in SQL_MAP_LIST:
        # Read map with key
        filters = map.get(sqlKey, None)
        # If key is find, but value is empty, it is an error
        assert filters != "", f"Key '{sqlKey}' has not value in '{map.__name__}' map"
        # If no key find, we continue to search in another map
        if filters is None:
            continue
        # If key find, return value
        return Localisation.objects.get(*filters)
    # If that part is reach, key does not exist on all map
    raise f"Key '{sqlKey}' not find on any SQL_MAPS"
