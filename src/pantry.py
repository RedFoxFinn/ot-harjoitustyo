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
    self._db = dbh.Database_handler(True, db_path)
  
  # start Pantry application
  def start(self, label_text, button_text):
    label = ttk.Label(master = self._root, text = label_text)
    button = ttk.Button(master = self._root, text = button_text)
    entry = ttk.Entry(master = self._root)

    label.pack()
    button.pack()
    entry.pack()

window = Tk()
window.title("Pantry")

ui = Pantry_UI(window,"src/database/pantry.db")
ui.start("Pantry", "nappi")

window.mainloop()
