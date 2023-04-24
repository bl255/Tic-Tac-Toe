"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie
author: Martina Vasiľová
email:
discord:
poznámka: Jak jsem psala v chate na lekci, zkusila jsem zadání vypracovat s GUI.
"""

from tkinter import Tk, Canvas
from tic_tac_toe_main_class import TicTacToe

from settings_gui import main_background, main_canvas_height, main_canvas_width, pad

window = Tk()
window.minsize(main_canvas_width + 2 * pad, main_canvas_height + 2 * pad)
window.title("Tic-Tac-Toe")
window.iconbitmap("images/ico2.ico")
window.configure(bg=main_background)

main_canvas = Canvas(window, width=main_canvas_width, height=main_canvas_height)
main_canvas.pack(padx=pad, pady=pad)
tictactoe = TicTacToe(main_canvas)

window.mainloop()
