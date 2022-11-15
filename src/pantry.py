# depends on tkinter for UI creation, import tkinter library for python3
# additionally imports db_handler from projects database-directory

from tkinter import Tk, ttk

from database.db_handler import Database_handler
from ui.add_product import AddProduct

# class implementation for the base of Pantry UI

class Pantry_UI:

  # class initialization
  # connect or create database
  def __init__(self, root, db_path):
    self._root = root
    self._current_view = None

  # start Pantry application
  def start(self, label_text):
    self._dbh = Database_handler(True, "src/database/pantry_db.db")
    self._show_add_product()
  
  def _show_add_product(self):
    self._current_view = AddProduct(self._root, self._dbh)
    self._current_view.pack()

window = Tk()
window.title("Pantry")

ui = Pantry_UI(window,"src/database/pantry.db")
ui.start("Pantry")

window.mainloop()
