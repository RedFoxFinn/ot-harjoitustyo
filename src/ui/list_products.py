"""
depends on tkinter and datetime
"""

import tkinter as tk
from tkinter import ttk, constants
from tools.date_tools import expiration_check
from tools.date_tools import convert_timestamp
from tools.highlights import highlight_expired_label
from tools.regex_validators import selector_type_validation_for_ingredient

filtering = [
    'Kaikki',
    'Juomat',
    'Ruoat',
    'Raaka-aineet'
]


class ListProducts:
    """
    Luokka, jonka vastuulla on esittää sovelluksen tietokantaan
    talletettujen tuotteiden listaus ja listalla olevien tuotteiden
    lukumäärän lisäyksen, vähentämisen ja poistamisen toiminnot
    """

    def __init__(self, root, middleware, to_stats, to_add, refresh):
        """
        Luokan konstruktorifunktio, joka luo tuotelistauksen

        Args:
            root: sovelluksen ikkuna
            dbh: DatabaseHandler, jota sovellus käyttää
            to_stats: funktio, jolla voidaan siirtyä
              tilastointinäkymään
            to_add: funktio, jolla voidaan siirtyä lisäysnäkymään
            refresh: funktio, joka päivittää listausnäkymän
              hyödyntämällä pantry.py:n handle_list_products -funktiota
        """
        self._root = root
        self._middleware = middleware
        self._back_to_stats = to_stats
        self._go_to_add = to_add
        self._refresh = refresh
        self._frame = None
        self._filtering = filtering[0]
        self._update()

    def _update_product(self, pid: int, remove: bool = False, change: int = 1, subtract: bool = True):
        """
        class function for product row changes triggered by add, subtract and remove -buttons

        Args:
            id: int, product id
            remove: bool, is it removal
            change: int, change in number of products on row
            subtract: bool, to subtract or add
        """
        result = self._middleware.update_product(
            pid=pid, remove=remove, change=change, subtract=subtract)

        if result:
            self._refresh()

    def _update(self):
        """
        class function for initializing the product list
        """
        self._products = self._middleware.get_products()
        self._frame = ttk.Frame(master=self._root)
        self._label = ttk.Label(master=self._frame, text="Listaus")
        self._back_to_stats_button = ttk.Button(
            self._frame, command=self._back_to_stats, text=" < Tilastointi")
        self._add_new = ttk.Button(
            self._frame, command=self._go_to_add, text="Lisää tuote > ")
        self._label.grid(row=0, column=1, columnspan=6, padx=8, pady=8)
        self._back_to_stats_button.grid(row=0, column=0, padx=8, pady=8)
        self._add_new.grid(row=0, column=7, padx=8, pady=8)
        if self._products is not None and len(self._products) > 0:
            for index, item in enumerate(self._products):
                highlight = highlight_expired_label(item[2])
                ttk.Label(self._frame, text=f"{item[1]}",
                          foreground=highlight
                          ).grid(row=index+1, column=1, padx=4, pady=4)
                ttk.Label(self._frame, text=f"{item[3]} kpl",
                          foreground=highlight
                          ).grid(row=index+1, column=2, padx=4, pady=4)
                ttk.Label(
                    self._frame,
                    text=f"{convert_timestamp(item[2])}",
                    foreground=highlight
                ).grid(row=index+1, column=3, padx=4, pady=4)
                if selector_type_validation_for_ingredient(item[4]):
                    ttk.Label(self._frame, text=f"{item[6]}").grid(
                        row=index+1, column=4, padx=4, pady=4)
                else:
                    ttk.Label(self._frame, text=f"{item[4]}").grid(
                        row=index+1, column=4, padx=4, pady=4)
                if expiration_check(item[2]):
                    ttk.Button(self._frame, command=lambda: self._update_product(
                        pid=item[0],
                        remove=True),
                        text="Poista").grid(
                            row=index+1, column=7, padx=4, pady=4)
                else:
                    ttk.Button(self._frame, command=lambda: self._update_product(
                        pid=item[0],
                        remove=False,
                        change=1,
                        subtract=True),
                        text="-").grid(
                            row=index+1, column=5, padx=4, pady=4)
                    ttk.Button(self._frame, command=lambda: self._update_product(
                        pid=item[0],
                        remove=False,
                        change=1,
                        subtract=False),
                        text="+").grid(
                            row=index+1, column=6, padx=4, pady=4)
                    ttk.Button(self._frame, command=lambda: self._update_product(
                        pid=item[0],
                        remove=True),
                        text="Poista").grid(
                            row=index+1, column=7, padx=4, pady=4)
        else:
            ttk.Label(self._frame, text="Ei tuotteita :(").grid(
                row=1, column=1, padx=4, pady=4)
        self._frame.columnconfigure((1, 2, 3), weight=1, minsize=80)
        self._frame.columnconfigure(4, weight=1, minsize=92)
        self._frame.columnconfigure((5, 6), weight=1, minsize=36)
        self._frame.columnconfigure(7, weight=1, minsize=80)

    def destroy(self):
        """
        Luokan funktio, joka poistaa luokan ilmentymän käyttöliittymästä
        """
        self._frame.destroy()

    def pack(self):
        """
        Luokan funktio, joka paketoi luokan ilmentymän käyttöliittymässä näytettäväksi
        """
        self._frame.pack(fill=constants.X)
