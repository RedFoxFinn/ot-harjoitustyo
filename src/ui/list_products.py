# depends on tkinter and datetime

import tkinter as tk
from tkinter import ttk, messagebox, constants
import datetime

sorting_orders = [
    'expiring first',
    'alphabetically'
]


class ListProducts:
    def __init__(self, root, dbh, to_stats, to_add):
        self._root = root
        self._db = dbh
        self._back_to_stats = to_stats
        self._go_to_add = to_add
        self._frame = None
        self._update()

    def _update(self):
        self._current_date = datetime.date.today()
        self._products = self._db.get_products()
        self._sort = sorting_orders[0]
        self._frame = ttk.Frame(master=self._root)
        self._label = ttk.Label(master=self._frame, text="Listaus")
        self._back_to_stats_button = ttk.Button(
            self._frame, command=self._back_to_stats, text=" < Tilastointi")
        self._add_new = ttk.Button(
            self._frame, command=self._go_to_add, text="Lisää tuote > ")
        self._label.grid(row=0, column=1, columnspan=2, padx=8, pady=8)
        self._back_to_stats_button.grid(row=0, column=0, padx=8, pady=8)
        self._add_new.grid(row=0, column=2, padx=8, pady=8)
        self._frame.columnconfigure(1, weight=1, minsize=320)

    def destroy(self):
        self._frame.destroy()

    def pack(self):
        self._frame.pack(fill=constants.X)
