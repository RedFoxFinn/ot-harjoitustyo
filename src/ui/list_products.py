# depends on tkinter and datetime

import tkinter as tk
from tkinter import ttk, messagebox, constants
import datetime

filtering = [
    'Kaikki',
    'Juomat',
    'Ruoat',
    'Raaka-aineet'
]


class ListProducts:
    def __init__(self, root, dbh, to_stats, to_add, refresh):
        self._root = root
        self._db = dbh
        self._back_to_stats = to_stats
        self._go_to_add = to_add
        self._refresh = refresh
        self._frame = None
        self._filtering = filtering[0]
        self._update()

    def _expiration_check(self, checkup):
        _current_timestamp = datetime.datetime(
            self._current_date.year,
            self._current_date.month,
            self._current_date.day).timestamp()
        if _current_timestamp > checkup:
            return True
        return False

    def _expiration_soon_check(self, checkup):
        _exp_soon_date = self._current_date + datetime.timedelta(days=2)
        _exp_soon_timestamp = datetime.datetime(
            _exp_soon_date.year,
            _exp_soon_date.month,
            _exp_soon_date.day).timestamp()
        if checkup < _exp_soon_timestamp:
            return True
        return False

    def _filter_all(self):
        self._filtering = filtering[0]

    def _filter_drinks(self):
        self._filtering = filtering[1]

    def _filter_foods(self):
        self._filtering = filtering[2]

    def _filter_ingredients(self):
        self._filtering = filtering[3]

    def _highlight_expired_label(self, checkup):
        expired = self._expiration_check(checkup)
        expires_soon = self._expiration_soon_check(checkup)
        if expired:
            return "red"
        if not expired and expires_soon:
            return "orange"
        return "black"

    def _update_product(self, id:int, remove:bool=False, change:int=1, subtract:bool=True):
        result = False
        
        if remove:
            result = self._db.remove_product(product_id=id)
        if not remove:
            result = self._db.update_count(product_id=id, change=change, subtract=subtract)
        if result:
            self._products = self._db.get_products()
            self._refresh()

    def _update(self):
        self._current_date = datetime.date.today()
        self._products = self._db.get_products()
        if self._products is not None and len(self._products) > 0:
            self._drinks = list(
                filter(lambda product: product[4] == filtering[1], self._products))
            self._foods = list(
                filter(lambda product: product[4] == filtering[2], self._products))
            self._ingredients = list(
                filter(lambda product: product[4] == filtering[3], self._products))
        self._frame = ttk.Frame(master=self._root)
        _filter_all = ttk.Button(
            self._frame, command=self._filter_all, text=filtering[0])
        _filter_drinks = ttk.Button(
            self._frame, command=self._filter_drinks, text=filtering[1])
        _filter_foods = ttk.Button(
            self._frame, command=self._filter_foods, text=filtering[2])
        _filter_ingredients = ttk.Button(
            self._frame, command=self._filter_ingredients, text=filtering[3])
        self._label = ttk.Label(master=self._frame, text="Listaus")
        self._back_to_stats_button = ttk.Button(
            self._frame, command=self._back_to_stats, text=" < Tilastointi")
        self._add_new = ttk.Button(
            self._frame, command=self._go_to_add, text="Lisää tuote > ")
        self._label.grid(row=0, column=1, columnspan=4, padx=8, pady=8)
        self._back_to_stats_button.grid(row=0, column=0, padx=8, pady=8)
        self._add_new.grid(row=0, column=5, padx=8, pady=8)
        _filter_all.grid(row=1, column=1, padx=4, pady=8)
        _filter_drinks.grid(row=1, column=2, padx=4, pady=8)
        _filter_foods.grid(row=1, column=3, padx=4, pady=8)
        _filter_ingredients.grid(row=1, column=4, padx=4, pady=8)
        if self._products is not None and len(self._products) > 0:
            for index, item in enumerate(self._products):
                ttk.Label(self._frame, text=f"{item[1]}",
                          foreground=self._highlight_expired_label(item[2])
                          ).grid(row=index+2, column=1, padx=4, pady=4)
                ttk.Label(self._frame, text=f"{item[3]} kpl",
                          foreground=self._highlight_expired_label(item[2])
                          ).grid(row=index+2, column=2, padx=4, pady=4)
                ttk.Label(
                    self._frame,
                    text=f"{datetime.date.fromtimestamp(item[2])}",
                    foreground=self._highlight_expired_label(item[2])
                ).grid(row=index+2, column=3, padx=4, pady=4)
                if item[4] == "Raaka-aineet":
                    ttk.Label(self._frame, text=f"{item[6]}").grid(
                        row=index+2, column=4, padx=4, pady=4)
                else:
                    ttk.Label(self._frame, text=f"{item[4]}").grid(
                        row=index+2, column=4, padx=4, pady=4)
                if self._expiration_check(item[2]):
                    ttk.Button(self._frame, command=lambda: self._update_product(
                        id=item[0],
                        remove=True),
                        text="Poista").grid(
                            row=index+2, column=5, padx=4, pady=4)
                else:
                    ttk.Button(self._frame, command=lambda: self._update_product(
                        id=item[0],
                        remove=False,
                        change=1,
                        subtract=True),
                        text="-").grid(
                            row=index+2, column=5, padx=4, pady=4)
                    ttk.Button(self._frame, command=lambda: self._update_product(
                        id=item[0],
                        remove=False,
                        change=1,
                        subtract=False),
                        text="+").grid(
                            row=index+2, column=6, padx=4, pady=4)
                    ttk.Button(self._frame, command=lambda: self._update_product(
                        id=item[0],
                        remove=True),
                        text="Poista").grid(
                            row=index+2, column=7, padx=4, pady=4)
        else:
            ttk.Label(self._frame, text="Ei tuotteita :(").grid(
                row=2, column=1, padx=4, pady=4)
        self._frame.columnconfigure((1, 2, 3, 4), weight=1, minsize=64)

    def destroy(self):
        self._frame.destroy()

    def pack(self):
        self._frame.pack(fill=constants.X)
