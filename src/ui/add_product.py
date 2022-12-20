# depends on tkinter, tkcalendar, re (regex) and datetime

import tkinter as tk
from tkinter import ttk, messagebox, constants
from tkcalendar import DateEntry

from tools.date_tools import get_current_date
from tools.date_tools import get_exp_timestamp
from tools.regex_validators import selector_type_validation_for_ingredient
from tools.builders import build_id_from_selector_number

_type_default = [f"{0:02d} - valitse tyyppi"]
_subtype_default = [f"{0:02d} - valitse alatyyppi"]


class AddProduct:
    """
    Luokka, jonka vastuulla on esittää lisäysnäkymä ja suorittaa
    talletettavien tietojen tallettamiseksi DatabaseHandlerin kutsun
    """

    def __init__(self, root, middleware, to_stats, to_list):
        """
        Luokan konstruktorifunktio, joka luo lisäysnäkymän

        Args:
            root: sovelluksen ikkuna
            dbh: DatabaseHandler, jota sovellus käyttää
            to_stats: funktio, jolla voidaan siirtyä
              tilastointinäkymään
            to_list: funktio, jolla voidaan siirtyä
              listausnäkymään
        """
        self._root = root
        self._name = None
        self._type = None
        self._subtype = None
        self._storage_life = None
        self._number_of = None
        self._frame = None
        self._middleware = middleware
        self._back_to_stats = to_stats
        self._go_to_list = to_list
        self._clicked_type = tk.StringVar(self._root)
        self._clicked_subtype = tk.StringVar(self._root)
        self._initialize()

    __texts = [
        "Tuotteen lisäys",
        "Lisää tuote",
        "Tuote",
        "Tyyppi",
        "Säilyvyys",
        "Lukumäärä",
        "Alatyyppi"
    ]

    def _click_product(self):
        """
        Luokan työkalufunktio, joka on vastuussa DatabaseHandlerin
        kutsumisesta tuoterivin lisäämiseksi sovelluksen tietokantaan
        """
        success = False
        _name = self._name.get()
        _type = self._clicked_type.get()
        _storage_life = self._storage_life.get_date()
        _number_of = int(self._number_of.get())
        _subtype = "00"
        if self._subtype != None and bool(self._subtype.grid_info()):
            _subtype = self._clicked_subtype.get()
        else:
            _subtype = "00"

        if len(_name) > 0 and not _type.find('00') > -1 and _number_of > 0:
            success = self._middleware.add_product(
            pname=_name, ptype=build_id_from_selector_number(_type[:2]), pexp=get_exp_timestamp(
                _storage_life.year, _storage_life.month, _storage_life.day),
            psubtype=build_id_from_selector_number(_subtype[:2]), pcount=_number_of)
        else:
            messagebox.showwarning("Lisäys", f"{_name} lisäys ei onnistunut. Tarkista syötteesi oikeellisuus.")

        if success:
            self._name.delete(0, 'end')
            self._number_of.delete(0, 'end')
            self._clicked_type.set(_type_default[0])
            messagebox.showinfo("Lisäys", f"{_name} lisäys onnistui!")

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

    def _initialize(self):
        _current_date = get_current_date(as_object=True)

        def _types():
            types_in_db = self._middleware.get_types_for_selector()
            self._clicked_type.set(types_in_db[0])
            return ttk.OptionMenu(self._frame, self._clicked_type, *types_in_db)

        def _subtypes(*args):
            _subtypes_in_db = self._middleware.get_subtypes_for_selector()
            if selector_type_validation_for_ingredient(self._clicked_type.get()):
                self._clicked_subtype.set(_subtypes_in_db[0])
                self._subtype = ttk.OptionMenu(
                    self._frame, self._clicked_subtype, *_subtypes_in_db)
                subtype_label.grid(row=5, column=0, padx=4, pady=4)
                self._subtype.grid(row=5, column=1, padx=4,
                                   pady=4, sticky=(constants.E, constants.W))
            else:
                subtype_label.grid_remove()
                self._subtype.grid_remove()

        self._frame = ttk.Frame(master=self._root)
        self._clicked_type.trace_add("write", _subtypes)
        label = ttk.Label(master=self._frame, text=self.__texts[0])
        back_to_stats = ttk.Button(
            self._frame, command=self._back_to_stats, text=" < Tilastointi")
        list_all = ttk.Button(
            self._frame, command=self._go_to_list, text="Näytä tuotteet > ")
        button = ttk.Button(master=self._frame,
                            text=self.__texts[1], command=self._click_product)
        self._name = ttk.Entry(master=self._frame)
        name_label = ttk.Label(master=self._frame, text=self.__texts[2])
        self._type = _types()
        type_label = ttk.Label(master=self._frame, text=self.__texts[3])
        self._storage_life = DateEntry(
            self._frame,
            selectmode="day",
            year=_current_date.year,
            month=_current_date.month,
            day=_current_date.day,
        )
        storage_life_label = ttk.Label(
            master=self._frame, text=self.__texts[4])
        self._number_of = ttk.Spinbox(self._frame, from_=1, to_=64)
        number_of_label = ttk.Label(master=self._frame, text=self.__texts[5])
        subtype_label = ttk.Label(master=self._frame, text=self.__texts[6])

        label.grid(row=0, column=1, columnspan=2, padx=8, pady=8)
        back_to_stats.grid(row=0, column=0, padx=8, pady=8)
        list_all.grid(row=0, column=2, padx=8, pady=8)
        name_label.grid(row=1, column=0, padx=4, pady=12)
        self._name.grid(row=1, column=1, padx=4, pady=12,
                        sticky=(constants.E, constants.W))
        type_label.grid(row=2, column=0, padx=4, pady=12)
        self._type.grid(row=2, column=1, padx=4, pady=12,
                        sticky=(constants.E, constants.W))
        storage_life_label.grid(row=3, column=0, padx=4, pady=12)
        self._storage_life.grid(row=3, column=1, padx=12,
                                pady=4, sticky=(constants.E, constants.W))
        number_of_label.grid(row=4, column=0, padx=4, pady=12)
        self._number_of.grid(row=4, column=1, padx=4, pady=12,
                             sticky=(constants.E, constants.W))
        button.grid(row=6, column=1, padx=4, pady=12)
        self._frame.columnconfigure(1, weight=1, minsize=320)
