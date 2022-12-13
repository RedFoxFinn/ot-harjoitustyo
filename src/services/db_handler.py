"""
depends on sqlite3 database, import sqlite3 library for python3
additionally depends on re, package to use regular expressions
and datetime for timestamp requiring functionalities
"""

import sqlite3
import datetime

from tools.db_validator import validate_database_path
from tools.db_validator import validate_database_existence


class DatabaseHandler:
    """
    class implementation for Database_handler, class that will handle all interaction with sql-db
    """
    __table_creation = [
        """CREATE TABLE Products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
        "Kasvipohjaiset valmisteet",
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

    def __fetch_typeid(self, typename: str):
        return self._db.execute("SELECT id FROM Types WHERE type_name=?", [typename]).fetchone()

    def __init__(self, db_set: bool, database: str):  # pylint: disable=too-many-statements
        """
        class initialization
        > if db_set is True
        > database contains valid database path
        > path leads to valid file
        >> connect to database file
        > else create new database with automatic table creation
        """
        if db_set and validate_database_path(database) and validate_database_existence(database):
            self._db = sqlite3.connect(database)
        elif not db_set and database is not None and validate_database_path(database):
            self._db = sqlite3.connect(database)
            for item in self.__table_creation:
                try:
                    self._db.execute(item)
                except:  # pylint: disable=bare-except
                    # try: always requires except: even if it would be this simple
                    # therefore I was required to add disable
                    print("table already exists")
            for item in self.__type_creation:
                self.add_type(item)
            __type_id = self.__fetch_typeid("Raaka-aineet")[0]
            for item in self.__subtype_creation:
                self.add_subtype(item, __type_id)
        else:
            self._db = sqlite3.connect("src/services/pantry.db")
            for item in self.__table_creation:
                try:
                    self._db.execute(item)
                except:  # pylint: disable=bare-except
                    # try: always requires except: even if it would be this simple
                    # therefore I was required to add disable
                    print("table already exists")
            for item in self.__type_creation:
                self.add_type(item)
            __type_id = self.__fetch_typeid("Raaka-aineet")[0]
            for item in self.__subtype_creation:
                self.add_subtype(item, __type_id)
        self._db.isolation_level = None

    def add_product(self,
                    name: str,
                    type_of: int,
                    storage_life: int,
                    subtype: int = 0,
                    count: int = 1):
        """
        function for adding new product with its name,
        type, subtype and storage_life as arguments
        name (string), type (int) and storage_life (int) needed,
        subtype (int) optional, count (int) optional
        """
        product = self._db.execute("""
            SELECT P.id, P.number_of FROM Products P WHERE P.name=? AND P.type=? AND P.subtype=? AND P.storage_life=?
        """, [name, type_of, subtype, storage_life]).fetchone()
        try:
            if product is not None:
                self._db.execute("""
                    UPDATE Products SET number_of=? WHERE id=?
                """, [product[1]+count, product[0]])
            else:
                self._db.execute("""
                    INSERT INTO Products (
                        name,
                        type,
                        subtype,
                        storage_life,
                        number_of
                    ) VALUES (?,?,?,?,?)
                """, [name, type_of, subtype, storage_life, count])
            return True
        except:  # pylint: disable=bare-except
            # try: always requires except: even if it would be this simple
            # therefore I was required to add disable
            return False

    def get_products(self):
        """
        function for fetching products from db
        returns None if no product in db
        joins Product with Type and conditionally joins with Subtype
        if Product.subtype has value greater than 0
        """
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
                                    ON R.sid AND R.sid=S.id ORDER BY R.storage_life ASC, R.pname ASC
        """).fetchall()
        print(products)
        return products if len(products) > 0 else None

    def _get_default_exp(self):
        _date = datetime.date.today()+datetime.timedelta(days=2)
        return datetime.datetime(_date.year, _date.month, _date.day).timestamp()

    def get_products_by_storage_life(
            self,
            expiring: bool = True,
            exp: int = _get_default_exp):
        """
        function for fetching expiring or expired products
        """
        products = None
        today = datetime.date.today()
        current = datetime.datetime(
            today.year, today.month, today.day).timestamp()
        products = self._db.execute("""
            SELECT number_of FROM Products WHERE storage_life BETWEEN ? AND ? ORDER BY storage_life ASC, name ASC
        """, [current, exp]).fetchall() if expiring else self._db.execute("""
            SELECT number_of FROM Products WHERE storage_life < ? ORDER BY storage_life ASC, name ASC
        """, [exp]).fetchall()
        return products

    def get_productcount(self, product_type: int = None, distinct: bool = True):
        """
        function for fetching number of products in db
        """
        count = 0
        if distinct:
            if product_type is None:
                count += self._db.execute(
                    "SELECT count(*) FROM Products"
                ).fetchall()[0][0]
            else:
                count += self._db.execute(
                    "SELECT count(*) FROM Products WHERE type=?", [
                        product_type]
                ).fetchall()[0][0]
            return count

        if product_type is not None:
            products = self._db.execute(
                "SELECT number_of FROM Products WHERE type=?", [
                    product_type]
            ).fetchall()
            for p_x in products:
                print(p_x[0])
                count += p_x[0]
        if product_type is None:
            products = self._db.execute(
                "SELECT number_of FROM Products"
            ).fetchall()
            for p_x in products:
                print(p_x[0])
                count += p_x[0]
        print(count)
        return count

    def remove_product(self, product_id: int):
        """
        function for removing product from db
        """
        try:
            self._db.execute("DELETE FROM Products WHERE id=?", [product_id])
            return True
        except:  # pylint: disable=bare-except
            # try: always requires except: even if it would be this simple
            # therefore I was required to add disable
            return False

    def update_count(self, product_id: int, change: int = 1, subtract: bool = True):
        """
        function for updating number of products with certain id
        """
        _product = self._db.execute("""
            SELECT id, number_of FROM Products WHERE id=?
        """, [product_id]).fetchone()
        if _product is not None and subtract and _product[1]-change == 0:
            return self.remove_product(product_id)
        if _product is not None and subtract:
            try:
                self._db.execute("""
                    UPDATE Products SET number_of=number_of-? WHERE id=?
                """, [change, product_id])
                return True
            except:  # pylint: disable=bare-except
                # try: always requires except: even if it would be this simple
                # therefore I was required to add disable
                return False
        else:
            try:
                self._db.execute("""
                    UPDATE Products SET number_of=number_of+? WHERE id=?
                """, [change, product_id])
                return True
            except:  # pylint: disable=bare-except
                # try: always requires except: even if it would be this simple
                # therefore I was required to add disable
                return False

    def add_type(self, name: str):
        """
        function for adding new type with its name as argument
        optional argument subtype (integer which is the id of subtype)
        """
        try:
            self._db.execute(
                "INSERT INTO Types (type_name) VALUES (?)", [name])
            return True
        except:  # pylint: disable=bare-except
            # try: always requires except: even if it would be this simple
            # therefore I was required to add disable
            return False

    def get_types(self):
        """
        function for fetching types from db
        returns None if no types in db
        """
        types = self._db.execute("SELECT type_name, id FROM Types").fetchall()
        return types if len(types) > 0 else None

    def get_typecount(self):
        """
        function for fetching number of types in db
        """
        count = self._db.execute("SELECT count(*) FROM Types").fetchall()[0][0]
        return count

    def add_subtype(self, name: str, type_of: int):
        """
        function for adding new subtype with its name as argument
        adding fails, if exact same name already exists in db
        """
        try:
            self._db.execute("""
                INSERT INTO Subtypes (subtype_name, type) VALUES (?,?)
            """, [name, type_of])
            return True
        except:  # pylint: disable=bare-except
            # try: always requires except: even if it would be this simple
            # therefore I was required to add disable
            return False

    def get_subtypes(self):
        """
        function for fetching subtypes from db
        returns None if no subtypes in db
        """
        subtypes = self._db.execute("""
            SELECT type_name, subtype_name, S.id FROM Subtypes S LEFT JOIN Types T ON S.type=T.id
        """).fetchall()
        return subtypes if len(subtypes) > 0 else None

    def get_subtypecount(self):
        """
        function for fetching number of subtypes in db
        """
        count = self._db.execute(
            "SELECT count(*) FROM Subtypes").fetchall()[0][0]
        return count
