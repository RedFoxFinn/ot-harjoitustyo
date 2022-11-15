
from tkinter import Tk, ttk, messagebox, constants

class AddProduct:
  def __init__(self, root, dbh):
    self._root = root
    self._name = None
    self._type = None
    self._subtype = None
    self._storage_life = None
    self._number_of = None
    self._frame = None
    self._db = dbh
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
    value0 = self._name.get()
    value1 = self._type.get()
    value2 = self._storage_life.get()
    value3 = self._subtype.get()
    value4 = self._number_of.get()
    
    success = False
    if len(value0) > 0 and len(value1) > 0 and len(value2) > 0:
      if len(value3) > 0 and len(value4) > 0:
        success = self._db.add_product(value0,value1,value2,subtype=value3,count=value4)
      elif len(value3) > 0:
        success = self._db.add_product(value0,value1,value2,subtype=value3)
      elif len(value4) > 0:
        success = self._db.add_product(value0,value1,value2,count=value4)
      else:
        success = self._db.add_product(value0,value1,value2)
    if success:
      self._name.delete(0,'end')
      self._type.delete(0,'end')
      self._storage_life.delete(0,'end')
      self._subtype.delete(0,'end')
      self._number_of.delete(0,'end')
      messagebox.showinfo("Lisäys", f"{value0} lisäys onnistui!")
  
  def destroy(self):
    self._frame.destroy()

  def pack(self):
    self._frame.pack(fill=constants.X)

  def _initialize(self):
    self._frame = ttk.Frame(master=self._root)
    label = ttk.Label(master = self._frame, text = self.__texts[0])
    button = ttk.Button(master = self._frame, text = self.__texts[1], command=self._click_product)
    self._name = ttk.Entry(master=self._frame)
    name_label = ttk.Label(master=self._frame, text=self.__texts[2])
    self._type = ttk.Entry(master = self._frame)
    type_label = ttk.Label(master=self._frame, text=self.__texts[3])
    self._storage_life = ttk.Entry(master=self._frame)
    storage_life_label = ttk.Label(master=self._frame, text=self.__texts[4])
    self._number_of = ttk.Entry(master=self._frame)
    number_of_label = ttk.Label(master=self._frame, text=self.__texts[5])
    self._subtype = ttk.Entry(master=self._frame)
    subtype_label = ttk.Label(master=self._frame, text=self.__texts[6])
    
    label.grid(row = 0, column=0, columnspan=2, padx=4, pady=4)
    name_label.grid(row=1,column=0, padx=4, pady=4)
    self._name.grid(row=1, column=1, padx=4, pady=4)
    type_label.grid(row=2,column=0, padx=4, pady=4)
    self._type.grid(row=2,column=1, padx=4, pady=4)
    storage_life_label.grid(row=3,column=0, padx=4, pady=4)
    self._storage_life.grid(row=3,column=1, padx=4, pady=4)
    number_of_label.grid(row=4,column=0, padx=4, pady=4)
    self._number_of.grid(row=4,column=1, padx=4, pady=4)
    subtype_label.grid(row=5,column=0, padx=4, pady=4)
    self._subtype.grid(row=5,column=1, padx=4, pady=4)
    button.grid(row=6,column=1,padx=4, pady=4)