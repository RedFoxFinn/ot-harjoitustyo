
from tools.builders import build_elements_for_selector


class Middleware:
    """
    implementation for class Middleware, which acts as middleware between UI and DatabaseHandler

    Args (init function):
      root: application root, the window
      dbh: DatabaseHandler created in application startup
    """

    def __init__(self, dbh):
        self._db = dbh

    def get_types(self):
        resp = self._db.get_types()
        return resp

    def get_numbers_by_types(self):
        types = self._db.get_types()
        numbers_by_types = []
        for typ in types:
            count = self._db.get_productcount(
                product_type=typ[1], distinct=False)
            numbers_by_types.append((typ[1], typ[0], count))
        return numbers_by_types

    def get_products(self):
        products = self._db.get_products()
        return products

    def get_product_count(self):
        count = self._db.get_productcount()
        return count

    def get_expiring_products(self, timestamp):
        products = self._db.get_products_by_storage_life(
            expiring=True, exp=timestamp)
        return products

    def get_expiring_products_count(self, timestamp):
        products = self.get_expiring_products(timestamp)
        count = 0
        for prod in products:
            count += prod[0]
        return count

    def get_expired_products(self, timestamp):
        products = self._db.get_products_by_storage_life(
            expiring=False, exp=timestamp)
        return products

    def get_expired_products_count(self, timestamp):
        products = self.get_expired_products(timestamp)
        count = 0
        for prod in products:
            count += prod[0]
        return count

    def get_types_for_selector(self):
        types = build_elements_for_selector(
            list_of=self._db.get_types(), for_type=True)
        return types

    def get_subtypes_for_selector(self):
        subtypes = build_elements_for_selector(
            list_of=self._db.get_subtypes(), for_type=False)
        return subtypes

    def add_product(self, pname: str, ptype: int, pexp: int, psubtype: int = 0, pcount: int = 1):
        result = self._db.add_product(
            name=pname,
            type_of=ptype,
            storage_life=pexp,
            subtype=psubtype,
            count=pcount
        )
        return result

    def update_product(
            self,
            pid: int,
            remove: bool = False,
            change: int = 1,
            subtract: bool = True):
        result = None

        if remove:
            result = self._db.remove_product(product_id=pid)
        if not remove:
            result = self._db.update_count(
                product_id=pid, change=change, subtract=subtract)
        return result
