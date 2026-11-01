class ImageDraw:
    def __init__(self, *a, **k): pass
    def Draw(self, *a, **k): return self
    def rectangle(self, *a, **k): pass
    def text(self, *a, **k): pass
    def __getattr__(self, n): return lambda *a, **k: None

def Draw(*a, **k):
    return ImageDraw()