class Dummy:
    def __call__(self, *a, **k): return False
    def __getattr__(self, n): return Dummy()
def showinfo(*a, **k): return None
def showerror(*a, **k): return None
def showwarning(*a, **k): return None
def askyesno(*a, **k): return False
