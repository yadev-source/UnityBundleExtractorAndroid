# Dummy tkinter package - iterable
import sys, types

class Dummy:
    def __init__(self, *a, **k): pass
    def __call__(self, *a, **k): return Dummy()
    def __getattr__(self, name): return Dummy()
    def __getitem__(self, key): return Dummy()
    def __setitem__(self, k, v): pass
    def __iter__(self): return iter([])
    def __bool__(self): return False
    def __contains__(self, i): return False
    def __str__(self): return ""
    def __repr__(self): return "Dummy"

Tk = Dummy()
Frame = Dummy()
Label = Dummy()
Button = Dummy()
Canvas = Dummy()
Widget = Dummy()
Tcl = Dummy

def __getattr__(name):
    # Auto-create submodule dummy kayak messagebox, filedialog, etc
    mod = types.ModuleType(f"tkinter.{name}")
    mod.__getattr__ = lambda n: Dummy()
    # Semua atribut di submodule juga Dummy
    for attr in ["showinfo", "showerror", "askyesno", "askopenfilename", "Tk", "Frame"]:
        setattr(mod, attr, Dummy())
    sys.modules[f"tkinter.{name}"] = mod
    return mod
