# depends on tkinter for UI creation, import tkinter library for python3
# additionally imports db_handler from projects database-directory

from tkinter import Tk

from services.db_handler import DatabaseHandler
from ui.add_product import AddProduct
from ui.stats import Stats
from ui.list_products import ListProducts

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
        self._show_stats()

    def _handle_add_product(self):
        self._hide_current_view()
        self._show_add_product()

    def _handle_stats(self):
        self._hide_current_view()
        self._show_stats()

    def _handle_list_products(self):
        self._hide_current_view()
        self._show_list_products()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_add_product(self):
        self._current_view = AddProduct(
            self._root, self._dbh, to_stats=self._handle_stats,
            to_list=self._handle_list_products)
        self._current_view.pack()

    def _show_stats(self):
        self._current_view = Stats(
            self._root, self._dbh, to_add=self._handle_add_product,
            to_list=self._handle_list_products)
        self._current_view.pack()

    def _show_list_products(self):
        self._current_view = ListProducts(
            self._root, self._dbh, to_stats=self._handle_stats,
            to_add=self._handle_add_product, refresh=self._handle_list_products)
        self._current_view.pack()


window = Tk()
window.title("Pantry")
window.geometry("800x600")

ui = PantryUI(window, "src/services/pantry.db")
ui.start()

window.mainloop()
