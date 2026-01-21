import tkinter as tk
import sys
sys.path.insert(0, '.')
from ui.creategui_P230_v2 import Data_P230_Checker_V2

try:
    root = tk.Tk()
    root.geometry('1000x700')
    ui = Data_P230_Checker_V2(root)
    root.update_idletasks()
    print('Stage cards positions (key: row,column)')
    max_col = -1
    for k,c in ui.stage_cards.items():
        gi = c.grid_info()
        r = gi.get('row')
        col = gi.get('column')
        print(f"{k}: {r},{col}")
        if col is not None and col > max_col:
            max_col = col
    print('max column index seen =', max_col)
    root.destroy()
except Exception as e:
    print('ERROR during verification:', e)
    raise
