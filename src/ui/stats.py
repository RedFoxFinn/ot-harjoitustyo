
from tkinter import Tk, ttk, constants
import datetime


class Stats:
    def __init__(self, root, dbh, to_add):
        self._root = root
        self._db = dbhdatabase
        self._go_to_add = to_add
        self._initialize()

    def destroy(self):
        self._frame.destroy()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def update(self):
        self._current_date = datetime.date.today()
        _types = self._db.get_types()
        _number_of_products = self._db.get_productcount()
        _numbers_by_types = []
        for t in _types:
            count = self._db.get_productcount(
                product_type=t[1], distinct=False)
            _numbers_by_types.append((t[1], t[0], count))

        self._frame = ttk.Frame(master=self._root)
        label = ttk.Label(master=self._frame, text="Stats")
        add_new = ttk.Button(
            self._frame, command=self._go_to_add, text="Lisää tuote")
        _products_lf = ttk.LabelFrame(self._frame, text="Tuotteita")
        _types_lf = ttk.LabelFrame(self._frame, text="Tuotteet tyypeittäin")
        _products_label = ttk.Label(
            _products_lf, text="Tuoterivejä talletettuna %g" % _number_of_products)
        _type1_label = ttk.Label(
            _types_lf, text=f"Tyyppiä {_numbers_by_types[0][1]} tallennettuna {_numbers_by_types[0][2]}")
        _type2_label = ttk.Label(
            _types_lf, text=f"Tyyppiä {_numbers_by_types[1][1]} tallennettuna {_numbers_by_types[1][2]}")
        _type3_label = ttk.Label(
            _types_lf, text=f"Tyyppiä {_numbers_by_types[2][1]} tallennettuna {_numbers_by_types[2][2]}")

        add_new.grid(row=0, column=0, padx=4, pady=4)
        label.grid(row=0, column=1, padx=4, pady=4)
        _products_lf.grid(row=1, column=1, padx=4, pady=4)
        _products_label.grid(row=2, column=1, padx=4, pady=4)
        _types_lf.grid(row=3, column=1, padx=4, pady=4)
        _type1_label.grid(row=4, column=1, padx=4, pady=4)
        _type2_label.grid(row=5, column=1, padx=4, pady=4)
        _type3_label.grid(row=6, column=1, padx=4, pady=4)
        self._frame.columnconfigure(1, weight=1, minsize=320)

    def _initialize(self):
        self.update()
