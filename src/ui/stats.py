
from tkinter import Tk, ttk, constants
import datetime


class Stats:
    def __init__(self, root, dbh, to_add):
        self._root = root
        self._db = dbh
        self._go_to_add = to_add
        self._initialize()

    def destroy(self):
        self._frame.destroy()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def update(self):
        self._current_date = datetime.date.today()
        self._exp_soon_date = self._current_date + datetime.timedelta(days=2)
        _types = self._db.get_types()
        _number_of_products = self._db.get_productcount()
        _numbers_by_types = []
        for t in _types:
            count = self._db.get_productcount(
                product_type=t[1], distinct=False)
            _numbers_by_types.append((t[1], t[0], count))
        _expiring_products = self._db.get_products_by_storage_life(
            expired=False,
            expiring=True,
            exp=datetime.datetime(
                self._exp_soon_date.year,
                self._exp_soon_date.month,
                self._exp_soon_date.day).timestamp())
        _expiring_products_total = 0
        for e in _expiring_products:
            _expiring_products_total += e[0]
        _expired_products = self._db.get_products_by_storage_life(
            expired=True,
            expiring=False,
            exp=datetime.datetime(
                self._current_date.year,
                self._current_date.month,
                self._current_date.day).timestamp())
        _expired_products_total = 0
        for e in _expired_products:
            _expired_products_total += e[0]

        self._frame = ttk.Frame(master=self._root)
        label = ttk.Label(master=self._frame, text="Stats")
        add_new = ttk.Button(
            self._frame, command=self._go_to_add, text="Lisää tuote")
        _products_lf = ttk.LabelFrame(self._frame, text="Tuotteita")
        _types_lf = ttk.LabelFrame(self._frame, text="Tuotteet tyypeittäin")
        _expiring_lf = ttk.LabelFrame(self._frame, text="Pian vanhenevat tuotteet")
        _expired_lf = ttk.LabelFrame(self._frame, text="Vanhentuneet tuotteet")
        _products_label = ttk.Label(
            _products_lf, text="Tuoterivejä talletettuna %g" % _number_of_products)
        _type1_label = ttk.Label(
            _types_lf, text=f"Tyyppiä {_numbers_by_types[0][1]} tallennettuna yhteensä {_numbers_by_types[0][2]} kappaletta")
        _type2_label = ttk.Label(
            _types_lf, text=f"Tyyppiä {_numbers_by_types[1][1]} tallennettuna yhteensä {_numbers_by_types[1][2]} kappaletta")
        _type3_label = ttk.Label(
            _types_lf, text=f"Tyyppiä {_numbers_by_types[2][1]} tallennettuna yhteensä {_numbers_by_types[2][2]} kappaletta")
        _exp_soon_rows_label = ttk.Label(
            _expiring_lf, text=f"2 päivän sisään vanhenevia tuoterivejä: {len(_expiring_products)}")
        _exp_soon_total_label = ttk.Label(
            _expiring_lf, text=f"2 päivän sisään vanhenevia tuotteita yhteensä: {_expiring_products_total}")
        _expd_rows_label = ttk.Label(
            _expired_lf, text=f"Vanhentuneita tuotteita {len(_expired_products)} riviä")
        _expd_total_label = ttk.Label(
            _expired_lf, text=f"Yhteensä vanhentuneita tuotteita {_expired_products_total} kappaletta")

        add_new.grid(row=0, column=0, padx=8, pady=8)
        label.grid(row=0, column=1, padx=8, pady=8)
        _products_lf.grid(row=1, column=1, padx=4, pady=12)
        _products_label.grid(row=2, column=1, padx=4, pady=4)
        _types_lf.grid(row=3, column=1, padx=4, pady=12)
        _type1_label.grid(row=4, column=1, padx=4, pady=4)
        _type2_label.grid(row=5, column=1, padx=4, pady=4)
        _type3_label.grid(row=6, column=1, padx=4, pady=4)
        _expiring_lf.grid(row=7, column=1, padx=4, pady=12)
        _exp_soon_rows_label.grid(row=8, column=1, padx=4, pady=4)
        _exp_soon_total_label.grid(row=9, column=1, padx=4, pady=4)
        _expired_lf.grid(row=10, column=1, padx=4, pady=12)
        _expd_rows_label.grid(row=11, column=1, padx=4, pady=4)
        _expd_total_label.grid(row=12, column=1, padx=4, pady=4)
        self._frame.columnconfigure(1, weight=1, minsize=320)

    def _initialize(self):
        self.update()
