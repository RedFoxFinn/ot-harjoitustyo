
import tkinter as tk
from tkinter import ttk, messagebox, constants
from tkcalendar import DateEntry
import datetime
import re

class AddProduct:
    _type_default = [f"{0:02d} - valitse tyyppi"]
    _subtype_default = [f"{0:02d} - valitse alatyyppi"]
    def __init__(self, root, dbh):
        self._root = root
        self._name = None
        self._type = None
        self._subtype = None
        self._storage_life = None
        self._number_of = None
        self._frame = None
        self._db = dbh
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
        _name = self._name.get()
        _type = self._clicked_type.get()
        _storage_life = self._storage_life.get_date()
        _number_of = int(self._number_of.get())
        _subtype = 0
        if self._subtype != None and bool(self._subtype.grid_info()):
            _subtype = self._clicked_subtype.get()
        else:
            _subtype = 0
        success = False

        success = self._db.add_product(
            _name, _type,
            datetime.datetime(_storage_life.year,_storage_life.month,_storage_life.day).timestamp(),
            subtype=_subtype, count=_number_of)

        if success:
            self._name.delete(0, 'end')
            self._number_of.delete(0, 'end')
            self._clicked_type.set(self._type_default[0])
            self._clicked_subtype.set(self._subtype_default[0])
            messagebox.showinfo("Lisäys", f"{_name} lisäys onnistui!")

    def destroy(self):
        self._frame.destroy()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def _initialize(self):
        _current_date = datetime.date.today()
        def _types():
            types_in_db = self._type_default + [f"{t[1]:02d} - {t[0]}" for t in self._db.get_types()]
            self._clicked_type.set(types_in_db[0])
            return ttk.OptionMenu(self._frame,self._clicked_type,*types_in_db)
        def _subtypes(*args):
            _subtypes_in_db = self._subtype_default + [f"{s[2]:02d} - {s[1]}" for s in self._db.get_subtypes()]
            if re.search("Raaka-aineet",self._clicked_type.get()):
                self._clicked_subtype.set(_subtypes_in_db[0])
                self._subtype = ttk.OptionMenu(self._frame,self._clicked_subtype,*_subtypes_in_db)
                subtype_label.grid(row=5, column=0, padx=4, pady=4)
                self._subtype.grid(row=5, column=1, padx=4, pady=4, sticky=(constants.E, constants.W))
            else:
                subtype_label.grid_remove()
                self._subtype.grid_remove()

        self._frame = ttk.Frame(master=self._root)
        self._clicked_type.trace("w",_subtypes)
        label = ttk.Label(master=self._frame, text=self.__texts[0])
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
        self._number_of = ttk.Spinbox(self._frame,from_=1,to_=64)
        number_of_label = ttk.Label(master=self._frame, text=self.__texts[5])
        subtype_label = ttk.Label(master=self._frame, text=self.__texts[6])

        label.grid(row=0, column=0, columnspan=2, padx=4, pady=4)
        name_label.grid(row=1, column=0, padx=4, pady=4)
        self._name.grid(row=1, column=1, padx=4, pady=4, sticky=(constants.E, constants.W))
        type_label.grid(row=2, column=0, padx=4, pady=4)
        self._type.grid(row=2, column=1, padx=4, pady=4, sticky=(constants.E, constants.W))
        storage_life_label.grid(row=3, column=0, padx=4, pady=4)
        self._storage_life.grid(row=3, column=1, padx=4, pady=4, sticky=(constants.E, constants.W))
        number_of_label.grid(row=4, column=0, padx=4, pady=4)
        self._number_of.grid(row=4, column=1, padx=4, pady=4, sticky=(constants.E, constants.W))
        button.grid(row=6, column=1, padx=4, pady=4)
        self._frame.columnconfigure(1,weight=1,minsize=320)
