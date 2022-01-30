from os.path import abspath
from configparser import ConfigParser, ExtendedInterpolation


def parseSqlConfig(file: str):
    try:
        sql_config = ConfigParser()
        sql_config._interpolation = ExtendedInterpolation()
        sql_config.read(file)
    except:
        raise Exception(f"[ERROR] Impossible to parse SQL Configuration file '{SQL_CONFIG_PATH}'")

    return sql_config
