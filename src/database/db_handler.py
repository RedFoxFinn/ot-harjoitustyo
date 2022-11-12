# depends on sqlite3 database, import sqlite3 library for python3
# additionally depends on re, package to use regular expressions

import sqlite3
import re

# class implementation for Database_handler, class that will handle all interaction with sql-db

class Database_handler:
  # protected private variable for class that predefines strings for table creation step of a new database
  __table_creation = [
    "CREATE TABLE Products (id INTEGER PRIMARY KEY, name TEXT, type INTEGER, storage_life INTEGER)",
    "CREATE TABLE Types (id INTEGER PRIMARY KEY, type_name TEXT, subtype INTEGER)",
    "CREATE TABLE Subtypes (id INTEGER PRIMARY KEY, subtype_name)"
  ]

  # protected private variable for checking the database path
  __db_path_re = ["src/database/", ".db"]

  # protected private function to check validity of database path string
  # minimum length 17 characters (path + '.db' + db file name at least 1 character)
  # regular expressions: path contains "src/database/" path and file type extension '.db'
  def __check_db_path(self, str):
    str_length = True if len(str) >= 17 else False
    str_pt1_validity = True if re.search(self.__db_path_re[0],str) != None else False
    str_pt2_validity = True if re.search(self.__db_path_re[1],str) != None else False
    
    return True if str_length and str_pt1_validity and str_pt2_validity else False

  # class initialization, if db_set is True and database contains string with 
  def __init__(self,db_set,database):
    if db_set and database != None and self.__check_db_path(database):
      self._db = sqlite3.connect(database)
    else:
      self._db = sqlite3.connect("src/database/pantry.db")
      for item in self.__table_creation:
        try:
          self._db.execute(item)
        except:
          print("table already exists")

  def __str__(self):
    return "Pantry tietokanta"