# depends on tkinter for UI creation, import tkinter library for python3
# additionally imports db_handler from projects database-directory

from tkinter import Tk

from services.db_handler import DatabaseHandler
from ui.add_product import AddProduct
from ui.stats import Stats
from ui.list_products import ListProducts
from services.middleware import Middleware

class PantryUI:
    """
    Luokka, jonka vastuulla on sovelluksen suorittaminen,
    sovelluksen tietokannan yhdistäminen sekä
    käyttöliittymän osien välillä siirtyminen ja
    yhdistetyn tietokannan näille tarjoaminen
    """

    """
    class initialization
    connect or create database
    """
    def __init__(self, root, db_path):
        """
        Luokan konstruktorifunktio, joka luo sovelluksen käyttöliittymän
        ja yhdistää tietokantatiedostoon

        Args:
            root: sovelluksen ikkuna
            db_path: käytettävän tietokantatiedoston polku
        """
        self._root = root
        self._current_view = None
        self._dbh = DatabaseHandler(True, db_path)
        self._middleware = Middleware(root, self._dbh)

    # start Pantry application
    def start(self):
        """
        Luokan funktio, joka käynnistää käyttöliittymän suorituksen
        Oletuksena aloitetaan tilastointinäkymässä
        """
        self._show_stats()

    def _handle_add_product(self):
        """
        Luokan funktio, joka vaihtaa esitettävän näkymän
        vaihdetaan lisäysnäkymään
        """
        self._hide_current_view()
        self._show_add_product()

    def _handle_stats(self):
        """
        Luokan funktio, joka vaihtaa esitettävän näkymän
        vaihdetaan tilastointinäkymään
        """
        self._hide_current_view()
        self._show_stats()

    def _handle_list_products(self):
        """
        Luokan funktio, joka vaihtaa esitettävän näkymän
        vaihdetaan listausnäkymään
        """
        self._hide_current_view()
        self._show_list_products()

    def _hide_current_view(self):
        """
        Luokan funktio, joka poistaa nykyisen näkymän
        """
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_add_product(self):
        """
        Luokan funktio, jonka vastuulla on alustaa näytettävän
        näkymän käyttöliittymäluokka - lisäysnäkymä
        """
        self._current_view = AddProduct(
            self._root, self._middleware, to_stats=self._handle_stats,
            to_list=self._handle_list_products)
        self._current_view.pack()

    def _show_stats(self):
        """
        Luokan funktio, jonka vastuulla on alustaa näytettävän
        näkymän käyttöliittymäluokka - tilastointinäkymä
        """
        self._current_view = Stats(
            self._root, self._middleware, to_add=self._handle_add_product,
            to_list=self._handle_list_products)
        self._current_view.pack()

    def _show_list_products(self):
        """
        Luokan funktio, jonka vastuulla on alustaa näytettävän
        näkymän käyttöliittymäluokka - listausnäkymä
        """
        self._current_view = ListProducts(
            self._root, self._middleware, to_stats=self._handle_stats,
            to_add=self._handle_add_product, refresh=self._handle_list_products)
        self._current_view.pack()


window = Tk()
window.title("Pantry")
window.geometry("1024x800")

ui = PantryUI(window, "src/services/pantry.db")
ui.start()

window.mainloop()
