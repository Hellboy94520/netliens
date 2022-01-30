from webbook.models.localisation import Localisation

SQL_MAP_CONTINENT = {
    202: Localisation.objects.get(code="EUR", parent=None),
    203: Localisation.objects.get(code="AMR", parent=None),
    204: Localisation.objects.get(code="AMR", parent=None),
    205: Localisation.objects.get(code="AFR", parent=None),
    206: Localisation.objects.get(code="AFR", parent=None),
    523: Localisation.objects.get(code="AFR", parent=None),
    207: Localisation.objects.get(code="ASA", parent=None),
    208: Localisation.objects.get(code="OCE", parent=None),
    209: "", #TODO: Find a match
    210: "", #TODO: Find a match
    211: Localisation.objects.get(code="OCE", parent=None)
}

SQL_MAP_COUNTRY = {
    # Europe - EUR
    401: Localisation.objects.get(code="FRA", parent=Localisation.objects.get(code="EUR", parent=None)), # France
    402: Localisation.objects.get(code="DEU", parent=Localisation.objects.get(code="EUR", parent=None)),
    403: Localisation.objects.get(code="AUT", parent=Localisation.objects.get(code="EUR", parent=None)),
    404: Localisation.objects.get(code="BEL", parent=Localisation.objects.get(code="EUR", parent=None)),
    405: Localisation.objects.get(code="CYP", parent=Localisation.objects.get(code="ASA", parent=None)),
    406: Localisation.objects.get(code="DNK", parent=Localisation.objects.get(code="EUR", parent=None)),
    407: Localisation.objects.get(code="ESP", parent=Localisation.objects.get(code="EUR", parent=None)),
    408: Localisation.objects.get(code="FIN", parent=Localisation.objects.get(code="EUR", parent=None)),
    410: Localisation.objects.get(code="GRC", parent=Localisation.objects.get(code="EUR", parent=None)),
    411: Localisation.objects.get(code="HUN", parent=Localisation.objects.get(code="EUR", parent=None)),
    412: Localisation.objects.get(code="IRL", parent=Localisation.objects.get(code="EUR", parent=None)),
    413: Localisation.objects.get(code="ISL", parent=Localisation.objects.get(code="EUR", parent=None)),
    414: Localisation.objects.get(code="ITA", parent=Localisation.objects.get(code="EUR", parent=None)),
    415: Localisation.objects.get(code="LUX", parent=Localisation.objects.get(code="EUR", parent=None)),
    416: Localisation.objects.get(code="MKD", parent=Localisation.objects.get(code="EUR", parent=None)),
    417: Localisation.objects.get(code="MLT", parent=Localisation.objects.get(code="EUR", parent=None)),
    418: Localisation.objects.get(code="MCO", parent=Localisation.objects.get(code="EUR", parent=None)),
    419: Localisation.objects.get(code="NOR", parent=Localisation.objects.get(code="EUR", parent=None)),
    420: Localisation.objects.get(code="NLD", parent=Localisation.objects.get(code="EUR", parent=None)),
    421: Localisation.objects.get(code="POL", parent=Localisation.objects.get(code="EUR", parent=None)),
    422: Localisation.objects.get(code="PRT", parent=Localisation.objects.get(code="EUR", parent=None)),
    423: Localisation.objects.get(code="ROU", parent=Localisation.objects.get(code="EUR", parent=None)),
    424: Localisation.objects.get(code="GBR", parent=Localisation.objects.get(code="EUR", parent=None)),
    425: Localisation.objects.get(code="SWE", parent=Localisation.objects.get(code="EUR", parent=None)),
    426: Localisation.objects.get(code="CHE", parent=Localisation.objects.get(code="EUR", parent=None)),
    427: Localisation.objects.get(code="UKR", parent=Localisation.objects.get(code="EUR", parent=None)),

    # Asia - ASA
    463: Localisation.objects.get(code="YEM", parent=Localisation.objects.get(code="ASA", parent=None)),
    464: Localisation.objects.get(code="VNM", parent=Localisation.objects.get(code="ASA", parent=None)),
    465: Localisation.objects.get(code="TUR", parent=Localisation.objects.get(code="ASA", parent=None)),
    466: "", #TO,DO: Not found
    467: Localisation.objects.get(code="THA", parent=Localisation.objects.get(code="ASA", parent=None)),
    468: "", #TODO: Not found
    469: "", #TODO: Not found
    470: Localisation.objects.get(code="LKA", parent=Localisation.objects.get(code="ASA", parent=None)),
    471: Localisation.objects.get(code="SGP", parent=Localisation.objects.get(code="ASA", parent=None)),
    472: Localisation.objects.get(code="PHL", parent=Localisation.objects.get(code="ASA", parent=None)),
    473: Localisation.objects.get(code="PSE", parent=Localisation.objects.get(code="ASA", parent=None)),
    474: Localisation.objects.get(code="PAK", parent=Localisation.objects.get(code="ASA", parent=None)),
    475: Localisation.objects.get(code="NPL", parent=Localisation.objects.get(code="ASA", parent=None)),
    476: Localisation.objects.get(code="MMR", parent=Localisation.objects.get(code="ASA", parent=None)),
    477: Localisation.objects.get(code="MNG", parent=Localisation.objects.get(code="ASA", parent=None)),
    478: Localisation.objects.get(code="MDV", parent=Localisation.objects.get(code="ASA", parent=None)),
    479: Localisation.objects.get(code="MYS", parent=Localisation.objects.get(code="ASA", parent=None)),
    480: Localisation.objects.get(code="LBN", parent=Localisation.objects.get(code="ASA", parent=None)),
    481: Localisation.objects.get(code="LAO", parent=Localisation.objects.get(code="ASA", parent=None)),
    482: Localisation.objects.get(code="KWT", parent=Localisation.objects.get(code="ASA", parent=None)),
    483: Localisation.objects.get(code="JOR", parent=Localisation.objects.get(code="ASA", parent=None)),
    484: Localisation.objects.get(code="JPN", parent=Localisation.objects.get(code="ASA", parent=None)),
    485: Localisation.objects.get(code="ISR", parent=Localisation.objects.get(code="ASA", parent=None)),
    486: Localisation.objects.get(code="IRN", parent=Localisation.objects.get(code="ASA", parent=None)),
    487: Localisation.objects.get(code="IRQ", parent=Localisation.objects.get(code="ASA", parent=None)),
    488: Localisation.objects.get(code="IDN", parent=Localisation.objects.get(code="ASA", parent=None)),
    489: Localisation.objects.get(code="IND", parent=Localisation.objects.get(code="ASA", parent=None)),
    490: "", #TODO: Not found
    491: Localisation.objects.get(code="ARE", parent=Localisation.objects.get(code="ASA", parent=None)),
    492: Localisation.objects.get(code="PRK", parent=Localisation.objects.get(code="ASA", parent=None)), #INFO: Choose PRK (South Corea)
    493: Localisation.objects.get(code="CHN", parent=Localisation.objects.get(code="ASA", parent=None)),
    494: Localisation.objects.get(code="KHM", parent=Localisation.objects.get(code="ASA", parent=None)),
    495: Localisation.objects.get(code="BTN", parent=Localisation.objects.get(code="ASA", parent=None)),
    496: Localisation.objects.get(code="BGD", parent=Localisation.objects.get(code="ASA", parent=None)),
    497: Localisation.objects.get(code="ARM", parent=Localisation.objects.get(code="ASA", parent=None)),
    498: Localisation.objects.get(code="SAU", parent=Localisation.objects.get(code="ASA", parent=None)),
    499: Localisation.objects.get(code="AFG", parent=Localisation.objects.get(code="ASA", parent=None)),

    # America - AMR
    500: Localisation.objects.get(code="USA", parent=Localisation.objects.get(code="AMR", parent=None)),
    501: Localisation.objects.get(code="CAN", parent=Localisation.objects.get(code="AMR", parent=None)),
    502: Localisation.objects.get(code="MEX", parent=Localisation.objects.get(code="AMR", parent=None)),
    503: "", #TODO: Where put this one ?
    504: Localisation.objects.get(code="ARG", parent=Localisation.objects.get(code="AMR", parent=None)),
    505: Localisation.objects.get(code="CRI", parent=Localisation.objects.get(code="AMR", parent=None)),
    506: Localisation.objects.get(code="BOL", parent=Localisation.objects.get(code="AMR", parent=None)),
    507: Localisation.objects.get(code="BLZ", parent=Localisation.objects.get(code="AMR", parent=None)),
    508: Localisation.objects.get(code="BRA", parent=Localisation.objects.get(code="AMR", parent=None)),
    509: Localisation.objects.get(code="CHL", parent=Localisation.objects.get(code="AMR", parent=None)),
    510: Localisation.objects.get(code="COL", parent=Localisation.objects.get(code="AMR", parent=None)),
    511: Localisation.objects.get(code="ECU", parent=Localisation.objects.get(code="AMR", parent=None)),
    512: Localisation.objects.get(code="GTM", parent=Localisation.objects.get(code="AMR", parent=None)),
    513: Localisation.objects.get(code="GUY", parent=Localisation.objects.get(code="AMR", parent=None)),
    514: Localisation.objects.get(code="HND", parent=Localisation.objects.get(code="AMR", parent=None)),
    515: Localisation.objects.get(code="NIC", parent=Localisation.objects.get(code="AMR", parent=None)),
    516: Localisation.objects.get(code="PAN", parent=Localisation.objects.get(code="AMR", parent=None)),
    517: Localisation.objects.get(code="PRY", parent=Localisation.objects.get(code="AMR", parent=None)),
    518: Localisation.objects.get(code="PER", parent=Localisation.objects.get(code="AMR", parent=None)),
    519: "", #TODO: Not found
    520: Localisation.objects.get(code="URY", parent=Localisation.objects.get(code="AMR", parent=None)),
    521: Localisation.objects.get(code="VEN", parent=Localisation.objects.get(code="AMR", parent=None)),
    522: "", #TODO: Where put this one ?

    # Africa - AFR
    524: Localisation.objects.get(code="DZA", parent=Localisation.objects.get(code="AFR", parent=None)),
    525: Localisation.objects.get(code="AGO", parent=Localisation.objects.get(code="AFR", parent=None)),
    526: Localisation.objects.get(code="BEN", parent=Localisation.objects.get(code="AFR", parent=None)),
    527: Localisation.objects.get(code="BFA", parent=Localisation.objects.get(code="AFR", parent=None)),
    528: Localisation.objects.get(code="CMR", parent=Localisation.objects.get(code="AFR", parent=None)),
    529: Localisation.objects.get(code="CPV", parent=Localisation.objects.get(code="AFR", parent=None)),
    530: Localisation.objects.get(code="CAF", parent=Localisation.objects.get(code="AFR", parent=None)),
    531: Localisation.objects.get(code="COM", parent=Localisation.objects.get(code="AFR", parent=None)),
    532: Localisation.objects.get(code="COG", parent=Localisation.objects.get(code="AFR", parent=None)),
    533: Localisation.objects.get(code="CIV", parent=Localisation.objects.get(code="AFR", parent=None)),
    534: Localisation.objects.get(code="DJI", parent=Localisation.objects.get(code="AFR", parent=None)),
    535: Localisation.objects.get(code="EGY", parent=Localisation.objects.get(code="AFR", parent=None)),
    536: Localisation.objects.get(code="ETH", parent=Localisation.objects.get(code="AFR", parent=None)),
    537: Localisation.objects.get(code="GAB", parent=Localisation.objects.get(code="AFR", parent=None)),
    538: Localisation.objects.get(code="GMB", parent=Localisation.objects.get(code="AFR", parent=None)),
    539: Localisation.objects.get(code="GHA", parent=Localisation.objects.get(code="AFR", parent=None)),
    540: Localisation.objects.get(code="GNQ", parent=Localisation.objects.get(code="AFR", parent=None)),
    541: Localisation.objects.get(code="KEN", parent=Localisation.objects.get(code="AFR", parent=None)),
    542: Localisation.objects.get(code="LBR", parent=Localisation.objects.get(code="AFR", parent=None)),
    543: Localisation.objects.get(code="LBY", parent=Localisation.objects.get(code="AFR", parent=None)),
    544: Localisation.objects.get(code="MDG", parent=Localisation.objects.get(code="AFR", parent=None)),
    545: Localisation.objects.get(code="MLI", parent=Localisation.objects.get(code="AFR", parent=None)),
    546: Localisation.objects.get(code="MAR", parent=Localisation.objects.get(code="AFR", parent=None)),
    547: Localisation.objects.get(code="MRT", parent=Localisation.objects.get(code="AFR", parent=None)),
    548: Localisation.objects.get(code="MOZ", parent=Localisation.objects.get(code="AFR", parent=None)),
    549: Localisation.objects.get(code="NAM", parent=Localisation.objects.get(code="AFR", parent=None)),
    550: Localisation.objects.get(code="NER", parent=Localisation.objects.get(code="AFR", parent=None)),
    551: Localisation.objects.get(code="NGA", parent=Localisation.objects.get(code="AFR", parent=None)),
    552: Localisation.objects.get(code="UGA", parent=Localisation.objects.get(code="AFR", parent=None)),
    553: Localisation.objects.get(code="RWA", parent=Localisation.objects.get(code="AFR", parent=None)),
    554: "", #TODO: Not found
    555: Localisation.objects.get(code="SEN", parent=Localisation.objects.get(code="AFR", parent=None)),
    556: "", #TODO: PAS DE PARENT ICI pour SYC
    557: Localisation.objects.get(code="SLE", parent=Localisation.objects.get(code="AFR", parent=None)),
    558: Localisation.objects.get(code="SOM", parent=Localisation.objects.get(code="AFR", parent=None)),
    559: Localisation.objects.get(code="SDN", parent=Localisation.objects.get(code="AFR", parent=None)),
    560: Localisation.objects.get(code="TZA", parent=Localisation.objects.get(code="AFR", parent=None)),
    561: Localisation.objects.get(code="TCD", parent=Localisation.objects.get(code="AFR", parent=None)),
    562: Localisation.objects.get(code="TGO", parent=Localisation.objects.get(code="AFR", parent=None)),
    563: Localisation.objects.get(code="TUN", parent=Localisation.objects.get(code="AFR", parent=None)),
    564: Localisation.objects.get(code="ZMB", parent=Localisation.objects.get(code="AFR", parent=None)),
    565: Localisation.objects.get(code="ZWE", parent=Localisation.objects.get(code="AFR", parent=None)),
    566: "", #TODO: Where put this one?
    567: "", #TODO: Where put this one?

    # Oceanie - OCE
    570: Localisation.objects.get(code="AUS", parent=Localisation.objects.get(code="OCE", parent=None)),
    571: Localisation.objects.get(code="NZL", parent=Localisation.objects.get(code="OCE", parent=None)),
    572: Localisation.objects.get(code="FJI", parent=Localisation.objects.get(code="OCE", parent=None)),
    573: "", #TODO: Where put this one?
    575: "", #TODO: Where put this one?
    576: "", #TODO: 'Ile Maurice' not found to not confuse with 'Maurice' !
    598: "", #TODO: Where put this one?
    599: "", #TODO: Where put this one?

    # Europe - EUR
    600: Localisation.objects.get(code="ALB", parent=Localisation.objects.get(code="EUR", parent=None)),
    601: Localisation.objects.get(code="AND", parent=Localisation.objects.get(code="EUR", parent=None)),
    603: Localisation.objects.get(code="BLR", parent=Localisation.objects.get(code="EUR", parent=None)),
    604: Localisation.objects.get(code="BIH", parent=Localisation.objects.get(code="EUR", parent=None)),
    605: Localisation.objects.get(code="BGR", parent=Localisation.objects.get(code="EUR", parent=None)),
    606: Localisation.objects.get(code="HRV", parent=Localisation.objects.get(code="EUR", parent=None)),
    607: Localisation.objects.get(code="EST", parent=Localisation.objects.get(code="EUR", parent=None)),
    608: "", #TODO: Not found
    609: "", #TODO: Not found
    610: "", #TODO: Not found
    611: "", #TODO: Not found
    612: Localisation.objects.get(code="LIE", parent=Localisation.objects.get(code="EUR", parent=None)),
    613: Localisation.objects.get(code="LTU", parent=Localisation.objects.get(code="EUR", parent=None)),
    614: Localisation.objects.get(code="MDA", parent=Localisation.objects.get(code="EUR", parent=None)),
    615: "", #TODO: Not found
    616: Localisation.objects.get(code="RUS", parent=Localisation.objects.get(code="EUR", parent=None)),
    617: Localisation.objects.get(code="SMR", parent=Localisation.objects.get(code="EUR", parent=None)),
    618: Localisation.objects.get(code="SVK", parent=Localisation.objects.get(code="EUR", parent=None)),
    619: Localisation.objects.get(code="SVN", parent=Localisation.objects.get(code="EUR", parent=None)),
    620: "", #TODO: Not found

    621: "" #TODO: Not found
}

FRANCE = Localisation.objects.get(code="FRA", parent=Localisation.objects.get(code="EUR", parent=None))

SQL_MAP_FR_REGION = {
    301: Localisation.objects.get(insee=44, parent=FRANCE),
    302: Localisation.objects.get(insee=75, parent=FRANCE),
    303: Localisation.objects.get(insee=84, parent=FRANCE),
    304: Localisation.objects.get(insee=28, parent=FRANCE),
    305: Localisation.objects.get(insee=27, parent=FRANCE),
    306: Localisation.objects.get(insee=53, parent=FRANCE),
    307: Localisation.objects.get(insee=24, parent=FRANCE),
    308: Localisation.objects.get(insee=44, parent=FRANCE),
    309: Localisation.objects.get(insee=94, parent=FRANCE),
    311: Localisation.objects.get(insee=27, parent=FRANCE),
    312: Localisation.objects.get(insee=28, parent=FRANCE),
    313: Localisation.objects.get(insee=11, parent=FRANCE),
    314: Localisation.objects.get(insee=76, parent=FRANCE),
    315: Localisation.objects.get(insee=75, parent=FRANCE),
    316: Localisation.objects.get(insee=44, parent=FRANCE),
    317: Localisation.objects.get(insee=76, parent=FRANCE),
    318: Localisation.objects.get(insee=32, parent=FRANCE),
    319: Localisation.objects.get(insee=52, parent=FRANCE),
    320: Localisation.objects.get(insee=32, parent=FRANCE),
    321: Localisation.objects.get(insee=75, parent=FRANCE),
    322: Localisation.objects.get(insee=93, parent=FRANCE),
    323: Localisation.objects.get(insee=84, parent=FRANCE),
    325: "" #TODO: Which region to use for DOM-TOM ?
}


SQL_MAP_LIST = [
    SQL_MAP_CONTINENT,
    SQL_MAP_COUNTRY,
    SQL_MAP_FR_REGION
]
