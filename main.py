import db
import tkinter as tk
from ui import CatalogoUI

db.criar_tabela()

root = tk.Tk()
app = CatalogoUI(root)
root.mainloop()
