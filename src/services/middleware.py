
from tools.builders import build_elements_for_selector

class Middleware:
    """
    implementation for class Middleware, which acts as middleware between UI and DatabaseHandler
    
    Args (init function):
      root: application root, the window
      dbh: DatabaseHandler created in application startup
    """
    def __init__(self, root, dbh):
        self.root = root
        self._db = dbh

    def get_types(self):
        resp = self._db.get_types()
        return resp

    def get_numbers_by_types(self):
        types = self._db.get_types()
        numbers_by_types = []
        for t in types:
            count = self._db.get_productcount(
                product_type=t[1], distinct=False)
            numbers_by_types.append((t[1], t[0], count))
        return numbers_by_types

    def get_products(self):
        products = self._db.get_products()
        return products

    def get_product_count(self):
        count = self._db.get_productcount()
        return count

    def get_expiring_products(self, timestamp):
        products = self._db.get_products_by_storage_life(expiring=True, exp=timestamp)
        return products

    def get_expiring_products_count(self, timestamp):
        products = self.get_expiring_products(timestamp)
        count = 0
        for prod in products:
            count += prod[0]
        return count

    def get_expired_products(self, timestamp):
        products = self._db.get_products_by_storage_life(expiring=False, exp=timestamp)
        return products

    def get_expired_products_count(self, timestamp):
        products = self.get_expired_products(timestamp)
        count = 0
        for prod in products:
            count += prod[0]
        return count

    def get_types_for_selector(self):
        types = build_elements_for_selector(list_of=self._db.get_types(), for_type=True)
        return types

    def get_subtypes_for_selector(self):
        subtypes = build_elements_for_selector(list_of=self._db.get_subtypes(), for_type=False)
        return subtypes

    def add_product(self, pname, ptype, pexp, psubtype, pcount):
        res = self._db.add_product(
            name=pname,
            type_of=ptype,
            storage_life=pexp,
            subtype=psubtype,
            count=pcount
        )
        return res

    def update_product(self, id:int, remove:bool=False, change:int=1, subtract:bool=True):
        result = False

        if remove:
            result = self._db.remove_product(product_id=id)
        if not remove:
            result = self._db.update_count(
                product_id=id, change=change, subtract=subtract)
        if result:
            self._products = self._db.get_products()
        return result