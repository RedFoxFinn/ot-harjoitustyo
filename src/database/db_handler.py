# depends on sqlite3 database, import sqlite3 library for python3
# additionally depends on re, package to use regular expressions

import sqlite3
import re
import os

# class implementation for Database_handler, class that will handle all interaction with sql-db


class DatabaseHandler:
  # protected private variable for class that predefines
  # strings for table creation step of a new database
    __table_creation = [
        """CREATE TABLE Products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            type INTEGER NOT NULL,
            subtype INTEGER NOT NULL,
            storage_life INTEGER NOT NULL,
            number_of INTEGER NOT NULL
        )""",
        """CREATE TABLE Types (
            id INTEGER PRIMARY KEY,
            type_name TEXT NOT NULL UNIQUE
        )""",
        """CREATE TABLE Subtypes (
            id INTEGER PRIMARY KEY,
            subtype_name TEXT NOT NULL UNIQUE,
            type INTEGER NOT NULL
        )"""
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
    def __check_db_path(self, db_str: str):
        str_length = bool(len(db_str) >= 17)
        str_pt1_validity = bool(re.search(self.__db_path_re[0], db_str))
        str_pt2_validity = bool(re.search(self.__db_path_re[1], db_str))

        return bool(str_length and str_pt1_validity and str_pt2_validity)

    def __check_validity(self, db_path):
        if db_path is not None:
            return self.__check_db_path(db_path)
        return False

    def __fetch_typeid(self, typename: str):
        return self._db.execute("SELECT id FROM Types WHERE type_name=?", [typename]).fetchone()

    # class initialization
    # > if db_set is True
    # > database contains valid database path
    # > path leads to valid file
    # >> connect to database file
    # > else create new database with automatic table creation
    def __init__(self, db_set: bool, database: str):  # pylint: disable=too-many-statements
        if db_set and self.__check_validity(database) and os.path.isfile(database):
            self._db = sqlite3.connect(database)
        elif not db_set and database is not None and self.__check_db_path(database):
            self._db = sqlite3.connect(database)
            for item in self.__table_creation:
                try:
                    self._db.execute(item)
                except:  # pylint: disable=bare-except
                    print("table already exists")
            for item in self.__type_creation:
                self.add_type(item)
            __type_id = self.__fetch_typeid("Raaka-aineet")[0]
            for item in self.__subtype_creation:
                self.add_subtype(item, __type_id)
        else:
            self._db = sqlite3.connect("src/database/pantry.db")
            for item in self.__table_creation:
                try:
                    self._db.execute(item)
                except:  # pylint: disable=bare-except
                    print("table already exists")
            for item in self.__type_creation:
                self.add_type(item)
            __type_id = self.__fetch_typeid("Raaka-aineet")[0]
            for item in self.__subtype_creation:
                self.add_subtype(item, __type_id)
        self._db.isolation_level = None

    # function for adding new product with its name,
    # type, subtype and storage_life as arguments
    # name (string), type (int) and storage_life (int) needed,
    # subtype (int) optional, count (int) optional
    def add_product(self,
                    name: str,
                    type_of: int,
                    storage_life: int,
                    subtype: int = 0,
                    count: int = 1):
        try:
            self._db.execute("""
                INSERT INTO Products (
                    name,
                    type,
                    subtype,
                    storage_life,
                    number_of
                ) VALUES (?,?,?,?,?)""", [name, type_of, subtype, storage_life, count])
            return True
        except:  # pylint: disable=bare-except
            return False

    # function for fetching products from db
    # returns None if no product in db
    # joins Product with Type and conditionally joins with Subtype
    # if Product.subtype has value greater than 0
    def get_products(self):
        products = self._db.execute("""
            SELECT
                R.*,
                S.subtype_name AS subtype_name FROM (
                    SELECT
                        P.id AS pid,
                        P.name AS pname,
                        P.storage_life AS storage_life,
                        P.number_of AS number_of,
                        T.type_name AS type_name,
                        P.subtype AS sid FROM
                            Products P LEFT JOIN Types T
                                ON P.type=T.id) R LEFT JOIN Subtypes S
                                    ON R.sid AND R.sid=S.id
        """).fetchall()
        return products if len(products) > 0 else None

    # function for fetching number of products in db
    def get_productcount(self):
        count = self._db.execute(
            "SELECT count(*) FROM Products").fetchall()[0][0]
        return count

    # function for removing product from db
    def remove_product(self, product_id: int):
        try:
            self._db.execute("DELETE FROM Products WHERE id=?", [product_id])
            return True
        except:  # pylint: disable=bare-except
            return False

    # function for updating number of products with certain id
    def update_count(self, product_id: int, change: int = 1, subtract: bool = True):
        _product = self._db.execute("""
            SELECT id, number_of FROM Products WHERE id=?
        """, [product_id]).fetchone()
        if subtract and _product[1]-change == 0:
            return self.remove_product(product_id)
        elif subtract:
            try:
                self._db.execute("""
                    UPDATE Products SET number_of=number_of-? WHERE id=?
                """, [change, product_id])
                return True
            except:  # pylint: disable=bare-except
                return False
        else:
            try:
                self._db.execute("""
                    UPDATE Products SET number_of=number_of+? WHERE id=?
                """, [change, product_id])
                return True
            except:  # pylint: disable=bare-except
                return False

    # function for adding new type with its name as argument
    # optional argument subtype (integer which is the id of subtype)
    def add_type(self, name: str):
        try:
            self._db.execute(
                "INSERT INTO Types (type_name) VALUES (?)", [name])
            return True
        except:  # pylint: disable=bare-except
            return False

    # function for fetching types from db
    # returns None if no types in db
    def get_types(self):
        types = self._db.execute("SELECT type_name, id FROM Types").fetchall()
        return types if len(types) > 0 else None

    # function for fetching number of types in db
    def get_typecount(self):
        count = self._db.execute("SELECT count(*) FROM Types").fetchall()[0][0]
        return count

    # function for adding new subtype with its name as argument
    # adding fails, if exact same name already exists in db
    def add_subtype(self, name: str, type_of: int):
        try:
            self._db.execute("""
                INSERT INTO Subtypes (subtype_name, type) VALUES (?,?)
            """, [name, type_of])
            return True
        except:  # pylint: disable=bare-except
            return False

    # function for fetching subtypes from db
    # returns None if no subtypes in db
    def get_subtypes(self):
        subtypes = self._db.execute("""
            SELECT type_name, subtype_name, S.id FROM Subtypes S LEFT JOIN Types T ON S.type=T.id
        """).fetchall()
        return subtypes if len(subtypes) > 0 else None

    # function for fetching number of subtypes in db
    def get_subtypecount(self):
        count = self._db.execute(
            "SELECT count(*) FROM Subtypes").fetchall()[0][0]
        return count

    # function for deleting a subtype from db
    # with its name as argument

    # function for returning db status (???)
