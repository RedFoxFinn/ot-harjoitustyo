import os
import re

_db_path_re = ["src/services/", ".db"]


def validate_database_path(db_str: str):
    """
    function to check validity of database path string
    minimum length 17 characters (path + '.db' + db file name at least 1 character)
    regular expressions: path contains "src/database/" path and file type extension '.db'
    """
    str_length = bool(len(db_str) >= 17)
    str_pt1_validity = bool(re.search(_db_path_re[0], db_str))
    str_pt2_validity = bool(re.search(_db_path_re[1], db_str))

    return bool(str_length and str_pt1_validity and str_pt2_validity)


def validate_database_existence(db_path=None):
    """
    function to check existence of database in given path
    """
    return os.path.isfile(db_path)
