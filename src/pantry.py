# depends on tkinter for UI creation, import tkinter library for python3
# additionally imports db_handler from projects database-directory

from tkinter import Tk, ttk

from database import db_handler as dbh

# class implementation for the base of Pantry UI

class Pantry_UI:

  # class initialization
  # connect or create database
  def __init__(self, root, db_path):
    self._root = root
    self._entry = None
    self._db = dbh.Database_handler(False, db_path)

  def _click(self):
    entry_value = self._entry.get()
    if len(entry_value) > 0:
      self._db.add_subtype(entry_value)
  
  # start Pantry application
  def start(self, label_text, button_text):
    label = ttk.Label(master = self._root, text = label_text)
    button = ttk.Button(master = self._root, text = button_text, command=self._click)
    self._entry = ttk.Entry(master = self._root)

    label.pack()
    button.pack()
    self._entry.pack()

window = Tk()
window.title("Pantry")

ui = Pantry_UI(window,"src/database/pantry.db")
ui.start("Pantry", "nappi")

window.mainloop()
