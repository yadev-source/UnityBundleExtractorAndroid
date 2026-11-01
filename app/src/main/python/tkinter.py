# Dummy tkinter - iterable version
class Dummy:
    def __init__(self, *a, **k): pass
    def __call__(self, *a, **k): return Dummy()
    def __getattr__(self, name): return Dummy()
    def __getitem__(self, key): return Dummy()
    def __setitem__(self, key, val): pass
    def __iter__(self): return iter([])
    def __bool__(self): return False
    def __contains__(self, item): return False
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
    return Dummy()

__all__ = []
