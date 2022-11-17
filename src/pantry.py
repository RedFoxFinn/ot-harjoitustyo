# depends on tkinter for UI creation, import tkinter library for python3
# additionally imports db_handler from projects database-directory

from tkinter import Tk

from database.db_handler import DatabaseHandler
from ui.add_product import AddProduct

# class implementation for the base of Pantry UI

class PantryUI:
    # class initialization
    # connect or create database
    def __init__(self, root, db_path):
        self._root = root
        self._current_view = None
        self._dbh = DatabaseHandler(True, db_path)

    # start Pantry application
    def start(self):
        self._show_add_product()

    def _show_add_product(self):
        self._current_view = AddProduct(self._root, self._dbh)
        self._current_view.pack()

window = Tk()
window.title("Pantry")

ui = PantryUI(window,"src/database/pantry.db")
ui.start()

window.mainloop()
