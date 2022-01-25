from webbook.models.localisation import Localisation

SQL_MAP_CONTINENT = {
    202: {"code": "EUR", "parent": None},
    203: {"code": "AMR", "parent": None},
    204: {"code": "AMR", "parent": None},
    205: {"code": "AFR", "parent": None},
    206: {"code": "AFR", "parent": None},
    523: {"code": "AFR", "parent": None},
    207: {"code": "ASA", "parent": None},
    208: {"code": "OCE", "parent": None},
    209: "", #TODO: Find a match
    210: "", #TODO: Find a match
    211: {"code": "OCE", "parent": None}
}

SQL_MAP_COUNTRY = {
    # Europe - EUR
    401: {"code": "FRA", "parent": {"code": "EUR", "parent": None}}, # France
    402: {"code": "DEU", "parent": {"code": "EUR", "parent": None}},
    403: {"code": "AUT", "parent": {"code": "EUR", "parent": None}},
    404: {"code": "BEL", "parent": {"code": "EUR", "parent": None}},
    405: {"code": "CYP", "parent": {"code": "ASA", "parent": None}},
    406: {"code": "DNK", "parent": {"code": "EUR", "parent": None}},
    407: {"code": "ESP", "parent": {"code": "EUR", "parent": None}},
    408: {"code": "FIN", "parent": {"code": "EUR", "parent": None}},
    410: {"code": "GRC", "parent": {"code": "EUR", "parent": None}},
    411: {"code": "HUN", "parent": {"code": "EUR", "parent": None}},
    412: {"code": "IRL", "parent": {"code": "EUR", "parent": None}},
    413: {"code": "ISL", "parent": {"code": "EUR", "parent": None}},
    414: {"code": "ITA", "parent": {"code": "EUR", "parent": None}},
    415: {"code": "LUX", "parent": {"code": "EUR", "parent": None}},
    416: {"code": "MKD", "parent": {"code": "EUR", "parent": None}},
    417: {"code": "MLT", "parent": {"code": "EUR", "parent": None}},
    418: {"code": "MCO", "parent": {"code": "EUR", "parent": None}},
    419: {"code": "NOR", "parent": {"code": "EUR", "parent": None}},
    420: {"code": "NLD", "parent": {"code": "EUR", "parent": None}},
    421: {"code": "POL", "parent": {"code": "EUR", "parent": None}},
    422: {"code": "PRT", "parent": {"code": "EUR", "parent": None}},
    423: {"code": "ROU", "parent": {"code": "EUR", "parent": None}},
    424: {"code": "GBR", "parent": {"code": "EUR", "parent": None}},
    425: {"code": "SWE", "parent": {"code": "EUR", "parent": None}},
    426: {"code": "CHE", "parent": {"code": "EUR", "parent": None}},
    427: {"code": "UKR", "parent": {"code": "EUR", "parent": None}},

    # Asia - ASA
    463: {"code": "YEM", "parent": {"code": "ASA", "parent": None}},
    464: {"code": "VNM", "parent": {"code": "ASA", "parent": None}},
    465: {"code": "TUR", "parent": {"code": "ASA", "parent": None}},
    466: "", #TO,DO: Not found
    467: {"code": "THA", "parent": {"code": "ASA", "parent": None}},
    468: "", #TODO: Not found
    469: "", #TODO: Not found
    470: {"code": "LKA", "parent": {"code": "ASA", "parent": None}},
    471: {"code": "SGP", "parent": {"code": "ASA", "parent": None}},
    472: {"code": "PHL", "parent": {"code": "ASA", "parent": None}},
    473: {"code": "PSE", "parent": {"code": "ASA", "parent": None}},
    474: {"code": "PAK", "parent": {"code": "ASA", "parent": None}},
    475: {"code": "NPL", "parent": {"code": "ASA", "parent": None}},
    476: {"code": "MMR", "parent": {"code": "ASA", "parent": None}},
    477: {"code": "MNG", "parent": {"code": "ASA", "parent": None}},
    478: {"code": "MDV", "parent": {"code": "ASA", "parent": None}},
    479: {"code": "MYS", "parent": {"code": "ASA", "parent": None}},
    480: {"code": "LBN", "parent": {"code": "ASA", "parent": None}},
    481: {"code": "LAO", "parent": {"code": "ASA", "parent": None}},
    482: {"code": "KWT", "parent": {"code": "ASA", "parent": None}},
    483: {"code": "JOR", "parent": {"code": "ASA", "parent": None}},
    484: {"code": "JPN", "parent": {"code": "ASA", "parent": None}},
    485: {"code": "ISR", "parent": {"code": "ASA", "parent": None}},
    486: {"code": "IRN", "parent": {"code": "ASA", "parent": None}},
    487: {"code": "IRQ", "parent": {"code": "ASA", "parent": None}},
    488: {"code": "IDN", "parent": {"code": "ASA", "parent": None}},
    489: {"code": "IND", "parent": {"code": "ASA", "parent": None}},
    490: "", #TODO: Not found
    491: {"code": "ARE", "parent": {"code": "ASA", "parent": None}},
    492: {"code": "PRK", "parent": {"code": "ASA", "parent": None}}, #INFO: Choose PRK (South Corea}
    493: {"code": "CHN", "parent": {"code": "ASA", "parent": None}},
    494: {"code": "KHM", "parent": {"code": "ASA", "parent": None}},
    495: {"code": "BTN", "parent": {"code": "ASA", "parent": None}},
    496: {"code": "BGD", "parent": {"code": "ASA", "parent": None}},
    497: {"code": "ARM", "parent": {"code": "ASA", "parent": None}},
    498: {"code": "SAU", "parent": {"code": "ASA", "parent": None}},
    499: {"code": "AFG", "parent": {"code": "ASA", "parent": None}},

    # America - AMR
    500: {"code": "USA", "parent": {"code": "AMR", "parent": None}},
    501: {"code": "CAN", "parent": {"code": "AMR", "parent": None}},
    502: {"code": "MEX", "parent": {"code": "AMR", "parent": None}},
    503: "", #TODO: Where put this one ?
    504: {"code": "ARG", "parent": {"code": "AMR", "parent": None}},
    505: {"code": "CRI", "parent": {"code": "AMR", "parent": None}},
    506: {"code": "BOL", "parent": {"code": "AMR", "parent": None}},
    507: {"code": "BLZ", "parent": {"code": "AMR", "parent": None}},
    508: {"code": "BRA", "parent": {"code": "AMR", "parent": None}},
    509: {"code": "CHL", "parent": {"code": "AMR", "parent": None}},
    510: {"code": "COL", "parent": {"code": "AMR", "parent": None}},
    511: {"code": "ECU", "parent": {"code": "AMR", "parent": None}},
    512: {"code": "GTM", "parent": {"code": "AMR", "parent": None}},
    513: {"code": "GUY", "parent": {"code": "AMR", "parent": None}},
    514: {"code": "HND", "parent": {"code": "AMR", "parent": None}},
    515: {"code": "NIC", "parent": {"code": "AMR", "parent": None}},
    516: {"code": "PAN", "parent": {"code": "AMR", "parent": None}},
    517: {"code": "PRY", "parent": {"code": "AMR", "parent": None}},
    518: {"code": "PER", "parent": {"code": "AMR", "parent": None}},
    519: "", #TODO: Not found
    520: {"code": "URY", "parent": {"code": "AMR", "parent": None}},
    521: {"code": "VEN", "parent": {"code": "AMR", "parent": None}},
    522: "", #TODO: Where put this one ?

    # Africa - AFR
    524: {"code": "DZA", "parent": {"code": "AFR", "parent": None}},
    525: {"code": "AGO", "parent": {"code": "AFR", "parent": None}},
    526: {"code": "BEN", "parent": {"code": "AFR", "parent": None}},
    527: {"code": "BFA", "parent": {"code": "AFR", "parent": None}},
    528: {"code": "CMR", "parent": {"code": "AFR", "parent": None}},
    529: {"code": "CPV", "parent": {"code": "AFR", "parent": None}},
    530: {"code": "CAF", "parent": {"code": "AFR", "parent": None}},
    531: {"code": "COM", "parent": {"code": "AFR", "parent": None}},
    532: {"code": "COG", "parent": {"code": "AFR", "parent": None}},
    533: {"code": "CIV", "parent": {"code": "AFR", "parent": None}},
    534: {"code": "DJI", "parent": {"code": "AFR", "parent": None}},
    535: {"code": "EGY", "parent": {"code": "AFR", "parent": None}},
    536: {"code": "ETH", "parent": {"code": "AFR", "parent": None}},
    537: {"code": "GAB", "parent": {"code": "AFR", "parent": None}},
    538: {"code": "GMB", "parent": {"code": "AFR", "parent": None}},
    539: {"code": "GHA", "parent": {"code": "AFR", "parent": None}},
    540: {"code": "GNQ", "parent": {"code": "AFR", "parent": None}},
    541: {"code": "KEN", "parent": {"code": "AFR", "parent": None}},
    542: {"code": "LBR", "parent": {"code": "AFR", "parent": None}},
    543: {"code": "LBY", "parent": {"code": "AFR", "parent": None}},
    544: {"code": "MDG", "parent": {"code": "AFR", "parent": None}},
    545: {"code": "MLI", "parent": {"code": "AFR", "parent": None}},
    546: {"code": "MAR", "parent": {"code": "AFR", "parent": None}},
    547: {"code": "MRT", "parent": {"code": "AFR", "parent": None}},
    548: {"code": "MOZ", "parent": {"code": "AFR", "parent": None}},
    549: {"code": "NAM", "parent": {"code": "AFR", "parent": None}},
    550: {"code": "NER", "parent": {"code": "AFR", "parent": None}},
    551: {"code": "NGA", "parent": {"code": "AFR", "parent": None}},
    552: {"code": "UGA", "parent": {"code": "AFR", "parent": None}},
    553: {"code": "RWA", "parent": {"code": "AFR", "parent": None}},
    554: "", #TODO: Not found
    555: {"code": "SEN", "parent": {"code": "AFR", "parent": None}},
    556: "", #TODO: PAS DE PARENT ICI pour SYC
    557: {"code": "SLE", "parent": {"code": "AFR", "parent": None}},
    558: {"code": "SOM", "parent": {"code": "AFR", "parent": None}},
    559: {"code": "SDN", "parent": {"code": "AFR", "parent": None}},
    560: {"code": "TZA", "parent": {"code": "AFR", "parent": None}},
    561: {"code": "TCD", "parent": {"code": "AFR", "parent": None}},
    562: {"code": "TGO", "parent": {"code": "AFR", "parent": None}},
    563: {"code": "TUN", "parent": {"code": "AFR", "parent": None}},
    564: {"code": "ZMB", "parent": {"code": "AFR", "parent": None}},
    565: {"code": "ZWE", "parent": {"code": "AFR", "parent": None}},
    566: "", #TODO: Where put this one?
    567: "", #TODO: Where put this one?

    # Oceanie - OCE
    570: {"code": "AUS", "parent": {"code": "OCE", "parent": None}},
    571: {"code": "NZL", "parent": {"code": "OCE", "parent": None}},
    572: {"code": "FJI", "parent": {"code": "OCE", "parent": None}},
    573: "", #TODO: Where put this one?
    575: "", #TODO: Where put this one?
    576: "", #TODO: 'Ile Maurice' not found to not confuse with 'Maurice' !
    598: "", #TODO: Where put this one?
    599: "", #TODO: Where put this one?

    # Europe - EUR
    600: {"code": "ALB", "parent": {"code": "EUR", "parent": None}},
    601: {"code": "AND", "parent": {"code": "EUR", "parent": None}},
    603: {"code": "BLR", "parent": {"code": "EUR", "parent": None}},
    604: {"code": "BIH", "parent": {"code": "EUR", "parent": None}},
    605: {"code": "BGR", "parent": {"code": "EUR", "parent": None}},
    606: {"code": "HRV", "parent": {"code": "EUR", "parent": None}},
    607: {"code": "EST", "parent": {"code": "EUR", "parent": None}},
    608: "", #TODO: Not found
    609: "", #TODO: Not found
    610: "", #TODO: Not found
    611: "", #TODO: Not found
    612: {"code": "LIE", "parent": {"code": "EUR", "parent": None}},
    613: {"code": "LTU", "parent": {"code": "EUR", "parent": None}},
    614: {"code": "MDA", "parent": {"code": "EUR", "parent": None}},
    615: "", #TODO: Not found
    616: {"code": "RUS", "parent": {"code": "EUR", "parent": None}},
    617: {"code": "SMR", "parent": {"code": "EUR", "parent": None}},
    618: {"code": "SVK", "parent": {"code": "EUR", "parent": None}},
    619: {"code": "SVN", "parent": {"code": "EUR", "parent": None}},
    620: "", #TODO: Not found

    621: "" #TODO: Not found
}


SQL_MAP_FR_REGION = {
    301: {"insee": "44", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    302: {"insee": "75", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    303: {"insee": "84", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    304: {"insee": "28", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    305: {"insee": "27", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    306: {"insee": "53", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    307: {"insee": "24", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    308: {"insee": "44", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    309: {"insee": "94", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    311: {"insee": "27", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    312: {"insee": "28", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    313: {"insee": "11", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    314: {"insee": "76", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    315: {"insee": "75", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    316: {"insee": "44", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    317: {"insee": "76", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    318: {"insee": "32", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    319: {"insee": "52", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    320: {"insee": "32", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    321: {"insee": "75", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    322: {"insee": "93", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    323: {"insee": "84", "parent": {"code": "FRA", "parent": { "code": "EUR", "parent": None}}},
    325: "" #TODO: Which region to use for DOM-TOM ?
}


SQL_MAP_LIST = [
    SQL_MAP_CONTINENT,
    SQL_MAP_COUNTRY,
    SQL_MAP_FR_REGION
]
