import tkinter as tk
import sys
sys.path.insert(0, '.')
from ui.creategui_P140_v2 import Data_P140_Checker_V2

root = tk.Tk()
root.geometry('1200x800')
ui = Data_P140_Checker_V2(root)

# Walk widget tree and print summary
def summarize(widget, indent=0):
    try:
        cls = widget.winfo_class()
    except Exception:
        cls = type(widget).__name__
    info = ' ' * indent + f"{widget}: class={cls}, w={widget.winfo_width()}, h={widget.winfo_height()}"
    # if label-like
    try:
        text = widget.cget('text')
        info += f", text={text}"
    except Exception:
        pass
    print(info)
    for child in widget.winfo_children():
        summarize(child, indent+2)

root.update_idletasks()
summarize(root)

# print specific probe: find Entry and Label texts
entries = root.eval('winfo children .')
print('\nTop-level children (root):', entries)

# Destroy without entering mainloop
root.destroy()
print('\nDone')
