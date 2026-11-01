# Dummy tkinter module
class Dummy:
    def __init__(self, *a, **k): pass
    def __call__(self, *a, **k): return Dummy()
    def __getattr__(self, name): return Dummy()
    def __getattribute__(self, name): 
        try:
            return object.__getattribute__(self, name)
        except:
            return Dummy()

Tk = Dummy
Frame = Dummy
Label = Dummy
Button = Dummy
Canvas = Dummy

def __getattr__(name):
    return Dummy()
