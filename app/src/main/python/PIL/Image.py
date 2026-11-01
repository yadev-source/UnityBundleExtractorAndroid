# Dummy PIL.Image - no native libs needed
class DummyImg:
    def __init__(self, *a, **k): pass
    def save(self, *a, **k): raise RuntimeError("Texture export disabled on Android - use PC")
    def tobytes(self, *a, **k): return b""
    @property
    def size(self): return (0,0)

def open(*a, **k):
    return DummyImg()

def new(*a, **k):
    return DummyImg()

def frombytes(*a, **k):
    return DummyImg()

def frombuffer(*a, **k):
    return DummyImg()

# constants yang dipakai UnityPy
FLIP_TOP_BOTTOM = 0
RAW = "RAW"
RGBA = "RGBA"