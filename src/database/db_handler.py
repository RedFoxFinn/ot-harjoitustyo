# depends on sqlite3 database, import sqlite3 library for python3
# additionally depends on re, package to use regular expressions

import sqlite3
import re
import os

# class implementation for Database_handler, class that will handle all interaction with sql-db
class Database_handler:
  # protected private variable for class that predefines strings for table creation step of a new database
  __table_creation = [
    "CREATE TABLE Products (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, type INTEGER NOT NULL, subtype DEFAULT 0, storage_life INTEGER NOT NULL)",
    "CREATE TABLE Types (id INTEGER PRIMARY KEY, type_name TEXT NOT NULL UNIQUE)",
    "CREATE TABLE Subtypes (id INTEGER PRIMARY KEY, subtype_name TEXT NOT NULL UNIQUE, type INTEGER NOT NULL)"
  ]

  __subtype_creation = [
    "Hedelmät",
    "Juomajauheet",
    "Juomatiivisteet",
    "Kalat",
    "Kasvikset",
    "Leivonta",
    "Lihat",
    "Maitotuotteet",
    "Marjat",
    "Mausteet",
    "Maustekastikkeet",
    "Munat",
    "Puolivalmisteet",
    "Rasvat, öljyt",
    "Ravintojauheet",
    "Sokerit",
    "Säilykkeet",
    "Vihannekset",
    "Viljatuotteet"
  ]

  __type_creation = [
    "Juomat",
    "Ruoat",
    "Raaka-aineet"
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

  # class initialization
  # > if db_set is True
  # > database contains valid database path
  # > path leads to valid file
  # >> connect to database file
  # > else create new database with automatic table creation
  def __init__(self,db_set,database):
    if db_set and database != None and self.__check_db_path(database) and os.path.isfilget_subtypecounte(database):
      self._db = sqlite3.connect(database)
    else:
      self._db = sqlite3.connect("src/database/pantry.db")
      for item in self.__table_creation:
        try:
          self._db.execute(item)
        except:
          print("table already exists")
      
      for item in self.__type_creation:
        self.add_type(item)
      
      __type_id = self._db.execute("SELECT id FROM Types WHERE type_name=?",["Raaka-aineet"]).fetchone()[0]
      
      for item in self.__subtype_creation:
        self.add_subtype(item, __type_id)

    self._db.isolation_level=None
  
  # function for adding new product with its name, type, subtype and storage_life as arguments

  # function for fetching products from db
  # returns None if no product in db
  # joins Product with Type and conditionally joins with Subtype if Product.subtype has value greater than 0
  def get_products(self):
    products = self._db.execute("SELECT R.*, S.subtype_name AS subtype_name FROM (SELECT P.id AS pid, P.name AS pname, P.storage_life AS storage_life, T.type_name AS type_name, P.subtype AS sid FROM Products P LEFT JOIN Types T ON P.type=T.id) R LEFT JOIN Subtypes S ON R.sid AND R.sid=S.id").fetchall()
    return products if len(products) > 0 else None

  # function for adding new type with its name as argument
  # optional argument subtype (integer which is the id of subtype)
  def add_type(self,name:str):
    try:
      self._db.execute("INSERT INTO Types (type_name) VALUES (?)", [name])
      return True
    except:
      return False

  # function for fetching types from db
  # returns None if no types in db
  def get_types(self):
    types = self._db.execute("SELECT type_name FROM Types").fetchall()
    return types if len(types) > 0 else None
  
  # function for fetching number of types in db
  def get_typecount(self):
    count = self._db.execute("SELECT count(*) FROM Types").fetchall()[0][0]
    return count

  # function for adding new subtype with its name as argument
  # adding fails, if exact same name already exists in db
  def add_subtype(self,name:str, type:int):
    try:
      self._db.execute("INSERT INTO Subtypes (subtype_name, type) VALUES (?,?)",[name,type])
      return True
    except:
      return False
  
  # function for fetching subtypes from db
  # returns None if no subtypes in db
  def get_subtypes(self):
    subtypes = self._db.execute("SELECT type_name, subtype_name FROM Subtypes S LEFT JOIN Types T ON S.type=T.id").fetchall()
    return subtypes if len(subtypes) > 0 else None

  # function for fetching number of subtypes in db
  def get_subtypecount(self):
    count = self._db.execute("SELECT count(*) FROM Subtypes").fetchall()[0][0]
    return count

  # function for deleting a subtype from db with its name as argument
  # TODO

  # function for returning db status (???)
  def __str__(self):
    return "Pantry tietokanta"